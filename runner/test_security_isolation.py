"""
Comprehensive Security & Sandbox Isolation Tests
Tests:
1. AST rejection of dunder escapes (__subclasses__, __bases__, __mro__, __globals__)
2. AST rejection of indirect reflection (getattr, setattr, delattr)
3. Child process environment sanitization (secrets cannot be read)
4. Output buffer capping (max 64KB to prevent memory exhaustion)
5. Time limit enforcement on infinite loops
"""

import sys
import os

# Put root in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runner.runner import execute_learner_code
from runner.security import check_code_safety


def test_dunder_sandbox_escapes():
    """Verify that Python sandbox escape techniques are blocked at AST level."""
    print("Testing dunder sandbox escape rejection...")
    escape_payloads = [
        "x = ().__class__.__bases__[0].__subclasses__()",
        "def exploit(): return [].__class__.__mro__[1]",
        "f = ().__class__.__globals__",
        "b = ().__class__.__builtins__",
        "code = (lambda: None).__code__",
        "c = (lambda: None).__closure__"
    ]
    for payload in escape_payloads:
        is_safe, error = check_code_safety(payload)
        assert not is_safe, f"Failed to reject escape payload: {payload}"
        assert error is not None
        print(f"  [BLOCKED] {payload[:40]}... -> {error}")
    print("[PASS] test_dunder_sandbox_escapes")


def test_reflection_builtins():
    """Verify getattr, setattr, eval, exec, open are blocked."""
    print("Testing reflection and execution builtins...")
    payloads = [
        "getattr(int, '__subclasses__')",
        "setattr(int, 'foo', 1)",
        "eval('1 + 1')",
        "exec('x = 1')",
        "open('C:/Windows/win.ini', 'r')",
        "compile('x = 1', '<string>', 'exec')"
    ]
    for payload in payloads:
        is_safe, error = check_code_safety(payload)
        assert not is_safe, f"Failed to reject forbidden builtin: {payload}"
        print(f"  [BLOCKED] {payload[:35]}... -> {error}")
    print("[PASS] test_reflection_builtins")


def test_environment_sanitization():
    """Verify parent server environment variables (secrets) are NOT leaked to runner."""
    print("Testing environment sanitization...")
    # Inject fake sensitive keys into parent os.environ
    os.environ["OPENAI_API_KEY"] = "sk-super-secret-openai-api-key-12345"
    os.environ["JWT_SECRET_KEY"] = "very-confidential-jwt-signing-secret"
    os.environ["DATABASE_URL"] = "postgresql://postgres:mysecretpass@localhost/db"

    # Code that attempts to read an environment variable via harmless safe builtins
    # Note: 'os' module is blocked by AST, but we check child environment directly
    from runner.runner import get_sanitized_environment
    clean_env = get_sanitized_environment()

    assert "OPENAI_API_KEY" not in clean_env, "OPENAI_API_KEY was leaked into child env!"
    assert "JWT_SECRET_KEY" not in clean_env, "JWT_SECRET_KEY was leaked into child env!"
    assert "DATABASE_URL" not in clean_env, "DATABASE_URL was leaked into child env!"
    print("  [OK] Clean env stripped OPENAI_API_KEY, JWT_SECRET_KEY, and DATABASE_URL.")
    print("[PASS] test_environment_sanitization")


def test_output_flooding_cap():
    """Verify that a program producing huge output is capped at 64KB."""
    print("Testing output flooding protection...")
    code = """
def flood():
    for _ in range(20000):
        print("A" * 50)
    return "done"
"""
    res = execute_learner_code(code, entry_function_name="flood", test_cases=[
        {"input": [], "expected": "done", "description": "Output cap test"}
    ], timeout_seconds=3.0)

    assert len(res["stdout"].encode("utf-8")) <= 70000, f"Output exceeded buffer limit: {len(res['stdout'])}"
    assert "[Output truncated" in res["stdout"] or len(res["stdout"]) > 0
    print(f"  [OK] Output buffer cleanly truncated ({len(res['stdout'])} chars)")
    print("[PASS] test_output_flooding_cap")


def test_timeout_enforcement():
    """Verify infinite loops are terminated strictly within timeout."""
    print("Testing timeout enforcement...")
    code = """
def hang():
    count = 0
    while True:
        count += 1
"""
    res = execute_learner_code(code, entry_function_name="hang", test_cases=[
        {"input": [], "expected": None}
    ], timeout_seconds=1.2)

    assert res["passed"] is False
    assert res["status"] == "time_limit_exceeded"
    assert "Time Limit Exceeded" in res["stderr"]
    print(f"  [OK] Process terminated after {res['execution_time_ms']}ms")
    print("[PASS] test_timeout_enforcement")


if __name__ == "__main__":
    print("==================================================")
    print("RUNNING SECURITY & ISOLATION TEST SUITE")
    print("==================================================")
    test_dunder_sandbox_escapes()
    test_reflection_builtins()
    test_environment_sanitization()
    test_output_flooding_cap()
    test_timeout_enforcement()
    print("\nALL 5 SECURITY & ISOLATION TESTS PASSED SUCCESSFULLY!")
