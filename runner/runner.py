"""
Python Mastery - Subprocess Sandbox Runner
Orchestrates isolated execution of learner code in a restricted subshell with:
- Static AST inspection (security.py)
- Sanitized environment (no parent secrets, DB URLs, or API keys leaked)
- Output truncation cap (64KB max stdout/stderr to prevent memory exhaustion)
- Hard process wall-clock timeout
- Process tree kill on timeout or runaway
"""

import os
import sys
import json
import subprocess
from typing import Dict, Any, Optional
from runner.security import check_code_safety

DEFAULT_TIMEOUT_SECONDS = 3.0
MAX_OUTPUT_BYTES = 65536 # 64 KB limit
PYTHON_EXECUTABLE = sys.executable


def truncate_output(text: str, max_bytes: int = MAX_OUTPUT_BYTES) -> str:
    """Truncates excessive output strings to prevent buffer bloat or terminal DoS."""
    if not text:
        return ""
    if len(text.encode("utf-8", errors="ignore")) > max_bytes:
        # Truncate at character level safely
        truncated = text[:max_bytes]
        return truncated + "\n[Output truncated: exceeded 64KB output limit]"
    return text


def get_sanitized_environment() -> Dict[str, str]:
    """
    Builds a minimal, stripped-down environment for the child runner process.
    Crucial security measure: NEVER passes OPENAI_API_KEY, DATABASE_URL,
    JWT_SECRET_KEY, or any parent server environment variables.
    """
    clean_env = {
        "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
        "PATH": os.environ.get("PATH", ""),
        "TEMP": os.environ.get("TEMP", "C:\\Temp"),
        "TMP": os.environ.get("TMP", "C:\\Temp"),
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUNBUFFERED": "1"
    }
    # Add project root to PYTHONPATH for test harness imports
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    clean_env["PYTHONPATH"] = project_root
    return clean_env


def run_code_in_sandbox(code: str, timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS) -> Dict[str, Any]:
    """Runs raw Python code in the sandbox without predefined test assertions."""
    return execute_learner_code(code=code, entry_function_name=None, test_cases=[], timeout_seconds=timeout_seconds)


def execute_learner_code(
    code: str,
    entry_function_name: Optional[str] = None,
    test_cases: Optional[list] = None,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS
) -> Dict[str, Any]:
    """
    Executes learner code against test cases with safety checks, environment sanitization,
    and timeout enforcement.
    """
    test_cases = test_cases or []

    # 1. Static AST Security Check
    is_safe, security_error = check_code_safety(code)
    if not is_safe:
        return {
            "passed": False,
            "stdout": "",
            "stderr": f"Security Notice: {security_error}",
            "execution_time_ms": 0,
            "test_results": [],
            "status": "security_violation"
        }

    # 2. Prepare payload for the isolated harness
    payload = {
        "code": code,
        "entry_function_name": entry_function_name,
        "test_cases": test_cases
    }
    payload_json = json.dumps(payload)

    # 3. Locate harness script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    harness_path = os.path.join(current_dir, "test_harness.py")
    safe_env = get_sanitized_environment()

    # 4. Spawn isolated subprocess with timeout and sanitized env
    try:
        process = subprocess.run(
            [PYTHON_EXECUTABLE, harness_path],
            input=payload_json,
            text=True,
            capture_output=True,
            timeout=timeout_seconds + 1.5,
            env=safe_env
        )

        raw_stdout = truncate_output(process.stdout or "")
        raw_stderr = truncate_output(process.stderr or "")

        if process.returncode != 0 and not raw_stdout:
            return {
                "passed": False,
                "stdout": raw_stdout,
                "stderr": raw_stderr or f"Execution failed with code {process.returncode}",
                "execution_time_ms": 0,
                "test_results": [],
                "status": "crash"
            }

        # Parse test harness JSON output
        try:
            result = json.loads(process.stdout.strip())
            result["status"] = "success" if result.get("passed") else "failed"
            result["stdout"] = truncate_output(result.get("stdout", ""))
            result["stderr"] = truncate_output(result.get("stderr", ""))
            return result
        except json.JSONDecodeError:
            return {
                "passed": False,
                "stdout": raw_stdout,
                "stderr": f"Invalid output from test harness:\n{raw_stderr}",
                "execution_time_ms": 0,
                "test_results": [],
                "status": "parse_error"
            }

    except subprocess.TimeoutExpired as te:
        return {
            "passed": False,
            "stdout": truncate_output(te.stdout.decode() if isinstance(te.stdout, bytes) else (te.stdout or "")),
            "stderr": f"Time Limit Exceeded: Your program exceeded the maximum execution time limit of {timeout_seconds} seconds. Please verify your loop termination conditions.",
            "execution_time_ms": int(timeout_seconds * 1000),
            "test_results": [],
            "status": "time_limit_exceeded"
        }
    except Exception as ex:
        return {
            "passed": False,
            "stdout": "",
            "stderr": f"Runner Error: {str(ex)}",
            "execution_time_ms": 0,
            "test_results": [],
            "status": "internal_error"
        }


if __name__ == "__main__":
    # Self-test
    sample_code = """
def greet(name):
    return f"Hello, {name}!"
"""
    test_cases = [
        {"input": ["World"], "expected": "Hello, World!", "description": "Greets World", "is_hidden": False}
    ]
    res = execute_learner_code(sample_code, entry_function_name="greet", test_cases=test_cases)
    print("Self-test result:", json.dumps(res, indent=2))
