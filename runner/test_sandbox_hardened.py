"""
Comprehensive Hardened Sandbox Test Suite
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runner.runner import execute_learner_code, get_sanitized_environment
from runner.security import check_code_safety


def test_safe_arithmetic():
    print("Testing safe arithmetic...")
    code = """
def calculate(x, y):
    return (x + y) * 2
"""
    res = execute_learner_code(
        code=code,
        entry_function_name="calculate",
        test_cases=[{"input": [3, 4], "expected": 14}],
        timeout_seconds=2.0
    )
    assert res["passed"] is True, f"Expected pass, got: {res}"
    assert res["test_results"][0]["actual"] == 14
    print("  [PASS] test_safe_arithmetic")


def test_stability_ten_repetitions():
    print("Testing stability across 10 consecutive executions...")
    code = """
def add(a, b):
    return a + b
"""
    for i in range(10):
        res = execute_learner_code(
            code=code,
            entry_function_name="add",
            test_cases=[{"input": [i, i * 2], "expected": i * 3}],
            timeout_seconds=2.0
        )
        assert res["passed"] is True, f"Run {i} failed: {res}"
        assert res["status"] == "success"
    print("  [PASS] test_stability_ten_repetitions (10/10 passed)")


def test_infinite_loop_timeout():
    print("Testing infinite loop timeout enforcement...")
    code = """
def run():
    while True:
        pass
"""
    t0 = time.time()
    res = execute_learner_code(
        code=code,
        entry_function_name="run",
        test_cases=[{"input": [], "expected": None}],
        timeout_seconds=1.0
    )
    elapsed = time.time() - t0
    assert res["passed"] is False
    assert res["status"] == "time_limit_exceeded"
    assert "Time Limit Exceeded" in res["stderr"]
    print(f"  [PASS] test_infinite_loop_timeout (caught in {elapsed:.2f}s)")


def test_excessive_output_truncation():
    print("Testing 64KB max buffer output truncation...")
    code = """
def flood():
    print("A" * 200000)
    return True
"""
    res = execute_learner_code(
        code=code,
        entry_function_name="flood",
        test_cases=[{"input": [], "expected": True}],
        timeout_seconds=3.0
    )
    assert len(res["stdout"]) < 70000
    assert "[Output truncated: exceeded 64KB output limit]" in res["stdout"]
    print("  [PASS] test_excessive_output_truncation")


def test_filesystem_access_blocked():
    print("Testing filesystem access blocked...")
    code = """
def read_secrets():
    f = open("C:/Windows/win.ini")
    return f.read()
"""
    res = execute_learner_code(code, entry_function_name="read_secrets", test_cases=[])
    assert res["passed"] is False
    assert res["status"] == "security_violation"
    assert "open()" in res["stderr"]
    print("  [PASS] test_filesystem_access_blocked")


def test_environment_secret_leak_prevention():
    print("Testing parent secret leakage prevention...")
    os.environ["OPENAI_API_KEY"] = "sk-super-secret-key-12345"
    os.environ["DATABASE_URL"] = "postgresql://admin:secretpass@db.local/mastery"
    os.environ["JWT_SECRET_KEY"] = "super-secret-jwt-signing-key"

    clean_env = get_sanitized_environment()
    assert "OPENAI_API_KEY" not in clean_env
    assert "DATABASE_URL" not in clean_env
    assert "JWT_SECRET_KEY" not in clean_env
    print("  [PASS] test_environment_secret_leak_prevention")


def test_prohibited_imports():
    print("Testing prohibited module imports rejection...")
    forbidden = ["os", "sys", "subprocess", "shutil", "socket", "urllib", "requests", "importlib"]
    for mod in forbidden:
        code = f"import {mod}\ndef exploit():\n    return True\n"
        is_safe, err = check_code_safety(code)
        assert is_safe is False, f"Module {mod} was not blocked!"
        assert f"'{mod}'" in err
    print("  [PASS] test_prohibited_imports (all 8 blocked)")


if __name__ == "__main__":
    print("=" * 50)
    print("RUNNING HARDENED SANDBOX TEST SUITE")
    print("=" * 50)
    test_safe_arithmetic()
    test_stability_ten_repetitions()
    test_infinite_loop_timeout()
    test_excessive_output_truncation()
    test_filesystem_access_blocked()
    test_environment_secret_leak_prevention()
    test_prohibited_imports()
    print("=" * 50)
    print("ALL 7 HARDENED SANDBOX TESTS PASSED SUCCESSFULLY!")
    print("=" * 50)
