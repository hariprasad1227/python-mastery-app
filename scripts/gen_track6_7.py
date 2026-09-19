import json

challenges = []

def add_chal(cid, idx, mod, slug, title, diff, inst, starter, sol, func, tests, hints, xp=100):
    challenges.append({
        "id": cid,
        "order_index": idx,
        "level_number": mod,
        "slug": slug,
        "title": title,
        "difficulty": diff,
        "instructions": inst,
        "starter_code": starter,
        "solution_code": sol,
        "entry_function_name": func,
        "test_cases": tests,
        "hints": hints,
        "xp_reward": xp,
        "time_limit_seconds": 300 + (idx * 2),
        "sandbox_timeout_seconds": 3.0
    })

# --- TRACK 6: Error Handling & Resilient Code (51-60) ---
add_chal("chal-51", 51, 6, "challenge-safe-divide", "Safe Integer Division", "easy",
         "Write `safe_divide(a: int, b: int)` returning a / b rounded to 2 decimals, or None if b == 0 using try-except ZeroDivisionError.",
         "def safe_divide(a: int, b: int):\n    pass\n",
         "def safe_divide(a: int, b: int):\n    try:\n        return round(a / b, 2)\n    except ZeroDivisionError:\n        return None\n",
         "safe_divide",
         [{"input": [10, 2], "expected": 5.0, "description": "10 / 2 = 5", "is_hidden": False},
          {"input": [5, 0], "expected": None, "description": "Division by zero returns None", "is_hidden": False},
          {"input": [10, 3], "expected": 3.33, "description": "10 / 3 = 3.33", "is_hidden": True}],
         ["Use try ... except ZeroDivisionError: return None."], 85)

add_chal("chal-52", 52, 6, "challenge-safe-get", "Safe Key Lookup with Default", "easy",
         "Write `safe_get(d: dict, key: str, default: any)` returning d[key] or default if KeyError occurs.",
         "def safe_get(d: dict, key: str, default: any):\n    pass\n",
         "def safe_get(d: dict, key: str, default: any):\n    try:\n        return d[key]\n    except KeyError:\n        return default\n",
         "safe_get",
         [{"input": [{"name": "Alice"}, "name", "Unknown"], "expected": "Alice", "description": "Key exists", "is_hidden": False},
          {"input": [{"name": "Alice"}, "age", 0], "expected": 0, "description": "Key missing returns default", "is_hidden": False},
          {"input": [{}, "any", None], "expected": None, "description": "Empty dict", "is_hidden": True}],
         ["Catch KeyError and return default."], 80)

add_chal("chal-53", 53, 6, "challenge-safe-index", "Index Range Guard", "easy",
         "Write `safe_index_lookup(lst: list, idx: int)` returning lst[idx] or 'Out of Bounds' if IndexError occurs.",
         "def safe_index_lookup(lst: list, idx: int):\n    pass\n",
         "def safe_index_lookup(lst: list, idx: int):\n    try:\n        return lst[idx]\n    except IndexError:\n        return 'Out of Bounds'\n",
         "safe_index_lookup",
         [{"input": [[10, 20, 30], 1], "expected": 20, "description": "Valid index", "is_hidden": False},
          {"input": [[10, 20], 5], "expected": "Out of Bounds", "description": "Index too high", "is_hidden": False},
          {"input": [[], 0], "expected": "Out of Bounds", "description": "Empty list lookup", "is_hidden": True}],
         ["Catch IndexError."], 80)

add_chal("chal-54", 54, 6, "challenge-validate-age", "Age Range Validator", "easy",
         "Write `validate_age(age: int) -> str` returning 'Valid' if 0 <= age <= 120, else raising ValueError and catching it to return 'Invalid Age'.",
         "def validate_age(age: int) -> str:\n    pass\n",
         "def validate_age(age: int) -> str:\n    try:\n        if age < 0 or age > 120:\n            raise ValueError('Age out of range')\n        return 'Valid'\n    except ValueError:\n        return 'Invalid Age'\n",
         "validate_age",
         [{"input": [25], "expected": "Valid", "description": "25 is valid", "is_hidden": False},
          {"input": [-1], "expected": "Invalid Age", "description": "-1 is invalid", "is_hidden": False},
          {"input": [150], "expected": "Invalid Age", "description": "150 is invalid", "is_hidden": True}],
         ["Raise and catch ValueError."], 85)

