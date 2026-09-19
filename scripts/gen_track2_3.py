import json

challenges = []

def add_chal(cid, idx, mod, slug, title, diff, inst, starter, sol, func, tests, hints, xp=70):
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

# --- TRACK 2: Data Structures Deep Dive (11-20) ---
add_chal("chal-11", 11, 2, "challenge-remove-duplicates", "Remove Duplicates Preserving Order", "easy",
         "Write `remove_duplicates(items: list) -> list` removing duplicates while preserving the order of first appearance.",
         "def remove_duplicates(items: list) -> list:\n    pass\n",
         "def remove_duplicates(items: list) -> list:\n    seen = set()\n    out = []\n    for x in items:\n        if x not in seen:\n            seen.add(x)\n            out.append(x)\n    return out\n",
         "remove_duplicates",
         [{"input": [[1, 2, 2, 3, 4, 3, 5]], "expected": [1, 2, 3, 4, 5], "description": "Numbers with dupes", "is_hidden": False},
          {"input": [["a", "b", "a", "c"]], "expected": ["a", "b", "c"], "description": "Strings with dupes", "is_hidden": False},
          {"input": [[1, 1, 1]], "expected": [1], "description": "All identical", "is_hidden": True}],
         ["Use a set to track seen elements.", "Append unseen to a new list."], 70)

add_chal("chal-12", 12, 2, "challenge-second-largest", "Find Second Largest Number", "easy",
         "Write `second_largest(numbers: list[int]) -> int` returning the second distinct largest number in a list of integers.",
         "def second_largest(numbers: list[int]) -> int:\n    pass\n",
         "def second_largest(numbers: list[int]) -> int:\n    unique = sorted(list(set(numbers)))\n    if len(unique) < 2:\n        return unique[0]\n    return unique[-2]\n",
         "second_largest",
         [{"input": [[10, 20, 4, 45, 99]], "expected": 45, "description": "Distinct list", "is_hidden": False},
          {"input": [[5, 5, 5, 2]], "expected": 2, "description": "Duplicates with 2nd", "is_hidden": False},
          {"input": [[-10, -5, -20]], "expected": -10, "description": "Negative numbers", "is_hidden": True}],
         ["Convert to set to get distinct values.", "Sort ascending and pick [-2]."], 70)

add_chal("chal-13", 13, 2, "challenge-swap-coordinates", "Swap Tuple Coordinates", "easy",
         "Write `swap_coordinates(point: list) -> list` taking a 2-element coordinate pair [x, y] and returning [y, x].",
         "def swap_coordinates(point: list) -> list:\n    pass\n",
         "def swap_coordinates(point: list) -> list:\n    return [point[1], point[0]]\n",
         "swap_coordinates",
         [{"input": [[10, 20]], "expected": [20, 10], "description": "Swap 10 and 20", "is_hidden": False},
          {"input": [[0, 5]], "expected": [5, 0], "description": "Swap 0 and 5", "is_hidden": False},
          {"input": [[-1, -9]], "expected": [-9, -1], "description": "Negatives", "is_hidden": True}],
         ["Access index 1 and 0.", "Return as list."], 60)

add_chal("chal-14", 14, 2, "challenge-common-elements", "Find Set Intersection", "easy",
         "Write `common_elements(a: list, b: list) -> list` returning sorted unique elements found in both lists.",
         "def common_elements(a: list, b: list) -> list:\n    pass\n",
         "def common_elements(a: list, b: list) -> list:\n    return sorted(list(set(a) & set(b)))\n",
         "common_elements",
         [{"input": [[1, 2, 3, 4], [3, 4, 5, 6]], "expected": [3, 4], "description": "Overlapping numbers", "is_hidden": False},
          {"input": [["a", "b"], ["c", "d"]], "expected": [], "description": "Disjoint sets", "is_hidden": False},
          {"input": [[10, 20, 30], [20]], "expected": [20], "description": "Single overlap", "is_hidden": True}],
         ["Use set(a) & set(b).", "Sort the result with sorted()."], 70)

