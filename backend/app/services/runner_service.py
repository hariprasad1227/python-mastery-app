"""
Python Mastery - Runner Service
Bridges API endpoints to the isolated subprocess execution runner.
"""

from typing import Dict, Any, List, Optional
from runner.runner import execute_learner_code
from backend.app.schemas.runner import ExecuteRequest, ExecuteResponse, TestResultItem


def run_code_in_sandbox(request: ExecuteRequest) -> ExecuteResponse:
    """
    Invokes the safe runner sandbox for the learner's code.
    """
    test_cases_dicts = [
        tc.model_dump() if hasattr(tc, "model_dump") else tc
        for tc in request.test_cases
    ]
    result = execute_learner_code(
        code=request.code,
        entry_function_name=request.entry_function_name,
        test_cases=test_cases_dicts,
        timeout_seconds=request.timeout_seconds or 3.0
    )

    formatted_results = [
        TestResultItem(
            test_index=tr.get("test_index", 0),
            description=tr.get("description", ""),
            is_hidden=tr.get("is_hidden", False),
            passed=tr.get("passed", False),
            input=tr.get("input"),
            expected=tr.get("expected"),
            actual=tr.get("actual"),
            error=tr.get("error")
        )
        for tr in result.get("test_results", [])
    ]

    return ExecuteResponse(
        passed=result.get("passed", False),
        stdout=result.get("stdout", ""),
        stderr=result.get("stderr", ""),
        execution_time_ms=result.get("execution_time_ms", 0),
        test_results=formatted_results,
        status=result.get("status", "unknown")
    )