add_chal("chal-55", 55, 6, "challenge-parse-float-list", "Safe String to Float Parser", "medium",
         "Write `parse_float_list(str_list: list[str]) -> list[float]` converting string tokens to floats, ignoring tokens that raise ValueError.",
         "def parse_float_list(str_list: list[str]) -> list[float]:\n    pass\n",
         "def parse_float_list(str_list: list[str]) -> list[float]:\n    res = []\n    for s in str_list:\n        try:\n            res.append(float(s))\n        except ValueError:\n            continue\n    return res\n",
         "parse_float_list",
         [{"input": [["1.5", "abc", "3.0", "xyz", "4"]], "expected": [1.5, 3.0, 4.0], "description": "Mix of valid/invalid", "is_hidden": False},
          {"input": [["bad", "data"]], "expected": [], "description": "All invalid", "is_hidden": False},
          {"input": [["-2.5", "0.0"]], "expected": [-2.5, 0.0], "description": "Negatives and zeroes", "is_hidden": True}],
         ["Use try ... except ValueError in a loop."], 90)

add_chal("chal-56", 56, 6, "challenge-pop-safe", "Safe Stack Pop Handler", "easy",
         "Write `pop_safe(items: list)` returning items.pop() or None if items is empty without crashing.",
         "def pop_safe(items: list):\n    pass\n",
         "def pop_safe(items: list):\n    try:\n        return items.pop()\n    except IndexError:\n        return None\n",
         "pop_safe",
         [{"input": [[1, 2, 3]], "expected": 3, "description": "Non-empty pop", "is_hidden": False},
          {"input": [[]], "expected": None, "description": "Empty pop returns None", "is_hidden": False},
          {"input": [["solo"]], "expected": "solo", "description": "Single element pop", "is_hidden": True}],
         ["Catch IndexError on pop()."], 80)

add_chal("chal-57", 57, 6, "challenge-assert-positive", "All-Positive Array Assertion", "easy",
         "Write `assert_positive(nums: list[int]) -> bool` returning True if every number > 0, False if any <= 0.",
         "def assert_positive(nums: list[int]) -> bool:\n    pass\n",
         "def assert_positive(nums: list[int]) -> bool:\n    return all(x > 0 for x in nums)\n",
         "assert_positive",
         [{"input": [[1, 2, 3, 4]], "expected": True, "description": "All positive", "is_hidden": False},
          {"input": [[1, -2, 3]], "expected": False, "description": "Contains -2", "is_hidden": False},
          {"input": [[0, 5]], "expected": False, "description": "0 is not positive", "is_hidden": True}],
         ["Use all(x > 0 for x in nums)."], 75)

add_chal("chal-58", 58, 6, "challenge-nested-get", "Safe Nested Dictionary Access", "medium",
         "Write `nested_get(data: dict, keys: list[str])` traversing data along keys, returning None if any key is missing or not a dict.",
         "def nested_get(data: dict, keys: list[str]):\n    pass\n",
         "def nested_get(data: dict, keys: list[str]):\n    cur = data\n    for k in keys:\n        if not isinstance(cur, dict) or k not in cur:\n            return None\n        cur = cur[k]\n    return cur\n",
         "nested_get",
         [{"input": [{"user": {"profile": {"city": "Paris"}}}, ["user", "profile", "city"]], "expected": "Paris", "description": "3-level access", "is_hidden": False},
          {"input": [{"user": {"name": "Bob"}}, ["user", "age"]], "expected": None, "description": "Missing inner key", "is_hidden": False},
          {"input": [{}, ["any"]], "expected": None, "description": "Empty root", "is_hidden": True}],
         ["Traverse step by step.", "Verify isinstance(cur, dict)."], 95)

