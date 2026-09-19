"""
Python Mastery - Sandbox Test Harness
Executes user code within an isolated scope and evaluates outputs or functions against test cases.
Output is serialized as a JSON string to stdout.
"""

import sys
import io
import json
import traceback
import time
from typing import Any, Dict, List


def run_harness(payload: Dict[str, Any]) -> Dict[str, Any]:
    code = payload.get("code", "")
    entry_function_name = payload.get("entry_function_name")
    test_cases = payload.get("test_cases", [])

    # Redirect stdout and stderr
    captured_stdout = io.StringIO()
    captured_stderr = io.StringIO()
    sys.stdout = captured_stdout
    sys.stderr = captured_stderr

    ALLOWED_SANDBOX_MODULES = {
        "math", "json", "collections", "datetime", "itertools",
        "heapq", "re", "random", "functools", "string", "_strptime",
        "_datetime", "time"
    }

    def safe_import(name, *args, **kwargs):
        base_mod = name.split(".")[0]
        if base_mod not in ALLOWED_SANDBOX_MODULES:
            raise ImportError(f"Module '{name}' is restricted in sandbox.")
        return __import__(name, *args, **kwargs)

    # Restricted global namespace
    safe_globals = {
        "__name__": "__main__",
        "__builtins__": {
            # Standard safe builtins
            "abs": abs, "all": all, "any": any, "ascii": ascii, "bin": bin, "bool": bool,
            "bytearray": bytearray, "bytes": bytes, "callable": callable, "chr": chr,
            "complex": complex, "dict": dict, "divmod": divmod, "enumerate": enumerate,
            "filter": filter, "float": float, "format": format, "frozenset": frozenset,
            "hash": hash, "hex": hex, "int": int, "isinstance": isinstance,
            "issubclass": issubclass, "iter": iter, "len": len, "list": list, "map": map,
            "max": max, "min": min, "next": next, "oct": oct, "ord": ord, "pow": pow,
            "print": print, "range": range, "repr": repr, "reversed": reversed,
            "round": round, "set": set, "slice": slice, "sorted": sorted, "str": str,
            "sum": sum, "tuple": tuple, "type": type, "zip": zip,
            "super": super, "classmethod": classmethod, "staticmethod": staticmethod,
            "property": property, "__build_class__": __build_class__,
            "__import__": safe_import,
            "Exception": Exception, "ValueError": ValueError, "TypeError": TypeError,
            "IndexError": IndexError, "KeyError": KeyError, "ZeroDivisionError": ZeroDivisionError,
            "True": True, "False": False, "None": None
        }
    }

    start_time = time.perf_counter()
    compile_error = None
    runtime_error = None

    try:
        compiled = compile(code, "<learner_code>", "exec")
        exec(compiled, safe_globals)
    except Exception as e:
        runtime_error = traceback.format_exc()
        # Clean trace to avoid showing test harness internals
        trace_lines = runtime_error.splitlines()
        clean_lines = [l for l in trace_lines if "test_harness" not in l]
        runtime_error = "\n".join(clean_lines)

    execution_duration_ms = int((time.perf_counter() - start_time) * 1000)

    # Evaluate test cases
    test_results: List[Dict[str, Any]] = []
    all_passed = True

    if runtime_error:
        all_passed = False
    elif entry_function_name:
        # User is expected to define a function
        target_fn = safe_globals.get(entry_function_name)
        if not target_fn or not callable(target_fn):
            all_passed = False
            runtime_error = f"Expected function '{entry_function_name}' was not found in your code."
        else:
            for idx, tc in enumerate(test_cases):
                tc_inputs = tc.get("input", [])
                expected = tc.get("expected")
                desc = tc.get("description", f"Test {idx + 1}")
                is_hidden = tc.get("is_hidden", False)

                test_res = {
                    "test_index": idx,
                    "description": desc,
                    "is_hidden": is_hidden,
                    "passed": False,
                    "input": tc_inputs if not is_hidden else "[Hidden Test Case]",
                    "expected": expected if not is_hidden else "[Hidden]",
                    "actual": None,
                    "error": None
                }

                try:
                    actual = target_fn(*tc_inputs)
                    test_res["actual"] = actual if not is_hidden else "[Hidden]"
                    if actual == expected:
                        test_res["passed"] = True
                    else:
                        test_res["passed"] = False
                        all_passed = False
                except Exception as ex:
                    all_passed = False
                    test_res["error"] = f"{type(ex).__name__}: {str(ex)}"

                test_results.append(test_res)
    else:
        # Standard script output challenge
        captured_text = captured_stdout.getvalue().strip()
        for idx, tc in enumerate(test_cases):
            expected = str(tc.get("expected", "")).strip()
            passed = captured_text == expected
            if not passed:
                all_passed = False
            test_results.append({
                "test_index": idx,
                "description": tc.get("description", "Output verification"),
                "is_hidden": tc.get("is_hidden", False),
                "passed": passed,
                "input": "stdout",
                "expected": expected,
                "actual": captured_text,
                "error": None
            })

    stdout_val = captured_stdout.getvalue()
    stderr_val = captured_stderr.getvalue()
    if runtime_error:
        stderr_val = (stderr_val + "\n" + runtime_error).strip()

    is_passed = all_passed if len(test_cases) > 0 else (runtime_error is None and all_passed)

    return {
        "passed": is_passed,
        "stdout": stdout_val,
        "stderr": stderr_val,
        "execution_time_ms": execution_duration_ms,
        "test_results": test_results,
        "has_runtime_error": runtime_error is not None
    }


if __name__ == "__main__":
    # Expects payload via stdin or arguments
    try:
        raw_input_data = sys.stdin.read()
        payload = json.loads(raw_input_data)
        result = run_harness(payload)
        # Restore sys.stdout to output pure JSON result
        sys.stdout = sys.__stdout__
        print(json.dumps(result))
    except Exception as e:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        print(json.dumps({
            "passed": False,
            "stdout": "",
            "stderr": f"Harness Error: {str(e)}",
            "execution_time_ms": 0,
            "test_results": [],
            "has_runtime_error": True
        }))
