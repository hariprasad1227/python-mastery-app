import json

challenges = []

def add_chal(cid, idx, mod, slug, title, diff, inst, starter, sol, func, tests, hints, xp=120):
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

# --- TRACK 9: Python Standard Library & Collections (81-90) ---
add_chal("chal-81", 81, 9, "challenge-group-by-initial", "Group Words by Initial Letter", "easy",
         "Write `group_by_initial(words: list[str]) -> dict[str, list[str]]` grouping words by their lowercase first letter.",
         "def group_by_initial(words: list[str]) -> dict[str, list[str]]:\n    pass\n",
         "def group_by_initial(words: list[str]) -> dict[str, list[str]]:\n    groups = {}\n    for w in words:\n        if not w:\n            continue\n        init = w[0].lower()\n        groups.setdefault(init, []).append(w)\n    return groups\n",
         "group_by_initial",
         [{"input": [["apple", "banana", "apricot", "cherry", "blueberry"]], "expected": {"a": ["apple", "apricot"], "b": ["banana", "blueberry"], "c": ["cherry"]}, "description": "Initial grouping", "is_hidden": False},
          {"input": [[]], "expected": {}, "description": "Empty list", "is_hidden": False},
          {"input": [["Zebra", "zoo"]], "expected": {"z": ["Zebra", "zoo"]}, "description": "Case insensitive key", "is_hidden": True}],
         ["Use dict.setdefault(init, []).append(w)."], 85)

add_chal("chal-82", 82, 9, "challenge-top-k-frequent", "Top K Frequent Elements", "medium",
         "Write `top_k_frequent(items: list, k: int) -> list` returning the k most frequent elements sorted by frequency descending.",
         "def top_k_frequent(items: list, k: int) -> list:\n    pass\n",
         "def top_k_frequent(items: list, k: int) -> list:\n    from collections import Counter\n    counts = Counter(items)\n    sorted_items = sorted(counts.keys(), key=lambda x: (-counts[x], str(x)))\n    return sorted_items[:k]\n",
         "top_k_frequent",
         [{"input": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2], "description": "Top 2 frequent", "is_hidden": False},
          {"input": [["a", "b", "c"], 1], "expected": ["a"], "description": "Top 1 with tie", "is_hidden": False},
          {"input": [[4, 4, 4, 4], 1], "expected": [4], "description": "Single dominant item", "is_hidden": True}],
         ["Use collections.Counter.", "Sort by count descending."], 105)

add_chal("chal-83", 83, 9, "challenge-moving-average", "Moving Average Calculator", "medium",
         "Write `moving_average(data: list[float], window: int) -> list[float]` computing moving averages of size window rounded to 2 decimals.",
         "def moving_average(data: list[float], window: int) -> list[float]:\n    pass\n",
         "def moving_average(data: list[float], window: int) -> list[float]:\n    if len(data) < window or window <= 0:\n        return []\n    res = []\n    for i in range(len(data) - window + 1):\n        avg = sum(data[i:i + window]) / window\n        res.append(round(avg, 2))\n    return res\n",
         "moving_average",
         [{"input": [[1, 2, 3, 4, 5], 3], "expected": [2.0, 3.0, 4.0], "description": "Window of 3", "is_hidden": False},
          {"input": [[10, 20], 3], "expected": [], "description": "Window > len returns []", "is_hidden": False},
          {"input": [[4.0, 4.0, 4.0], 2], "expected": [4.0, 4.0], "description": "Identical floats", "is_hidden": True}],
         ["Sum slice of size window and divide by window."], 100)

