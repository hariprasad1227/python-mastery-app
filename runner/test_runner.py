"""
Verification Unit Tests for Python Mastery Execution Sandbox
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runner.runner import execute_learner_code


def test_successful_execution():
    code = """
def add(a, b):
    return a + b
"""
    test_cases = [
        {"input": [2, 3], "expected": 5, "description": "2 + 3 = 5"},
        {"input": [-1, 1], "expected": 0, "description": "-1 + 1 = 0"}
    ]
    res = execute_learner_code(code, entry_function_name="add", test_cases=test_cases)
    assert res["passed"] is True, f"Expected passed=True, got {res}"
    assert len(res["test_results"]) == 2
    print("[PASS] test_successful_execution")


def test_failed_assertion():
    code = """
def add(a, b):
    return a - b  # Bug
"""
    test_cases = [
        {"input": [2, 3], "expected": 5, "description": "2 + 3 = 5"}
    ]
    res = execute_learner_code(code, entry_function_name="add", test_cases=test_cases)
    assert res["passed"] is False
    assert res["test_results"][0]["passed"] is False
    assert res["test_results"][0]["actual"] == -1
    print("[PASS] test_failed_assertion")


def test_infinite_loop_timeout():
    code = """
def loop_forever():
    while True:
        pass
"""
    test_cases = [{"input": [], "expected": 1, "description": "Never finishes"}]
    res = execute_learner_code(code, entry_function_name="loop_forever", test_cases=test_cases, timeout_seconds=1.5)
    assert res["passed"] is False
    assert res["status"] == "time_limit_exceeded"
    assert "Time Limit Exceeded" in res["stderr"]
    print("[PASS] test_infinite_loop_timeout")


def test_security_violation_os():
    code = """
import os
def hack():
    os.listdir(".")
"""
    res = execute_learner_code(code, entry_function_name="hack")
    assert res["passed"] is False
    assert res["status"] == "security_violation"
    assert "Security Notice" in res["stderr"]
    assert "prohibited" in res["stderr"]
    print("[PASS] test_security_violation_os")


def test_security_violation_eval():
    code = """
def danger():
    return eval("1 + 1")
"""
    res = execute_learner_code(code, entry_function_name="danger")
    assert res["passed"] is False
    assert res["status"] == "security_violation"
    print("[PASS] test_security_violation_eval")


if __name__ == "__main__":
    print("Running sandbox verification tests...")
    test_successful_execution()
    test_failed_assertion()
    test_infinite_loop_timeout()
    test_security_violation_os()
    test_security_violation_eval()
    print("\nALL SANDBOX TESTS PASSED SUCCESSFULLY!")