add_chal("chal-15", 15, 2, "challenge-invert-dictionary", "Invert a Dictionary", "easy",
         "Write `invert_dictionary(mapping: dict) -> dict` inverting keys and values (assuming unique values).",
         "def invert_dictionary(mapping: dict) -> dict:\n    pass\n",
         "def invert_dictionary(mapping: dict) -> dict:\n    return {v: k for k, v in mapping.items()}\n",
         "invert_dictionary",
         [{"input": [{"apple": "fruit", "carrot": "vegetable"}], "expected": {"fruit": "apple", "vegetable": "carrot"}, "description": "String map", "is_hidden": False},
          {"input": [{"x": "y", "m": "n"}], "expected": {"y": "x", "n": "m"}, "description": "String characters", "is_hidden": False},
          {"input": [{"hello": "world"}], "expected": {"world": "hello"}, "description": "Single key-value", "is_hidden": True}],
         ["Use dict comprehension: {v: k for k, v in mapping.items()}."], 75)

add_chal("chal-16", 16, 2, "challenge-flatten-matrix", "Flatten 2D Matrix", "easy",
         "Write `flatten_matrix(matrix: list[list]) -> list` returning a 1D list containing all elements row by row.",
         "def flatten_matrix(matrix: list[list]) -> list:\n    pass\n",
         "def flatten_matrix(matrix: list[list]) -> list:\n    return [item for row in matrix for item in row]\n",
         "flatten_matrix",
         [{"input": [[[1, 2], [3, 4]]], "expected": [1, 2, 3, 4], "description": "2x2 matrix", "is_hidden": False},
          {"input": [[[1], [2, 3], [4, 5, 6]]], "expected": [1, 2, 3, 4, 5, 6], "description": "Ragged rows", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty matrix", "is_hidden": True}],
         ["Use nested list comprehension.", "Or loop through rows and items."], 70)

add_chal("chal-17", 17, 2, "challenge-merge-scores", "Merge Dictionaries with Sum", "easy",
         "Write `merge_scores(dict1: dict[str, int], dict2: dict[str, int]) -> dict[str, int]` summing values for overlapping keys.",
         "def merge_scores(dict1: dict, dict2: dict) -> dict:\n    pass\n",
         "def merge_scores(dict1: dict, dict2: dict) -> dict:\n    res = dict(dict1)\n    for k, v in dict2.items():\n        res[k] = res.get(k, 0) + v\n    return res\n",
         "merge_scores",
         [{"input": [{"Alice": 50, "Bob": 40}, {"Alice": 20, "Charlie": 30}], "expected": {"Alice": 70, "Bob": 40, "Charlie": 30}, "description": "Overlapping Alice", "is_hidden": False},
          {"input": [{}, {"A": 10}], "expected": {"A": 10}, "description": "Empty first dict", "is_hidden": False},
          {"input": [{"X": 1}, {"X": 2, "Y": 3}], "expected": {"X": 3, "Y": 3}, "description": "X overlapping", "is_hidden": True}],
         ["Copy dict1 into res.", "Loop through dict2 and add to res[k]."], 75)

add_chal("chal-18", 18, 2, "challenge-symmetric-diff", "Symmetric Difference", "easy",
         "Write `symmetric_diff(a: list, b: list) -> list` returning elements in either list A or list B, but not both, sorted.",
         "def symmetric_diff(a: list, b: list) -> list:\n    pass\n",
         "def symmetric_diff(a: list, b: list) -> list:\n    return sorted(list(set(a) ^ set(b)))\n",
         "symmetric_diff",
         [{"input": [[1, 2, 3], [3, 4, 5]], "expected": [1, 2, 4, 5], "description": "Overlap on 3", "is_hidden": False},
          {"input": [[1, 2], [1, 2]], "expected": [], "description": "Identical lists", "is_hidden": False},
          {"input": [[10], [20]], "expected": [10, 20], "description": "Disjoint", "is_hidden": True}],
         ["Use set(a) ^ set(b).", "Sort result with sorted()."], 70)

add_chal("chal-19", 19, 2, "challenge-chunk-list", "Chunk a List into Sublists", "easy",
         "Write `chunk_list(items: list, size: int) -> list[list]` dividing items into sublists of length `size` (last sublist may be smaller).",
         "def chunk_list(items: list, size: int) -> list[list]:\n    pass\n",
         "def chunk_list(items: list, size: int) -> list[list]:\n    return [items[i:i + size] for i in range(0, len(items), size)]\n",
         "chunk_list",
         [{"input": [[1, 2, 3, 4, 5], 2], "expected": [[1, 2], [3, 4], [5]], "description": "Chunk by 2", "is_hidden": False},
          {"input": [[1, 2, 3, 4], 2], "expected": [[1, 2], [3, 4]], "description": "Even division", "is_hidden": False},
          {"input": [[], 3], "expected": [], "description": "Empty list", "is_hidden": True}],
         ["Use range(0, len(items), size).", "Slice items[i:i+size]."], 80)

add_chal("chal-20", 20, 2, "challenge-anagram-check", "Anagram Detector", "easy",
         "Write `is_anagram(s1: str, s2: str) -> bool` returning True if s1 and s2 are anagrams (ignoring spaces and case).",
         "def is_anagram(s1: str, s2: str) -> bool:\n    pass\n",
         "def is_anagram(s1: str, s2: str) -> bool:\n    c1 = sorted([c.lower() for c in s1 if c.isalnum()])\n    c2 = sorted([c.lower() for c in s2 if c.isalnum()])\n    return c1 == c2\n",
         "is_anagram",
         [{"input": ["listen", "silent"], "expected": True, "description": "listen / silent", "is_hidden": False},
          {"input": ["hello", "world"], "expected": False, "description": "hello / world", "is_hidden": False},
          {"input": ["Dormitory", "Dirty Room"], "expected": True, "description": "Dormitory / Dirty Room", "is_hidden": True}],
         ["Strip non-alphanumeric and lowercase.", "Sort and compare lists."], 80)

# --- TRACK 3: Control Flow & Functional Python (21-30) ---
add_chal("chal-21", 21, 3, "challenge-squares-evens", "Squares of Even Numbers", "easy",
         "Write `squares_of_evens(nums: list[int]) -> list[int]` using a list comprehension returning squares of even integers.",
         "def squares_of_evens(nums: list[int]) -> list[int]:\n    pass\n",
         "def squares_of_evens(nums: list[int]) -> list[int]:\n    return [x * x for x in nums if x % 2 == 0]\n",
         "squares_of_evens",
         [{"input": [[1, 2, 3, 4, 5, 6]], "expected": [4, 16, 36], "description": "1 to 6", "is_hidden": False},
          {"input": [[1, 3, 5]], "expected": [], "description": "All odds", "is_hidden": False},
          {"input": [[0, 2]], "expected": [0, 4], "description": "0 and 2", "is_hidden": True}],
         ["Use [x * x for x in nums if x % 2 == 0]."], 75)

add_chal("chal-22", 22, 3, "challenge-char-frequencies", "Character Frequency Comprehension", "easy",
         "Write `char_frequencies(text: str) -> dict[str, int]` returning a dict of non-space character counts.",
         "def char_frequencies(text: str) -> dict[str, int]:\n    pass\n",
         "def char_frequencies(text: str) -> dict[str, int]:\n    clean = [c for c in text if c != ' ']\n    return {c: clean.count(c) for c in set(clean)}\n",
         "char_frequencies",
         [{"input": ["banana"], "expected": {"b": 1, "a": 3, "n": 2}, "description": "banana", "is_hidden": False},
          {"input": ["a b c"], "expected": {"a": 1, "b": 1, "c": 1}, "description": "spaced characters", "is_hidden": False},
          {"input": [""], "expected": {}, "description": "Empty string", "is_hidden": True}],
         ["Exclude spaces.", "Use comprehension over set(clean)."], 80)

add_chal("chal-23", 23, 3, "challenge-filter-primes", "Prime Number Filter", "medium",
         "Write `filter_primes(numbers: list[int]) -> list[int]` returning prime numbers (> 1) from the list in order.",
         "def filter_primes(numbers: list[int]) -> list[int]:\n    pass\n",
         "def filter_primes(numbers: list[int]) -> list[int]:\n    def is_p(n):\n        if n < 2:\n            return False\n        for i in range(2, int(n**0.5) + 1):\n            if n % i == 0:\n                return False\n        return True\n    return [n for n in numbers if is_p(n)]\n",
         "filter_primes",
         [{"input": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]], "expected": [2, 3, 5, 7], "description": "1 to 10", "is_hidden": False},
          {"input": [[0, 1, 4, 6]], "expected": [], "description": "No primes", "is_hidden": False},
          {"input": [[13, 17, 19]], "expected": [13, 17, 19], "description": "All primes", "is_hidden": True}],
         ["Define helper is_prime(n).", "Filter with list comprehension."], 90)

