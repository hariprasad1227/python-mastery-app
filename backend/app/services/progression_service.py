"""
Python Mastery - Progression Engine Service
Manages strict task locks, XP bonuses, level calculations, streak tracking, and badges.
"""

from typing import List, Dict, Any, Optional
from datetime import date, timedelta
from backend.app.schemas.progression import UserProfile, ModuleItem, ChallengeSummary, BadgeItem

# Seed Curriculum Cache
CURRICULUM_DATA: List[Dict[str, Any]] = [
    {
        "id": "mod-1",
        "slug": "level-1-basics",
        "title": "Level 1: Python Fundamentals",
        "description": "Variables, strings, expressions, and print statements.",
        "level_number": 1,
        "order_index": 1,
        "challenges": [
            {
                "id": "chal-1",
                "slug": "challenge-greet",
                "title": "Personalized Greeting",
                "instructions": "Write a function `greet(name: str) -> str` that returns 'Hello, <name>!'",
                "starter_code": "def greet(name: str) -> str:\n    # Return greeting string\n    pass\n",
                "entry_function_name": "greet",
                "xp_reward": 50,
                "hints": [
                    "Remember to use the `return` keyword instead of `print()`.",
                    "Use an f-string: `f'Hello, {name}!'`."
                ],
                "test_cases": [
                    {"input": ["Alice"], "expected": "Hello, Alice!", "description": "Greeting Alice", "is_hidden": False},
                    {"input": ["Bob"], "expected": "Hello, Bob!", "description": "Greeting Bob", "is_hidden": False},
                    {"input": ["Pythonista"], "expected": "Hello, Pythonista!", "description": "Greeting Pythonista", "is_hidden": True}
                ]
            }
        ]
    },
    {
        "id": "mod-2",
        "slug": "level-2-control-flow",
        "title": "Level 2: Decision Making",
        "description": "If-elif-else statements, boolean logic, and comparison.",
        "level_number": 2,
        "order_index": 2,
        "challenges": [
            {
                "id": "chal-2",
                "slug": "challenge-even-or-odd",
                "title": "Even or Odd Parity",
                "instructions": "Write a function `check_parity(n: int) -> str` that returns 'Even' if n is even, and 'Odd' otherwise.",
                "starter_code": "def check_parity(n: int) -> str:\n    # Return 'Even' or 'Odd'\n    pass\n",
                "entry_function_name": "check_parity",
                "xp_reward": 60,
                "hints": [
                    "Use the modulo operator `%`.",
                    "If `n % 2 == 0`, it's even."
                ],
                "test_cases": [
                    {"input": [4], "expected": "Even", "description": "4 is Even", "is_hidden": False},
                    {"input": [7], "expected": "Odd", "description": "7 is Odd", "is_hidden": False},
                    {"input": [0], "expected": "Even", "description": "0 is Even", "is_hidden": True}
                ]
            }
        ]
    },
    {
        "id": "mod-3",
        "slug": "level-3-loops",
        "title": "Level 3: Loops & Iteration",
        "description": "For loops, while loops, ranges, and accumulation.",
        "level_number": 3,
        "order_index": 3,
        "challenges": [
            {
                "id": "chal-3",
                "slug": "challenge-sum-multiples",
                "title": "Sum of Multiples",
                "instructions": "Write a function `sum_multiples(limit: int, factor: int) -> int` summing all positive integers <= limit divisible by factor.",
                "starter_code": "def sum_multiples(limit: int, factor: int) -> int:\n    # Calculate sum of multiples\n    pass\n",
                "entry_function_name": "sum_multiples",
                "xp_reward": 75,
                "hints": [
                    "Use a `for` loop with `range(factor, limit + 1, factor)`.",
                    "Or loop from 1 to limit and check `i % factor == 0`."
                ],
                "test_cases": [
                    {"input": [10, 3], "expected": 18, "description": "Multiples of 3 up to 10", "is_hidden": False},
                    {"input": [20, 5], "expected": 50, "description": "Multiples of 5 up to 20", "is_hidden": False}
                ]
            }
        ]
    },
    {
        "id": "mod-4",
        "slug": "level-4-functions",
        "title": "Level 4: Reusable Functions",
        "description": "Function signatures, parameters, return statements, and docstrings.",
        "level_number": 4,
        "order_index": 4,
        "challenges": [
            {
                "id": "chal-4",
                "slug": "challenge-palindrome",
                "title": "Palindrome Checker",
                "instructions": "Write a function `is_palindrome(text: str) -> bool` that returns True if the text is a palindrome, ignoring case and spaces.",
                "starter_code": "def is_palindrome(text: str) -> bool:\n    # Return True if palindrome\n    pass\n",
                "entry_function_name": "is_palindrome",
                "xp_reward": 90,
                "hints": [
                    "Clean the string with `char.lower()` and `char.isalnum()`.",
                    "Reverse with `[::-1]`."
                ],
                "test_cases": [
                    {"input": ["racecar"], "expected": True, "description": "racecar is a palindrome", "is_hidden": False},
                    {"input": ["hello"], "expected": False, "description": "hello is not a palindrome", "is_hidden": False}
                ]
            }
        ]
    },
    {
        "id": "mod-5",
        "slug": "level-5-data-structures",
        "title": "Level 5: Collections & Maps",
        "description": "Lists, dictionaries, sets, and comprehension patterns.",
        "level_number": 5,
        "order_index": 5,
        "challenges": [
            {
                "id": "chal-5",
                "slug": "challenge-word-frequency",
                "title": "Word Frequency Counter",
                "instructions": "Write a function `count_frequencies(words: list[str]) -> dict[str, int]` counting occurrences of each word.",
                "starter_code": "def count_frequencies(words: list[str]) -> dict[str, int]:\n    # Count frequencies\n    pass\n",
                "entry_function_name": "count_frequencies",
                "xp_reward": 100,
                "hints": [
                    "Initialize a dictionary `freq = {}`.",
                    "Use `freq[w] = freq.get(w, 0) + 1`."
                ],
                "test_cases": [
                    {"input": [["apple", "banana", "apple"]], "expected": {"apple": 2, "banana": 1}, "description": "Word frequencies", "is_hidden": False},
                    {"input": [[]], "expected": {}, "description": "Empty list", "is_hidden": True}
                ]
            }
        ]
    }
]

