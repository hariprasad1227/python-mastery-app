"""
Python Mastery - Comprehensive Educational Content & Lessons Engine
Provides in-depth conceptual tutorials, syntax guides, code examples,
and common pitfalls for all 10 Tracks and 100 Challenges.
"""

from typing import Dict, Any, List

TRACK_MASTER_LESSONS: Dict[int, Dict[str, Any]] = {
    1: {
        "track_number": 1,
        "title": "Python Fundamentals & Syntax",
        "subtitle": "Variables, Expressions, Primitive Types & String Formatting",
        "reading_time_minutes": 10,
        "overview": "Python is a dynamically typed, high-level programming language designed for readability. In this foundational track, you will master variable binding, scalar data types (int, float, bool, str), string operations, mathematical operators, and defining functions that return results.",
        "core_concepts": [
            {
                "name": "1. Variables & Dynamic Typing",
                "explanation": "In Python, variables are labels attached to objects in memory. You do not need to declare types explicitly. For example, `x = 42` creates an integer, and `x = 'hello'` reassigns the label to a string.",
                "example_code": "# Variable assignment and type inspection\nx = 10          # Integer\ny = 3.14        # Float\nis_valid = True # Boolean\nname = \"Antigravity\" # String\n\nprint(type(x))  # <class 'int'>\nprint(type(y))  # <class 'float'>\n"
            },
            {
                "name": "2. Functions & The Return Keyword",
                "explanation": "Functions encapsulate reusable logic. They are defined using the `def` keyword. Every function should explicitly `return` its result. If you omit `return`, Python implicitly returns `None`.",
                "example_code": "def calculate_total(price: float, tax_rate: float = 0.05) -> float:\n    \"\"\"Calculates total price including tax.\"\"\"\n    total = price + (price * tax_rate)\n    return round(total, 2)\n\nresult = calculate_total(100.0, 0.08) # Returns 108.0\n"
            },
            {
                "name": "3. String Manipulation & Modern F-Strings",
                "explanation": "Strings are immutable sequences of Unicode characters. Python 3.6+ introduces formatted string literals (f-strings) using `f'Hello, {variable}!'`, which evaluate expressions at runtime efficiently.",
                "example_code": "user = \"DeepMind\"\nxp = 500\n# Clean f-string interpolation\nmessage = f\"Welcome back, {user}! Current XP: {xp:,}\"\n\n# String methods: upper, lower, strip, split\nraw = \"  python rocks  \"\ncleaned = raw.strip().title() # 'Python Rocks'\n"
            },
            {
                "name": "4. Arithmetic & Parity Operations",
                "explanation": "Python supports standard arithmetic: `+`, `-`, `*`, `/` (float division), `//` (integer floor division), `%` (modulo/remainder), and `**` (exponentiation). The modulo operator `% 2 == 0` is the standard way to check if a number is even.",
                "example_code": "def check_parity(n: int) -> str:\n    return \"Even\" if n % 2 == 0 else \"Odd\"\n\n# Integer floor division vs true division\nprint(7 / 2)  # 3.5 (float)\nprint(7 // 2) # 3 (int floor)\nprint(7 % 2)  # 1 (remainder)\n"
            }
        ],
        "common_pitfalls": [
            "Forgetting `return`: Using `print()` instead of `return` in challenge functions will cause tests to fail with `None != expected`.",
            "String Immutability: You cannot modify a string in place (`s[0] = 'a'` raises a TypeError). Always create a new string.",
            "Zero Division: Always ensure divisor is not zero before calculating `a / b` or `a % b`."
        ]
    },
    2: {
        "track_number": 2,
        "title": "Data Structures Deep Dive",
        "subtitle": "Lists, Tuples, Dictionaries, Sets & Matrix Operations",
        "reading_time_minutes": 12,
        "overview": "Data structures organize and store data for efficient access and modification. Python provides four primary built-in collection types: mutable ordered Lists, immutable ordered Tuples, unique unordered Sets, and key-value Dictionaries.",
        "core_concepts": [
            {
                "name": "1. Lists: Ordered & Mutable Sequences",
                "explanation": "Lists allow indexed access (`list[0]`), negative indexing (`list[-1]`), slicing (`list[start:end:step]`), and dynamic resizing via `.append()`, `.extend()`, and `.pop()`.",
                "example_code": "numbers = [1, 2, 3, 4, 5]\nnumbers.append(6)\n\n# Slicing: [start:stop:step]\nreversed_copy = numbers[::-1] # [6, 5, 4, 3, 2, 1]\nsub_chunk = numbers[1:4]       # [2, 3, 4]\n"
            },
            {
                "name": "2. Dictionaries: O(1) Hash Map Key-Value Lookups",
                "explanation": "Dictionaries store key-value mappings using hash tables, giving average O(1) time complexity for insertion, retrieval, and deletion. Keys must be immutable (e.g. str, int, tuple).",
                "example_code": "counts = {}\nwords = [\"apple\", \"banana\", \"apple\"]\nfor w in words:\n    counts[w] = counts.get(w, 0) + 1\n\n# Inverting a dictionary\ninverted = {v: k for k, v in counts.items()}\n"
            },
            {
                "name": "3. Sets: Uniqueness & Mathematical Set Operations",
                "explanation": "Sets only store distinct elements with O(1) membership testing (`x in my_set`). They support mathematical union (`|`), intersection (`&`), difference (`-`), and symmetric difference (`^`).",
                "example_code": "team_a = {\"alice\", \"bob\", \"charlie\"}\nteam_b = {\"bob\", \"david\", \"alice\"}\n\ncommon = team_a & team_b        # {'alice', 'bob'}\nall_members = team_a | team_b   # {'alice', 'bob', 'charlie', 'david'}\nunique_to_a = team_a - team_b   # {'charlie'}\n"
            },
            {
                "name": "4. 2D Matrices & Nested Collections",
                "explanation": "A 2D matrix is represented as a list of lists: `[[1, 2], [3, 4]]`. Flattening or transposing matrices can be achieved using nested loops or list comprehensions.",
                "example_code": "matrix = [\n    [1, 2, 3],\n    [4, 5, 6]\n]\n# Flatten to [1, 2, 3, 4, 5, 6]\nflattened = [val for row in matrix for val in row]\n"
            }
        ],
        "common_pitfalls": [
            "Modifying a list while iterating over it: This causes skipped elements or unexpected behavior. Iterate over a copy or use list comprehension.",
            "Mutable default arguments: `def add_item(item, lst=[])` shares the same list across all calls! Always use `lst=None` and initialize inside.",
            "Dictionary keys must be hashable: Lists and dicts cannot be dictionary keys because they are mutable."
        ]
    },
    3: {
        "track_number": 3,
        "title": "Control Flow & Functional Python",
        "subtitle": "Comprehensions, Generators, Lambda Functions & Filtering",
        "reading_time_minutes": 12,
        "overview": "Idiomatic Python (Pythonic code) leverages expressive comprehension expressions and generator iterators instead of verbose imperative boilerplate loops.",
        "core_concepts": [
            {
                "name": "1. List & Dictionary Comprehensions",
                "explanation": "Comprehensions provide a concise syntax for transforming and filtering iterables: `[expr for item in iterable if condition]`.",
                "example_code": "numbers = range(10)\n# Squares of even numbers only\neven_squares = [x**2 for x in numbers if x % 2 == 0]\n\n# Dictionary comprehension: word -> length\nwords = [\"python\", \"fastapi\", \"react\"]\nlengths = {w: len(w) for w in words}\n"
            },
            {
                "name": "2. Generators & The Yield Keyword",
                "explanation": "Generators produce items on demand (lazy evaluation) without keeping the entire sequence in memory. This enables processing gigabyte-scale streams in O(1) space.",
                "example_code": "def fibonacci_generator(n: int):\n    a, b = 0, 1\n    for _ in range(n):\n        yield a\n        a, b = b, a + b\n\nfor num in fibonacci_generator(5):\n    print(num) # 0, 1, 1, 2, 3\n"
            },
            {
                "name": "3. Lambdas & Custom Sort Keys",
                "explanation": "Lambda functions are small anonymous single-expression functions: `lambda x: expression`. They are frequently used as sorting keys or mapping callbacks.",
                "example_code": "items = [(\"Alice\", 88), (\"Bob\", 95), (\"Charlie\", 72)]\n# Sort by score descending\nitems.sort(key=lambda pair: pair[1], reverse=True)\n"
            }
        ],
        "common_pitfalls": [
            "Overly complex comprehensions: If a comprehension has multiple nested for-loops and ifs, write a standard function with clear loops for readability.",
            "Exhausting generators: Generators can only be consumed once. If you need to iterate over the items multiple times, convert to a `list()`."
        ]
    },
    4: {
        "track_number": 4,
        "title": "Functions, Closures & Recursion",
        "subtitle": "Default Parameters, Recursive Call Stacks & Memoization",
        "reading_time_minutes": 15,
        "overview": "Functions in Python are first-class citizens: they can be passed as arguments, returned from other functions, and store enclosing scope variables (closures).",
        "core_concepts": [
            {
                "name": "1. Recursion: Base Case & Recursive Step",
                "explanation": "A recursive function calls itself to solve smaller subproblems. Every recursive function MUST have at least one base case that terminates without recursion to prevent `RecursionError: maximum recursion depth exceeded`.",
                "example_code": "def factorial(n: int) -> int:\n    if n <= 1:  # Base case\n        return 1\n    return n * factorial(n - 1)  # Recursive step\n"
            },
            {
                "name": "2. Closures & Function Factories",
                "explanation": "A closure occurs when an inner function retains access to variables from its enclosing outer function even after the outer function has finished executing.",
                "example_code": "def make_multiplier(factor: int):\n    def multiplier(n: int) -> int:\n        return n * factor\n    return multiplier\n\ndouble = make_multiplier(2)\ntriple = make_multiplier(3)\nprint(double(5)) # 10\nprint(triple(5)) # 15\n"
            },
            {
                "name": "3. Memoization (Caching Recursive Calls)",
                "explanation": "Naive recursive algorithms (like Fibonacci O(2^n)) duplicate calculations exponentially. Memoization stores previous computation results in a dictionary, reducing runtime to O(n).",
                "example_code": "memo = {}\ndef fib(n: int) -> int:\n    if n in (0, 1):\n        return n\n    if n not in memo:\n        memo[n] = fib(n - 1) + fib(n - 2)\n    return memo[n]\n"
            }
        ],
        "common_pitfalls": [
            "Missing base case: Omitting the base case in recursion causes infinite recursion until the call stack blows up.",
            "Python default recursion limit: Python limits recursion depth to ~1000 frames to prevent C-level stack overflow."
        ]
    },
    5: {
        "track_number": 5,
        "title": "Object-Oriented Programming (OOP)",
        "subtitle": "Classes, Inheritance, Dunder Methods & Polymorphism",
        "reading_time_minutes": 15,
        "overview": "OOP models real-world entities through classes that encapsulate state (attributes) and behavior (methods). Python supports single and multiple inheritance, method overriding, and rich operator overloading through special 'dunder' (double-underscore) methods.",
        "core_concepts": [
            {
                "name": "1. Classes, Attributes, and `self`",
                "explanation": "The `__init__` constructor initializes instance attributes. The first parameter of every instance method is `self`, which refers to the current instance of the class.",
                "example_code": "class BankAccount:\n    def __init__(self, owner: str, initial_balance: float = 0.0):\n        self.owner = owner\n        self.balance = initial_balance\n\n    def deposit(self, amount: float) -> float:\n        if amount <= 0:\n            raise ValueError(\"Deposit must be positive\")\n        self.balance += amount\n        return self.balance\n"
            },
            {
                "name": "2. Dunder Magic Methods",
                "explanation": "Dunders let user-defined classes interact with Python syntax: `__str__` (readable representation), `__repr__` (debugging), `__len__` (`len(obj)`), `__add__` (`obj1 + obj2`), and `__eq__` (`obj1 == obj2`).",
                "example_code": "class Vector:\n    def __init__(self, x: int, y: int):\n        self.x, self.y = x, y\n\n    def __repr__(self):\n        return f\"Vector({self.x}, {self.y})\"\n\n    def __add__(self, other):\n        return Vector(self.x + other.x, self.y + other.y)\n\nv1 = Vector(2, 3)\nv2 = Vector(5, 7)\nprint(v1 + v2) # Vector(7, 10)\n"
            },
            {
                "name": "3. Inheritance & `super()`",
                "explanation": "A child class inherits all attributes and methods from its parent. `super().__init__(...)` allows invoking the parent constructor cleanly.",
                "example_code": "class Animal:\n    def __init__(self, name: str):\n        self.name = name\n    def speak(self) -> str:\n        return \"...\"\n\nclass Dog(Animal):\n    def speak(self) -> str:\n        return f\"{self.name} says Woof!\"\n"
            }
        ],
        "common_pitfalls": [
            "Forgetting `self` as the first argument in method definitions.",
            "Class attributes vs Instance attributes: Defining an attribute directly under the class shares it among ALL instances!"
        ]
    },
    6: {
        "track_number": 6,
        "title": "Error Handling & Defensive Coding",
        "subtitle": "Try-Except-Finally, Specific Exceptions & Validation",
        "reading_time_minutes": 10,
        "overview": "Production Python follows the EAFP principle: 'Easier to Ask for Forgiveness than Permission'. Exception handling prevents abrupt crashes and allows systems to recover gracefully.",
        "core_concepts": [
            {
                "name": "1. The Try-Except-Else-Finally Structure",
                "explanation": "Exceptions are intercepted with `try ... except`. The optional `else` block runs only if no exception was raised, and `finally` runs unconditionally (e.g. for cleanup).",
                "example_code": "def safe_divide(a: float, b: float):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return None\n"
            },
            {
                "name": "2. Specific Exception Catching",
                "explanation": "Never write bare `except:`. Always catch specific exceptions (`KeyError`, `IndexError`, `ValueError`) to avoid masking critical bugs like `KeyboardInterrupt` or syntax errors.",
                "example_code": "def parse_int(text: str, default: int = 0) -> int:\n    try:\n        return int(text)\n    except (ValueError, TypeError):\n        return default\n"
            }
        ],
        "common_pitfalls": [
            "Catching `Exception` blindly: Catches bugs that should fail loudly during development.",
            "Silent failures: Swallowing exceptions without logging or returning an informative signal."
        ]
    },
    7: {
        "track_number": 7,
        "title": "Algorithms & Problem Solving",
        "subtitle": "Two Pointers, Binary Search, Sliding Window & Stacks",
        "reading_time_minutes": 15,
        "overview": "Master foundational algorithmic patterns that enable optimal time and space complexities: Two Pointers for sorted arrays, Binary Search for O(log n) lookups, Sliding Window for continuous subarrays, and Kadane's algorithm for maximum subarray sums.",
        "core_concepts": [
            {
                "name": "1. Two-Pointer Technique",
                "explanation": "Using two indices converging from opposite ends of a sorted array reduces O(n^2) brute force searches to O(n) linear scans.",
                "example_code": "def two_sum_sorted(nums: list[int], target: int) -> list[int]:\n    left, right = 0, len(nums) - 1\n    while left < right:\n        curr = nums[left] + nums[right]\n        if curr == target:\n            return [left, right]\n        elif curr < target:\n            left += 1\n        else:\n            right -= 1\n    return []\n"
            },
            {
                "name": "2. Binary Search: O(log n)",
                "explanation": "Divide-and-conquer on sorted sequences. Repeatedly halves the search space by inspecting the middle element.",
                "example_code": "def binary_search(nums: list[int], target: int) -> int:\n    low, high = 0, len(nums) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n"
            }
        ],
        "common_pitfalls": [
            "Off-by-one errors in binary search bounds (`low <= high` vs `low < high`).",
            "Integer overflow in other languages: Python natively handles arbitrarily large integers, but `mid = (low + high) // 2` is still standard."
        ]
    },
    8: {
        "track_number": 8,
        "title": "Text Processing & String Manipulation",
        "subtitle": "Regex Patterns, Encoding, Tokenization & Formatting",
        "reading_time_minutes": 10,
        "overview": "Real-world data is predominantly textual. Learn to normalize whitespace, perform ASCII-based cipher translations, sanitize inputs, mask sensitive data, and split/join complex tokens.",
        "core_concepts": [
            {
                "name": "1. ASCII Codes & Character Translation",
                "explanation": "`ord(char)` gives the integer ASCII/Unicode code point, and `chr(code)` converts an integer back to its character. This is fundamental for ciphers and hashing.",
                "example_code": "# Character shifting\ndef shift_char(c: str, shift: int = 1) -> str:\n    if c.isalpha():\n        base = ord('A') if c.isupper() else ord('a')\n        return chr((ord(c) - base + shift) % 26 + base)\n    return c\n"
            },
            {
                "name": "2. Tokenization & Delimiter Splitting",
                "explanation": "`.split()`, `.join()`, and regex tokenizers transform raw unstructured text into structured analytical units.",
                "example_code": "raw = \"python,fastapi,   react , postgres\"\ntags = [t.strip() for t in raw.split(\",\")]\nclean_csv = \", \".join(tags)\n"
            }
        ],
        "common_pitfalls": [
            "Using `+` concatenation in large loops: Creates O(n^2) intermediate string objects. Use `\"\".join(list_of_strings)` instead for O(n) performance."
        ]
    },
    9: {
        "track_number": 9,
        "title": "Python Standard Library Mastery",
        "subtitle": "Collections, Itertools, Heapq, Math & Datetime",
        "reading_time_minutes": 15,
        "overview": "Python comes with 'batteries included'. Don't reinvent the wheel: `collections.defaultdict`, `Counter`, `deque`, `heapq`, and `itertools` offer battle-tested C-speed implementations.",
        "core_concepts": [
            {
                "name": "1. Collections: Defaultdict, Counter, Deque",
                "explanation": "`defaultdict` automatically initializes missing keys; `Counter` tallies elements; `deque` provides O(1) double-ended queue pushes and pops.",
                "example_code": "from collections import Counter, deque\n\n# Frequency tally in O(n)\ncounts = Counter([\"a\", \"b\", \"a\", \"c\", \"a\"])\nprint(counts.most_common(1)) # [('a', 3)]\n\n# Double-ended queue\nq = deque([1, 2, 3])\nq.appendleft(0) # O(1)\nq.pop()         # O(1)\n"
            },
            {
                "name": "2. Heapq: Priority Queues in O(log n)",
                "explanation": "`heapq` provides min-heap operations over standard lists, allowing retrieval of the smallest/largest elements efficiently.",
                "example_code": "import heapq\n\nnums = [10, 2, 5, 1, 8]\nheapq.heapify(nums)\nsmallest = heapq.heappop(nums) # 1\n"
            }
        ],
        "common_pitfalls": [
            "Using `list.pop(0)` for a queue: `list.pop(0)` takes O(n) time because all elements must shift. Always use `collections.deque.popleft()` for O(1)."
        ]
    },
    10: {
        "track_number": 10,
        "title": "Advanced Mastery & System Capstones",
        "subtitle": "Trie Prefix Search, LRU Caches, State Machines & Rate Limiters",
        "reading_time_minutes": 15,
        "overview": "Synthesize all language features to build production-grade architectural components: Trie trees for autocomplete, LRU caches combining hash maps and linked structures, finite state machines, and sliding-window rate limiters.",
        "core_concepts": [
            {
                "name": "1. Prefix Tree (Trie)",
                "explanation": "A tree data structure where nodes represent characters, providing O(k) prefix matching and autocomplete search regardless of dictionary size.",
                "example_code": "class TrieNode:\n    def __init__(self):\n        self.children = {}\n        self.is_end = False\n\nclass Trie:\n    def __init__(self):\n        self.root = TrieNode()\n\n    def insert(self, word: str):\n        curr = self.root\n        for ch in word:\n            if ch not in curr.children:\n                curr.children[ch] = TrieNode()\n            curr = curr.children[ch]\n        curr.is_end = True\n"
            },
            {
                "name": "2. Least Recently Used (LRU) Cache",
                "explanation": "Combines a hash table for O(1) lookups with an ordered sequence (like `collections.OrderedDict`) to evict the oldest accessed items when capacity is exceeded.",
                "example_code": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity: int):\n        self.cap = capacity\n        self.cache = OrderedDict()\n\n    def get(self, key: int) -> int:\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n"
            }
        ],
        "common_pitfalls": [
            "Memory leaks in caches: Forgetting to evict stale entries causes process memory to grow indefinitely.",
            "State machine race conditions: Always transition states cleanly using defined event handlers."
        ]
    }
}


def get_lesson_for_challenge(challenge_id: str, title: str, level_number: int) -> Dict[str, Any]:
    """
    Returns a challenge-tailored lesson containing concept explanation,
    syntax guide, and practical code examples.
    """
    track_lesson = TRACK_MASTER_LESSONS.get(level_number, TRACK_MASTER_LESSONS[1])
    
    return {
        "track_number": level_number,
        "track_title": track_lesson["title"],
        "concept_headline": f"Concept Guide: {title}",
        "theory_overview": track_lesson["overview"],
        "core_concepts": track_lesson["core_concepts"],
        "common_pitfalls": track_lesson["common_pitfalls"]
    }


def get_all_track_lessons() -> List[Dict[str, Any]]:
    """Returns the full collection of all 10 Track Master Tutorials."""
    return [TRACK_MASTER_LESSONS[k] for k in sorted(TRACK_MASTER_LESSONS.keys())]