add_chal("chal-24", 24, 3, "challenge-extract-domains", "Extract Email Domains", "easy",
         "Write `extract_domains(emails: list[str]) -> list[str]` returning unique lowercase domain names sorted alphabetically.",
         "def extract_domains(emails: list[str]) -> list[str]:\n    pass\n",
         "def extract_domains(emails: list[str]) -> list[str]:\n    return sorted(list(set(e.split('@')[1].lower() for e in emails if '@' in e)))\n",
         "extract_domains",
         [{"input": [["alice@google.com", "bob@yahoo.com", "charlie@google.com"]], "expected": ["google.com", "yahoo.com"], "description": "Google & Yahoo", "is_hidden": False},
          {"input": [["user@GITHUB.COM"]], "expected": ["github.com"], "description": "Uppercase domain", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty list", "is_hidden": True}],
         ["Split on '@' and take index 1.", "Lower and deduplicate with set()."], 80)

add_chal("chal-25", 25, 3, "challenge-fibonacci-sequence", "Fibonacci Sequence Generator", "easy",
         "Write `generate_fibonacci(n: int) -> list[int]` returning the first n numbers of the Fibonacci sequence starting with [0, 1].",
         "def generate_fibonacci(n: int) -> list[int]:\n    pass\n",
         "def generate_fibonacci(n: int) -> list[int]:\n    if n <= 0:\n        return []\n    if n == 1:\n        return [0]\n    fib = [0, 1]\n    while len(fib) < n:\n        fib.append(fib[-1] + fib[-2])\n    return fib\n",
         "generate_fibonacci",
         [{"input": [5], "expected": [0, 1, 1, 2, 3], "description": "First 5 fibs", "is_hidden": False},
          {"input": [1], "expected": [0], "description": "First 1 fib", "is_hidden": False},
          {"input": [7], "expected": [0, 1, 1, 2, 3, 5, 8], "description": "First 7 fibs", "is_hidden": True}],
         ["Handle n <= 0 and n == 1.", "Append fib[-1] + fib[-2]."], 85)

add_chal("chal-26", 26, 3, "challenge-password-validator", "Password Complexity Validator", "easy",
         "Write `is_strong_password(pw: str) -> bool` returning True if pw has >= 8 chars, at least 1 uppercase, 1 lowercase, and 1 digit.",
         "def is_strong_password(pw: str) -> bool:\n    pass\n",
         "def is_strong_password(pw: str) -> bool:\n    if len(pw) < 8:\n        return False\n    has_upper = any(c.isupper() for c in pw)\n    has_lower = any(c.islower() for c in pw)\n    has_digit = any(c.isdigit() for c in pw)\n    return has_upper and has_lower and has_digit\n",
         "is_strong_password",
         [{"input": ["SecurePass1"], "expected": True, "description": "Valid password", "is_hidden": False},
          {"input": ["weakpass"], "expected": False, "description": "No uppercase or digit", "is_hidden": False},
          {"input": ["Short1A"], "expected": False, "description": "Too short (< 8)", "is_hidden": True}],
         ["Use any() with isupper(), islower(), isdigit().", "Check len(pw) >= 8."], 80)

add_chal("chal-27", 27, 3, "challenge-rank-items", "Pair Ranking with Enumerate", "easy",
         "Write `rank_items(items: list[str]) -> list[str]` returning strings formatted as '1. <item>', '2. <item>', etc.",
         "def rank_items(items: list[str]) -> list[str]:\n    pass\n",
         "def rank_items(items: list[str]) -> list[str]:\n    return [f'{i}. {item}' for i, item in enumerate(items, start=1)]\n",
         "rank_items",
         [{"input": [["Gold", "Silver", "Bronze"]], "expected": ["1. Gold", "2. Silver", "3. Bronze"], "description": "Medals rank", "is_hidden": False},
          {"input": [["Solo"]], "expected": ["1. Solo"], "description": "Single item", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty list", "is_hidden": True}],
         ["Use enumerate(items, start=1).", "Format as f'{i}. {item}'."], 75)

add_chal("chal-28", 28, 3, "challenge-add-all", "Variadic Multi-Adder", "easy",
         "Write `add_all(nums: list[int]) -> int` returning the sum of all integers in the list (or 0 if empty).",
         "def add_all(nums: list[int]) -> int:\n    pass\n",
         "def add_all(nums: list[int]) -> int:\n    return sum(nums)\n",
         "add_all",
         [{"input": [[1, 2, 3, 4]], "expected": 10, "description": "1+2+3+4 = 10", "is_hidden": False},
          {"input": [[]], "expected": 0, "description": "Empty list returns 0", "is_hidden": False},
          {"input": [[-5, 5, 10]], "expected": 10, "description": "Negatives and positives", "is_hidden": True}],
         ["Use sum()."], 65)

add_chal("chal-29", 29, 3, "challenge-sort-by-length", "Sort by String Length", "easy",
         "Write `sort_by_length(words: list[str]) -> list[str]` sorting words by length ascending. Break ties alphabetically.",
         "def sort_by_length(words: list[str]) -> list[str]:\n    pass\n",
         "def sort_by_length(words: list[str]) -> list[str]:\n    return sorted(words, key=lambda w: (len(w), w))\n",
         "sort_by_length",
         [{"input": [["apple", "pie", "banana", "kiwi"]], "expected": ["pie", "kiwi", "apple", "banana"], "description": "Lengths 3, 4, 5, 6", "is_hidden": False},
          {"input": [["bat", "ant", "cat"]], "expected": ["ant", "bat", "cat"], "description": "Equal length tie-breaking", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty list", "is_hidden": True}],
         ["Use sorted(words, key=lambda w: (len(w), w))."], 85)

add_chal("chal-30", 30, 3, "challenge-transpose-matrix", "Transpose Matrix", "medium",
         "Write `transpose_matrix(matrix: list[list[int]]) -> list[list[int]]` swapping rows and columns of a matrix.",
         "def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:\n    pass\n",
         "def transpose_matrix(matrix: list[list[int]]) -> list[list[int]]:\n    if not matrix or not matrix[0]:\n        return []\n    return [[matrix[r][c] for r in range(len(matrix))] for c in range(len(matrix[0]))]\n",
         "transpose_matrix",
         [{"input": [[[1, 2], [3, 4], [5, 6]]], "expected": [[1, 3, 5], [2, 4, 6]], "description": "3x2 to 2x3", "is_hidden": False},
          {"input": [[[1, 2], [3, 4]]], "expected": [[1, 3], [2, 4]], "description": "2x2 square", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty matrix", "is_hidden": True}],
         ["Use nested comprehension with row and col indices.", "Or use list(map(list, zip(*matrix)))."], 90)

with open("scripts/track2_3.json", "w", encoding="utf-8") as f:
    json.dump(challenges, f, indent=2)
print("Track 2 & 3 generated: 20 challenges")