# In-memory simulated learner state for demonstration & local development
CURRENT_PROFILE = {
    "id": "user-demo-123",
    "username": "python_learner",
    "display_name": "Alex Mercer",
    "total_xp": 120,
    "current_level": 2,
    "current_streak": 3,
    "longest_streak": 5,
    "completed_challenges": {"chal-1"},
    "badges": [
        {"code": "first_blood", "name": "First Spark", "description": "Ran your first Python program.", "icon": "⚡", "xp_bonus": 50, "awarded": True},
        {"code": "level1_master", "name": "Syntax Initiate", "description": "Completed Level 1.", "icon": "🌱", "xp_bonus": 100, "awarded": True},
        {"code": "logic_lord", "name": "Logic Master", "description": "Mastered conditional logic.", "icon": "🔮", "xp_bonus": 150, "awarded": False},
        {"code": "loop_luminary", "name": "Loop Luminary", "description": "Mastered loops.", "icon": "🔁", "xp_bonus": 200, "awarded": False},
        {"code": "function_guru", "name": "Function Guru", "description": "Mastered functions.", "icon": "⚙️", "xp_bonus": 250, "awarded": False}
    ]
}


def get_profile() -> UserProfile:
    total_xp = CURRENT_PROFILE["total_xp"]
    current_level = max(1, (total_xp // 100) + 1)
    CURRENT_PROFILE["current_level"] = current_level

    badge_models = [
        BadgeItem(**b) for b in CURRENT_PROFILE["badges"]
    ]

    return UserProfile(
        id=CURRENT_PROFILE["id"],
        username=CURRENT_PROFILE["username"],
        display_name=CURRENT_PROFILE["display_name"],
        total_xp=total_xp,
        current_level=current_level,
        current_streak=CURRENT_PROFILE["current_streak"],
        longest_streak=CURRENT_PROFILE["longest_streak"],
        badges=badge_models
    )


def get_curriculum() -> List[ModuleItem]:
    completed = set(CURRENT_PROFILE.get("completed_challenges", set()))
    modules: List[ModuleItem] = []

    # Strict progression: Challenge i is available if i-1 is completed. First challenge is always available.
    previous_completed = True

    for mod in CURRICULUM_DATA:
        challenge_summaries = []
        for ch in mod["challenges"]:
            ch_id = ch["id"]
            if ch_id in completed:
                status = "completed"
                previous_completed = True
            elif previous_completed:
                status = "available"
                previous_completed = False
            else:
                status = "locked"
                previous_completed = False

            challenge_summaries.append(
                ChallengeSummary(
                    id=ch["id"],
                    slug=ch["slug"],
                    title=ch["title"],
                    instructions=ch["instructions"],
                    starter_code=ch["starter_code"],
                    entry_function_name=ch.get("entry_function_name"),
                    xp_reward=ch["xp_reward"],
                    status=status,
                    hints=ch.get("hints", [])
                )
            )

        modules.append(
            ModuleItem(
                id=mod["id"],
                slug=mod["slug"],
                title=mod["title"],
                description=mod["description"],
                level_number=mod["level_number"],
                order_index=mod["order_index"],
                is_locked=all(c.status == "locked" for c in challenge_summaries),
                challenges=challenge_summaries
            )
        )

    return modules


def find_challenge_by_id(challenge_id: str) -> Optional[Dict[str, Any]]:
    for mod in CURRICULUM_DATA:
        for ch in mod["challenges"]:
            if ch["id"] == challenge_id:
                return ch
    return None


def record_challenge_completion(challenge_id: str) -> Dict[str, Any]:
    challenge = find_challenge_by_id(challenge_id)
    if not challenge:
        return {"xp_earned": 0, "new_badges": []}

    completed_set = CURRENT_PROFILE.setdefault("completed_challenges", set())
    is_first_time = challenge_id not in completed_set
    xp_to_award = challenge["xp_reward"] if is_first_time else 10  # Reduced XP for repeats

    if is_first_time:
        completed_set.add(challenge_id)
        CURRENT_PROFILE["total_xp"] += xp_to_award
        CURRENT_PROFILE["current_streak"] += 1

    # Check badges
    new_badges = []
    if len(completed_set) >= 1:
        for b in CURRENT_PROFILE["badges"]:
            if b["code"] == "first_blood" and not b["awarded"]:
                b["awarded"] = True
                new_badges.append(b["name"])
                CURRENT_PROFILE["total_xp"] += b["xp_bonus"]

    return {
        "xp_earned": xp_to_award,
        "new_streak": CURRENT_PROFILE["current_streak"],
        "unlocked_next": is_first_time,
        "badges_awarded": new_badges
    }