add_chal("chal-84", 84, 9, "challenge-group-consecutive", "Group Consecutive Elements", "medium",
         "Write `group_consecutive(lst: list) -> list[list]` grouping consecutive equal items together.",
         "def group_consecutive(lst: list) -> list[list]:\n    pass\n",
         "def group_consecutive(lst: list) -> list[list]:\n    if not lst:\n        return []\n    res = []\n    cur = [lst[0]]\n    for x in lst[1:]:\n        if x == cur[0]:\n            cur.append(x)\n        else:\n            res.append(cur)\n            cur = [x]\n    res.append(cur)\n    return res\n",
         "group_consecutive",
         [{"input": [[1, 1, 2, 3, 3]], "expected": [[1, 1], [2], [3, 3]], "description": "1, 1, 2, 3, 3", "is_hidden": False},
          {"input": [["a", "b", "c"]], "expected": [["a"], ["b"], ["c"]], "description": "All distinct", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty list", "is_hidden": True}],
         ["Group while x == cur[0]."], 95)

add_chal("chal-85", 85, 9, "challenge-euclidean-distance", "Euclidean Distance 2D", "easy",
         "Write `euclidean_distance(p1: list[float], p2: list[float]) -> float` returning distance between [x1, y1] and [x2, y2] rounded to 2 decimals.",
         "def euclidean_distance(p1: list[float], p2: list[float]) -> float:\n    pass\n",
         "def euclidean_distance(p1: list[float], p2: list[float]) -> float:\n    dx = p1[0] - p2[0]\n    dy = p1[1] - p2[1]\n    return round((dx*dx + dy*dy)**0.5, 2)\n",
         "euclidean_distance",
         [{"input": [[0.0, 0.0], [3.0, 4.0]], "expected": 5.0, "description": "3-4-5 triangle", "is_hidden": False},
          {"input": [[1.0, 1.0], [1.0, 1.0]], "expected": 0.0, "description": "Same point", "is_hidden": False},
          {"input": [[-2.0, -3.0], [1.0, 1.0]], "expected": 5.0, "description": "Negatives", "is_hidden": True}],
         ["Formula: sqrt((x2 - x1)^2 + (y2 - y1)^2)."], 80)

add_chal("chal-86", 86, 9, "challenge-days-between", "Days Between Two Dates", "easy",
         "Write `days_between(d1: str, d2: str) -> int` returning absolute number of days between two 'YYYY-MM-DD' formatted dates.",
         "def days_between(d1: str, d2: str) -> int:\n    pass\n",
         "def days_between(d1: str, d2: str) -> int:\n    from datetime import datetime\n    dt1 = datetime.strptime(d1, '%Y-%m-%d')\n    dt2 = datetime.strptime(d2, '%Y-%m-%d')\n    return abs((dt2 - dt1).days)\n",
         "days_between",
         [{"input": ["2026-01-01", "2026-01-10"], "expected": 9, "description": "9 days", "is_hidden": False},
          {"input": ["2025-12-31", "2026-01-01"], "expected": 1, "description": "1 day new year", "is_hidden": False},
          {"input": ["2024-02-28", "2024-03-01"], "expected": 2, "description": "Leap year day", "is_hidden": True}],
         ["Use datetime.strptime.", "Subtract datetimes and get .days."], 85)

add_chal("chal-87", 87, 9, "challenge-k-smallest", "Find K Smallest Elements", "easy",
         "Write `k_smallest(nums: list[int], k: int) -> list[int]` returning the k smallest numbers in ascending order.",
         "def k_smallest(nums: list[int], k: int) -> list[int]:\n    pass\n",
         "def k_smallest(nums: list[int], k: int) -> list[int]:\n    return sorted(nums)[:k]\n",
         "k_smallest",
         [{"input": [[7, 10, 4, 3, 20, 15], 3], "expected": [3, 4, 7], "description": "3 smallest", "is_hidden": False},
          {"input": [[1, 2], 5], "expected": [1, 2], "description": "k > len", "is_hidden": False},
          {"input": [[-5, -1, -10], 2], "expected": [-10, -5], "description": "Negative numbers", "is_hidden": True}],
         ["Use sorted(nums)[:k]."], 75)

add_chal("chal-88", 88, 9, "challenge-product-of-list", "List Product using Fold", "easy",
         "Write `product_of_list(nums: list[int]) -> int` returning product of all numbers (or 1 if empty).",
         "def product_of_list(nums: list[int]) -> int:\n    pass\n",
         "def product_of_list(nums: list[int]) -> int:\n    res = 1\n    for x in nums:\n        res *= x\n    return res\n",
         "product_of_list",
         [{"input": [[2, 3, 4]], "expected": 24, "description": "2*3*4 = 24", "is_hidden": False},
          {"input": [[]], "expected": 1, "description": "Empty list returns 1", "is_hidden": False},
          {"input": [[-1, 5, 2]], "expected": -10, "description": "With negative", "is_hidden": True}],
         ["Accumulate product starting at 1."], 70)

add_chal("chal-89", 89, 9, "challenge-parse-query-params", "URL Query Parameter Parser", "medium",
         "Write `parse_query_params(url: str) -> dict[str, str]` parsing query params after '?' into key-value pairs (or {} if none).",
         "def parse_query_params(url: str) -> dict[str, str]:\n    pass\n",
         "def parse_query_params(url: str) -> dict[str, str]:\n    if '?' not in url:\n        return {}\n    query = url.split('?', 1)[1]\n    res = {}\n    for pair in query.split('&'):\n        if '=' in pair:\n            k, v = pair.split('=', 1)\n            res[k] = v\n    return res\n",
         "parse_query_params",
         [{"input": ["https://example.com/search?q=python&lang=en"], "expected": {"q": "python", "lang": "en"}, "description": "Two params", "is_hidden": False},
          {"input": ["https://example.com/page"], "expected": {}, "description": "No params", "is_hidden": False},
          {"input": ["http://site.io/?a=1&b=2&c=3"], "expected": {"a": "1", "b": "2", "c": "3"}, "description": "Multiple params", "is_hidden": True}],
         ["Split on '?' then split on '&'.", "Split each pair on '='."], 95)

add_chal("chal-90", 90, 9, "challenge-cartesian-product", "Cartesian Product of Two Lists", "easy",
         "Write `cartesian_product(a: list, b: list) -> list[list]` returning all pairs [x, y] where x is in a and y is in b.",
         "def cartesian_product(a: list, b: list) -> list[list]:\n    pass\n",
         "def cartesian_product(a: list, b: list) -> list[list]:\n    return [[x, y] for x in a for y in b]\n",
         "cartesian_product",
         [{"input": [[1, 2], ["a", "b"]], "expected": [[1, "a"], [1, "b"], [2, "a"], [2, "b"]], "description": "2x2 product", "is_hidden": False},
          {"input": [[], [1, 2]], "expected": [], "description": "Empty first list", "is_hidden": False},
          {"input": [[1], [9]], "expected": [[1, 9]], "description": "Single pair", "is_hidden": True}],
         ["Use nested comprehension: [[x, y] for x in a for y in b]."], 80)

with open("scripts/track9.json", "w", encoding="utf-8") as f:
    json.dump(challenges, f, indent=2)
print("Track 9 generated: 10 challenges")
