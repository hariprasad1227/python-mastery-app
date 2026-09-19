import os
import sys
import json

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runner.runner import execute_learner_code

all_challenges = []

def add_chal(cid, idx, mod, slug, title, diff, inst, starter, sol, func, tests, hints, xp=50):
    all_challenges.append({
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

# --- TRACK 1: Python Fundamentals (1-10) ---
add_chal("chal-1", 1, 1, "challenge-greet", "Personalized Greeting", "easy",
         "Write `greet(name: str) -> str` returning 'Hello, <name>!'",
         "def greet(name: str) -> str:\n    pass\n",
         "def greet(name: str) -> str:\n    return f'Hello, {name}!'\n",
         "greet",
         [{"input": ["Alice"], "expected": "Hello, Alice!", "description": "Greeting Alice", "is_hidden": False},
          {"input": ["Bob"], "expected": "Hello, Bob!", "description": "Greeting Bob", "is_hidden": False},
          {"input": ["Pythonista"], "expected": "Hello, Pythonista!", "description": "Greeting Pythonista", "is_hidden": True}],
         ["Use f-string.", "Remember return keyword."], 50)

add_chal("chal-2", 2, 1, "challenge-even-or-odd", "Even or Odd Parity", "easy",
         "Write `check_parity(n: int) -> str` returning 'Even' or 'Odd'.",
         "def check_parity(n: int) -> str:\n    pass\n",
         "def check_parity(n: int) -> str:\n    return 'Even' if n % 2 == 0 else 'Odd'\n",
         "check_parity",
         [{"input": [4], "expected": "Even", "description": "4 is Even", "is_hidden": False},
          {"input": [7], "expected": "Odd", "description": "7 is Odd", "is_hidden": False},
          {"input": [0], "expected": "Even", "description": "0 is Even", "is_hidden": True}],
         ["Use % operator.", "Check n % 2 == 0."], 60)

add_chal("chal-3", 3, 1, "challenge-sum-multiples", "Sum of Multiples", "easy",
         "Write `sum_multiples(limit: int, factor: int) -> int` summing integers <= limit divisible by factor.",
         "def sum_multiples(limit: int, factor: int) -> int:\n    pass\n",
         "def sum_multiples(limit: int, factor: int) -> int:\n    return sum(i for i in range(factor, limit + 1, factor))\n",
         "sum_multiples",
         [{"input": [10, 3], "expected": 18, "description": "Multiples of 3 <= 10: 3+6+9 = 18", "is_hidden": False},
          {"input": [20, 5], "expected": 50, "description": "Multiples of 5 <= 20: 5+10+15+20 = 50", "is_hidden": False},
          {"input": [5, 7], "expected": 0, "description": "No multiples up to 5", "is_hidden": True}],
         ["Use range with step = factor.", "Sum the values."], 75)

add_chal("chal-4", 4, 1, "challenge-palindrome", "Palindrome Checker", "easy",
         "Write `is_palindrome(text: str) -> bool` returning True if text is a palindrome (ignoring case & non-alphanumerics).",
         "def is_palindrome(text: str) -> bool:\n    pass\n",
         "def is_palindrome(text: str) -> bool:\n    c = ''.join(ch.lower() for ch in text if ch.isalnum())\n    return c == c[::-1]\n",
         "is_palindrome",
         [{"input": ["racecar"], "expected": True, "description": "racecar", "is_hidden": False},
          {"input": ["hello"], "expected": False, "description": "hello", "is_hidden": False},
          {"input": ["A man, a plan, a canal: Panama"], "expected": True, "description": "Panama sentence", "is_hidden": True}],
         ["Clean string with isalnum().", "Compare with slice [::-1]."], 80)

add_chal("chal-5", 5, 1, "challenge-word-frequency", "Word Frequency Counter", "easy",
         "Write `count_frequencies(words: list[str]) -> dict[str, int]` counting frequency of each word.",
         "def count_frequencies(words: list[str]) -> dict[str, int]:\n    pass\n",
         "def count_frequencies(words: list[str]) -> dict[str, int]:\n    f = {}\n    for w in words:\n        f[w] = f.get(w, 0) + 1\n    return f\n",
         "count_frequencies",
         [{"input": [["apple", "banana", "apple"]], "expected": {"apple": 2, "banana": 1}, "description": "Word frequencies", "is_hidden": False},
          {"input": [["cat", "dog", "cat", "bird"]], "expected": {"cat": 2, "dog": 1, "bird": 1}, "description": "Animals list", "is_hidden": False},
          {"input": [[]], "expected": {}, "description": "Empty list", "is_hidden": True}],
         ["Initialize dict.", "Use dict.get(w, 0) + 1."], 85)

add_chal("chal-6", 6, 1, "challenge-title-case", "Sentence Title Casing", "easy",
         "Write `to_title_case(sentence: str) -> str` capitalizing the first letter of each word separated by spaces.",
         "def to_title_case(sentence: str) -> str:\n    pass\n",
         "def to_title_case(sentence: str) -> str:\n    return ' '.join(word.capitalize() for word in sentence.split(' '))\n",
         "to_title_case",
         [{"input": ["hello world"], "expected": "Hello World", "description": "hello world", "is_hidden": False},
          {"input": ["python programming is fun"], "expected": "Python Programming Is Fun", "description": "Multiple words", "is_hidden": False},
          {"input": ["quick brown fox"], "expected": "Quick Brown Fox", "description": "Fox test", "is_hidden": True}],
         ["Use sentence.split(' ').", "Capitalize each word with .capitalize()."], 60)

add_chal("chal-7", 7, 1, "challenge-factorial", "Factorial Calculator", "easy",
         "Write `factorial(n: int) -> int` returning the factorial of n (where 0! = 1).",
         "def factorial(n: int) -> int:\n    pass\n",
         "def factorial(n: int) -> int:\n    res = 1\n    for i in range(2, n + 1):\n        res *= i\n    return res\n",
         "factorial",
         [{"input": [5], "expected": 120, "description": "5! = 120", "is_hidden": False},
          {"input": [0], "expected": 1, "description": "0! = 1", "is_hidden": False},
          {"input": [6], "expected": 720, "description": "6! = 720", "is_hidden": True}],
         ["Start with res = 1.", "Loop from 2 to n."], 65)

add_chal("chal-8", 8, 1, "challenge-reverse-list", "Reverse a List", "easy",
         "Write `reverse_list(items: list) -> list` returning a new list with items in reversed order without using .reverse().",
         "def reverse_list(items: list) -> list:\n    pass\n",
         "def reverse_list(items: list) -> list:\n    return items[::-1]\n",
         "reverse_list",
         [{"input": [[1, 2, 3, 4]], "expected": [4, 3, 2, 1], "description": "1 to 4", "is_hidden": False},
          {"input": [["a", "b", "c"]], "expected": ["c", "b", "a"], "description": "Strings", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty list", "is_hidden": True}],
         ["Use list slicing [::-1]."], 60)

add_chal("chal-9", 9, 1, "challenge-leap-year", "Leap Year Validator", "easy",
         "Write `is_leap_year(year: int) -> bool` returning True if year is a leap year (divisible by 4, except century years unless divisible by 400).",
         "def is_leap_year(year: int) -> bool:\n    pass\n",
         "def is_leap_year(year: int) -> bool:\n    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)\n",
         "is_leap_year",
         [{"input": [2024], "expected": True, "description": "2024 is leap", "is_hidden": False},
          {"input": [1900], "expected": False, "description": "1900 is century non-leap", "is_hidden": False},
          {"input": [2000], "expected": True, "description": "2000 is 400-year leap", "is_hidden": True}],
         ["Check year % 400 == 0 first.", "Check year % 4 == 0 and year % 100 != 0."], 70)

add_chal("chal-10", 10, 1, "challenge-celsius-to-fahrenheit", "Temperature Converter", "easy",
         "Write `celsius_to_fahrenheit(c: float) -> float` converting Celsius to Fahrenheit (F = C * 9/5 + 32) rounded to 1 decimal place.",
         "def celsius_to_fahrenheit(c: float) -> float:\n    pass\n",
         "def celsius_to_fahrenheit(c: float) -> float:\n    return round(c * 9.0 / 5.0 + 32.0, 1)\n",
         "celsius_to_fahrenheit",
         [{"input": [0.0], "expected": 32.0, "description": "0C = 32F", "is_hidden": False},
          {"input": [100.0], "expected": 212.0, "description": "100C = 212F", "is_hidden": False},
          {"input": [37.0], "expected": 98.6, "description": "37C body temp", "is_hidden": True}],
         ["Use formula (c * 9/5) + 32.", "Use round(..., 1)."], 60)

with open("scripts/track1.json", "w", encoding="utf-8") as f:
    json.dump(all_challenges, f, indent=2)
print("Track 1 generated: 10 challenges")