add_chal("chal-59", 59, 6, "challenge-safe-parse-json", "Safe JSON String Parsing", "easy",
         "Write `safe_parse_json(s: str) -> dict` parsing a JSON string using json.loads, returning {} if json.JSONDecodeError occurs.",
         "def safe_parse_json(s: str) -> dict:\n    pass\n",
         "def safe_parse_json(s: str) -> dict:\n    import json\n    try:\n        return json.loads(s)\n    except (json.JSONDecodeError, TypeError):\n        return {}\n",
         "safe_parse_json",
         [{"input": ["{\"a\": 1, \"b\": 2}"], "expected": {"a": 1, "b": 2}, "description": "Valid JSON", "is_hidden": False},
          {"input": ["not a json string"], "expected": {}, "description": "Invalid JSON returns {}", "is_hidden": False},
          {"input": ["{\"key\": [1, 2]}"], "expected": {"key": [1, 2]}, "description": "Nested list JSON", "is_hidden": True}],
         ["Use try json.loads(s) except (json.JSONDecodeError, TypeError): return {}."], 85)

add_chal("chal-60", 60, 6, "challenge-catch-type-error", "Type Incompatibility Detector", "easy",
         "Write `catch_type_error(a: any, b: any) -> bool` attempting `a + b` returning True if TypeError occurs, False if succeeds.",
         "def catch_type_error(a: any, b: any) -> bool:\n    pass\n",
         "def catch_type_error(a: any, b: any) -> bool:\n    try:\n        _ = a + b\n        return False\n    except TypeError:\n        return True\n",
         "catch_type_error",
         [{"input": [5, "10"], "expected": True, "description": "int + str raises TypeError", "is_hidden": False},
          {"input": [5, 10], "expected": False, "description": "int + int succeeds", "is_hidden": False},
          {"input": ["hello", "world"], "expected": False, "description": "str + str succeeds", "is_hidden": True}],
         ["Try a + b and catch TypeError."], 80)

# --- TRACK 7: Algorithms & Problem Solving (61-70) ---
add_chal("chal-61", 61, 7, "challenge-two-sum", "Two Sum Indices", "medium",
         "Write `two_sum(nums: list[int], target: int) -> list[int]` returning 0-indexed positions [i, j] of two numbers summing to target.",
         "def two_sum(nums: list[int], target: int) -> list[int]:\n    pass\n",
         "def two_sum(nums: list[int], target: int) -> list[int]:\n    seen = {}\n    for i, x in enumerate(nums):\n        diff = target - x\n        if diff in seen:\n            return [seen[diff], i]\n        seen[x] = i\n    return []\n",
         "two_sum",
         [{"input": [[2, 7, 11, 15], 9], "expected": [0, 1], "description": "2 + 7 = 9", "is_hidden": False},
          {"input": [[3, 2, 4], 6], "expected": [1, 2], "description": "2 + 4 = 6", "is_hidden": False},
          {"input": [[3, 3], 6], "expected": [0, 1], "description": "3 + 3 = 6", "is_hidden": True}],
         ["Use a hash map to store value -> index.", "Lookup target - x."], 100)

add_chal("chal-62", 62, 7, "challenge-binary-search", "Binary Search Algorithm", "medium",
         "Write `binary_search(arr: list[int], target: int) -> int` returning the index of target in sorted arr, or -1 if not found in O(log n).",
         "def binary_search(arr: list[int], target: int) -> int:\n    pass\n",
         "def binary_search(arr: list[int], target: int) -> int:\n    lo, hi = 0, len(arr) - 1\n    while lo <= hi:\n        mid = (lo + hi) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            lo = mid + 1\n        else:\n            hi = mid - 1\n    return -1\n",
         "binary_search",
         [{"input": [[1, 3, 5, 7, 9, 11], 7], "expected": 3, "description": "Search 7", "is_hidden": False},
          {"input": [[1, 3, 5], 4], "expected": -1, "description": "Missing element", "is_hidden": False},
          {"input": [[10, 20, 30], 10], "expected": 0, "description": "First element", "is_hidden": True}],
         ["Maintain lo and hi pointers.", "Check middle element each step."], 100)

add_chal("chal-63", 63, 7, "challenge-max-sub-array", "Maximum Subarray Sum (Kadane's)", "medium",
         "Write `max_sub_array(nums: list[int]) -> int` returning the largest sum of any contiguous subarray.",
         "def max_sub_array(nums: list[int]) -> int:\n    pass\n",
         "def max_sub_array(nums: list[int]) -> int:\n    max_so_far = nums[0]\n    cur_max = nums[0]\n    for x in nums[1:]:\n        cur_max = max(x, cur_max + x)\n        max_so_far = max(max_so_far, cur_max)\n    return max_so_far\n",
         "max_sub_array",
         [{"input": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected": 6, "description": "[4,-1,2,1] has sum 6", "is_hidden": False},
          {"input": [[1]], "expected": 1, "description": "Single element", "is_hidden": False},
          {"input": [[5, 4, -1, 7, 8]], "expected": 23, "description": "All positive sum", "is_hidden": True}],
         ["Use Kadane's Algorithm: cur_max = max(x, cur_max + x)."], 110)

add_chal("chal-64", 64, 7, "challenge-merge-sorted", "Merge Two Sorted Lists", "medium",
         "Write `merge_sorted(a: list[int], b: list[int]) -> list[int]` merging two sorted lists into one sorted list in O(n+m).",
         "def merge_sorted(a: list[int], b: list[int]) -> list[int]:\n    pass\n",
         "def merge_sorted(a: list[int], b: list[int]) -> list[int]:\n    i, j = 0, 0\n    res = []\n    while i < len(a) and j < len(b):\n        if a[i] <= b[j]:\n            res.append(a[i])\n            i += 1\n        else:\n            res.append(b[j])\n            j += 1\n    res.extend(a[i:])\n    res.extend(b[j:])\n    return res\n",
         "merge_sorted",
         [{"input": [[1, 3, 5], [2, 4, 6]], "expected": [1, 2, 3, 4, 5, 6], "description": "Equal length merge", "is_hidden": False},
          {"input": [[], [1, 2]], "expected": [1, 2], "description": "One empty list", "is_hidden": False},
          {"input": [[1, 5, 9], [2, 3]], "expected": [1, 2, 3, 5, 9], "description": "Unequal lengths", "is_hidden": True}],
         ["Use two pointers i and j.", "Append smaller element and advance pointer."], 100)

add_chal("chal-65", 65, 7, "challenge-valid-parentheses", "Valid Balanced Parentheses", "medium",
         "Write `is_valid_parentheses(s: str) -> bool` checking if bracket pairs '()', '[]', '{}' are correctly matched and closed in order.",
         "def is_valid_parentheses(s: str) -> bool:\n    pass\n",
         "def is_valid_parentheses(s: str) -> bool:\n    stack = []\n    mapping = {')': '(', ']': '[', '}': '{'}\n    for c in s:\n        if c in '([{':\n            stack.append(c)\n        elif c in mapping:\n            if not stack or stack[-1] != mapping[c]:\n                return False\n            stack.pop()\n    return len(stack) == 0\n",
         "is_valid_parentheses",
         [{"input": ["()[]{}"], "expected": True, "description": "Multiple valid pairs", "is_hidden": False},
          {"input": ["(]"], "expected": False, "description": "Mismatched pair", "is_hidden": False},
          {"input": ["([{}])"], "expected": True, "description": "Nested brackets", "is_hidden": True}],
         ["Use a stack for open brackets.", "Pop and match when closing bracket seen."], 110)

add_chal("chal-66", 66, 7, "challenge-rotate-array", "Rotate Array by K Steps", "medium",
         "Write `rotate_array(nums: list[int], k: int) -> list[int]` rotating array elements to the right by k steps.",
         "def rotate_array(nums: list[int], k: int) -> list[int]:\n    pass\n",
         "def rotate_array(nums: list[int], k: int) -> list[int]:\n    if not nums:\n        return []\n    k = k % len(nums)\n    return nums[-k:] + nums[:-k]\n",
         "rotate_array",
         [{"input": [[1, 2, 3, 4, 5, 6, 7], 3], "expected": [5, 6, 7, 1, 2, 3, 4], "description": "Rotate right by 3", "is_hidden": False},
          {"input": [[-1, -100, 3, 99], 2], "expected": [3, 99, -1, -100], "description": "Rotate right by 2", "is_hidden": False},
          {"input": [[1, 2], 0], "expected": [1, 2], "description": "Rotate by 0", "is_hidden": True}],
         ["Calculate effective k = k % len(nums).", "Slice nums[-k:] + nums[:-k]."], 95)

add_chal("chal-67", 67, 7, "challenge-run-length-encode", "Run-Length String Encoding", "medium",
         "Write `run_length_encode(text: str) -> str` compressing consecutive repeating characters e.g. 'AAABBC' -> 'A3B2C1' (empty string -> '').",
         "def run_length_encode(text: str) -> str:\n    pass\n",
         "def run_length_encode(text: str) -> str:\n    if not text:\n        return ''\n    res = []\n    cur_ch = text[0]\n    count = 1\n    for ch in text[1:]:\n        if ch == cur_ch:\n            count += 1\n        else:\n            res.append(f'{cur_ch}{count}')\n            cur_ch = ch\n            count = 1\n    res.append(f'{cur_ch}{count}')\n    return ''.join(res)\n",
         "run_length_encode",
         [{"input": ["AAABBC"], "expected": "A3B2C1", "description": "AAABBC", "is_hidden": False},
          {"input": ["A"], "expected": "A1", "description": "Single char", "is_hidden": False},
          {"input": ["WWWWWW"], "expected": "W6", "description": "Repeated 6 times", "is_hidden": True}],
         ["Track current character and count.", "Append when character changes."], 105)

add_chal("chal-68", 68, 7, "challenge-int-sqrt", "Integer Square Root Floor", "easy",
         "Write `int_sqrt(n: int) -> int` returning floor(sqrt(n)) without importing math.",
         "def int_sqrt(n: int) -> int:\n    pass\n",
         "def int_sqrt(n: int) -> int:\n    if n < 0:\n        return 0\n    return int(n ** 0.5)\n",
         "int_sqrt",
         [{"input": [16], "expected": 4, "description": "sqrt(16) = 4", "is_hidden": False},
          {"input": [8], "expected": 2, "description": "sqrt(8) floor = 2", "is_hidden": False},
          {"input": [0], "expected": 0, "description": "sqrt(0) = 0", "is_hidden": True}],
         ["Use int(n ** 0.5)."], 80)

add_chal("chal-69", 69, 7, "challenge-move-zeroes", "Move Zeroes to End", "easy",
         "Write `move_zeroes(nums: list[int]) -> list[int]` moving all 0s to the end while maintaining relative order of non-zero elements.",
         "def move_zeroes(nums: list[int]) -> list[int]:\n    pass\n",
         "def move_zeroes(nums: list[int]) -> list[int]:\n    non_zeros = [x for x in nums if x != 0]\n    zeros = [0] * (len(nums) - len(non_zeros))\n    return non_zeros + zeros\n",
         "move_zeroes",
         [{"input": [[0, 1, 0, 3, 12]], "expected": [1, 3, 12, 0, 0], "description": "Two zeroes moved", "is_hidden": False},
          {"input": [[0]], "expected": [0], "description": "Single zero", "is_hidden": False},
          {"input": [[1, 2, 3]], "expected": [1, 2, 3], "description": "No zeroes", "is_hidden": True}],
         ["Collect non-zeros and append zeros count."], 80)

add_chal("chal-70", 70, 7, "challenge-climb-stairs", "Climbing Stairs Possibilities", "medium",
         "Write `climb_stairs(n: int) -> int` returning number of distinct ways to climb n steps taking 1 or 2 steps at a time (e.g. n=1 -> 1, n=2 -> 2, n=3 -> 3).",
         "def climb_stairs(n: int) -> int:\n    pass\n",
         "def climb_stairs(n: int) -> int:\n    if n <= 2:\n        return max(0, n)\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b\n",
         "climb_stairs",
         [{"input": [2], "expected": 2, "description": "2 steps = 2 ways", "is_hidden": False},
          {"input": [3], "expected": 3, "description": "3 steps = 3 ways", "is_hidden": False},
          {"input": [5], "expected": 8, "description": "5 steps = 8 ways", "is_hidden": True}],
         ["Fibonacci relation: ways(n) = ways(n-1) + ways(n-2)."], 100)

with open("scripts/track6_7.json", "w", encoding="utf-8") as f:
    json.dump(challenges, f, indent=2)
print("Track 6 & 7 generated: 20 challenges")
