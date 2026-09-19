"""
Database Engine, Session Factory, and Initial Seeder
Configures SQLAlchemy to connect to PostgreSQL / Supabase, with automatic fallback
to persistent SQLite for local zero-config operation.
"""

import os
import json
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.app.core.config import settings
from backend.app.models.entities import Base, Challenge, Badge

# Determine Database URL
# If postgresql is specified, use it. Otherwise, default to local persistent sqlite file
db_url = settings.DATABASE_URL
if not db_url or "localhost:5432" in db_url or "your-password" in db_url:
    # Use persistent SQLite in the project backend folder
    db_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "mastery.db")
    db_url = f"sqlite:///{db_file}"

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Create tables and seed initial curriculum, badges, and topic exams if empty."""
    Base.metadata.create_all(bind=engine)

    # SQLite column migration for user_progress, profiles, and xp_transactions
    from sqlalchemy import text
    with engine.connect() as conn:
        try:
            # user_progress migrations
            res_up = conn.execute(text("PRAGMA table_info(user_progress)")).fetchall()
            existing_cols_up = [r[1] for r in res_up]
            if "lesson_completed" not in existing_cols_up:
                conn.execute(text("ALTER TABLE user_progress ADD COLUMN lesson_completed BOOLEAN DEFAULT 0 NOT NULL"))
            if "practice_completed" not in existing_cols_up:
                conn.execute(text("ALTER TABLE user_progress ADD COLUMN practice_completed BOOLEAN DEFAULT 0 NOT NULL"))
            if "exam_passed" not in existing_cols_up:
                conn.execute(text("ALTER TABLE user_progress ADD COLUMN exam_passed BOOLEAN DEFAULT 0 NOT NULL"))

            # profiles migrations
            res_prof = conn.execute(text("PRAGMA table_info(profiles)")).fetchall()
            existing_cols_prof = [r[1] for r in res_prof]
            if "current_rank" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN current_rank VARCHAR(20) DEFAULT 'GOLD' NOT NULL"))
            if "performance_score" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN performance_score REAL DEFAULT 60.0 NOT NULL"))
            if "topic_exam_avg" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN topic_exam_avg REAL DEFAULT 60.0 NOT NULL"))
            if "coding_performance" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN coding_performance REAL DEFAULT 60.0 NOT NULL"))
            if "weekly_test_avg" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN weekly_test_avg REAL DEFAULT 60.0 NOT NULL"))
            if "monthly_test_avg" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN monthly_test_avg REAL DEFAULT 60.0 NOT NULL"))
            if "consistency_score" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN consistency_score REAL DEFAULT 60.0 NOT NULL"))
            if "consecutive_low_performance_count" not in existing_cols_prof:
                conn.execute(text("ALTER TABLE profiles ADD COLUMN consecutive_low_performance_count INTEGER DEFAULT 0 NOT NULL"))

            # xp_transactions migrations
            res_xp = conn.execute(text("PRAGMA table_info(xp_transactions)")).fetchall()
            existing_cols_xp = [r[1] for r in res_xp]
            if "transaction_key" not in existing_cols_xp:
                conn.execute(text("ALTER TABLE xp_transactions ADD COLUMN transaction_key VARCHAR(120)"))
            if "source_type" not in existing_cols_xp:
                conn.execute(text("ALTER TABLE xp_transactions ADD COLUMN source_type VARCHAR(50)"))
            if "source_id" not in existing_cols_xp:
                conn.execute(text("ALTER TABLE xp_transactions ADD COLUMN source_id VARCHAR(50)"))

            conn.commit()
        except Exception as e:
            pass

    with SessionLocal() as db:
        # Seed Badges if not present
        if db.query(Badge).count() == 0:
            badges_data = [
                Badge(id="b-1", code="first_blood", name="First Spark", description="Ran your first Python program successfully.", icon="⚡", xp_bonus=50),
                Badge(id="b-2", code="level1_master", name="Syntax Initiate", description="Completed Level 1: Variables & Data Types.", icon="🌱", xp_bonus=100),
                Badge(id="b-3", code="logic_lord", name="Logic Master", description="Conquered Level 2: Conditional Statements.", icon="🔮", xp_bonus=150),
                Badge(id="b-4", code="loop_luminary", name="Loop Luminary", description="Mastered Level 3: Loops & Iterations.", icon="🔁", xp_bonus=200),
                Badge(id="b-5", code="function_guru", name="Architect of Functions", description="Completed Level 4: Functions & Scope.", icon="⚙️", xp_bonus=250),
                Badge(id="b-6", code="collection_captain", name="Data Commander", description="Completed Level 5: Lists & Dictionaries.", icon="🏆", xp_bonus=300)
            ]
            db.add_all(badges_data)
            db.commit()

        # Seed Topic Exams
        from backend.app.content.topic_exams import seed_topic_exams
        seed_topic_exams(db)

        # Seed Level Final Tests and Periodic Tests
        from backend.app.content.level_and_periodic_tests import seed_level_and_periodic_tests
        seed_level_and_periodic_tests(db)

        # Seed Challenges if not present
        if db.query(Challenge).count() == 0:
            challenges_data = [
                Challenge(
                    id="chal-1",
                    slug="challenge-greet",
                    title="Personalized Greeting",
                    level_number=1,
                    order_index=1,
                    difficulty="easy",
                    instructions="Write a function `greet(name: str) -> str` that returns 'Hello, <name>!'",
                    starter_code="def greet(name: str) -> str:\n    # Return greeting string\n    pass\n",
                    solution_code="def greet(name: str) -> str:\n    return f'Hello, {name}!'\n",
                    entry_function_name="greet",
                    test_cases_json=json.dumps([
                        {"input": ["Alice"], "expected": "Hello, Alice!", "description": "Greeting Alice", "is_hidden": False},
                        {"input": ["Bob"], "expected": "Hello, Bob!", "description": "Greeting Bob", "is_hidden": False},
                        {"input": ["Pythonista"], "expected": "Hello, Pythonista!", "description": "Greeting Pythonista", "is_hidden": True}
                    ]),
                    hints_json=json.dumps([
                        "Remember to use the `return` keyword instead of `print()`.",
                        "Use an f-string: `f'Hello, {name}!'`."
                    ]),
                    xp_reward=50,
                    time_limit_seconds=300,
                    sandbox_timeout_seconds=3.0
                ),
                Challenge(
                    id="chal-2",
                    slug="challenge-even-or-odd",
                    title="Even or Odd Parity",
                    level_number=2,
                    order_index=2,
                    difficulty="easy",
                    instructions="Write a function `check_parity(n: int) -> str` that returns 'Even' if n is even, and 'Odd' otherwise.",
                    starter_code="def check_parity(n: int) -> str:\n    # Return 'Even' or 'Odd'\n    pass\n",
                    solution_code="def check_parity(n: int) -> str:\n    return 'Even' if n % 2 == 0 else 'Odd'\n",
                    entry_function_name="check_parity",
                    test_cases_json=json.dumps([
                        {"input": [4], "expected": "Even", "description": "4 is Even", "is_hidden": False},
                        {"input": [7], "expected": "Odd", "description": "7 is Odd", "is_hidden": False},
                        {"input": [0], "expected": "Even", "description": "0 is Even", "is_hidden": True}
                    ]),
                    hints_json=json.dumps([
                        "Use the modulo operator `%`.",
                        "If `n % 2 == 0`, it's even."
                    ]),
                    xp_reward=60,
                    time_limit_seconds=300,
                    sandbox_timeout_seconds=3.0
                ),
                Challenge(
                    id="chal-3",
                    slug="challenge-sum-multiples",
                    title="Sum of Multiples",
                    level_number=3,
                    order_index=3,
                    difficulty="medium",
                    instructions="Write a function `sum_multiples(limit: int, factor: int) -> int` summing all positive integers <= limit divisible by factor.",
                    starter_code="def sum_multiples(limit: int, factor: int) -> int:\n    # Calculate sum of multiples\n    pass\n",
                    solution_code="def sum_multiples(limit: int, factor: int) -> int:\n    return sum(i for i in range(factor, limit + 1, factor))\n",
                    entry_function_name="sum_multiples",
                    test_cases_json=json.dumps([
                        {"input": [10, 3], "expected": 18, "description": "Multiples of 3 up to 10: 3+6+9 = 18", "is_hidden": False},
                        {"input": [20, 5], "expected": 50, "description": "Multiples of 5 up to 20: 5+10+15+20 = 50", "is_hidden": False}
                    ]),
                    hints_json=json.dumps([
                        "Use a `for` loop with `range(factor, limit + 1, factor)`.",
                        "Or loop from 1 to limit and check `i % factor == 0`."
                    ]),
                    xp_reward=75,
                    time_limit_seconds=420,
                    sandbox_timeout_seconds=3.0
                ),
                Challenge(
                    id="chal-4",
                    slug="challenge-palindrome",
                    title="Palindrome Checker",
                    level_number=4,
                    order_index=4,
                    difficulty="medium",
                    instructions="Write a function `is_palindrome(text: str) -> bool` that returns True if the text is a palindrome, ignoring case and spaces.",
                    starter_code="def is_palindrome(text: str) -> bool:\n    # Return True if palindrome\n    pass\n",
                    solution_code="def is_palindrome(text: str) -> bool:\n    cleaned = ''.join(ch.lower() for ch in text if ch.isalnum())\n    return cleaned == cleaned[::-1]\n",
                    entry_function_name="is_palindrome",
                    test_cases_json=json.dumps([
                        {"input": ["racecar"], "expected": True, "description": "racecar is a palindrome", "is_hidden": False},
                        {"input": ["hello"], "expected": False, "description": "hello is not a palindrome", "is_hidden": False}
                    ]),
                    hints_json=json.dumps([
                        "Clean the string with `char.lower()` and `char.isalnum()`.",
                        "Reverse with `[::-1]`."
                    ]),
                    xp_reward=90,
                    time_limit_seconds=420,
                    sandbox_timeout_seconds=3.0
                ),
                Challenge(
                    id="chal-5",
                    slug="challenge-word-frequency",
                    title="Word Frequency Counter",
                    level_number=5,
                    order_index=5,
                    difficulty="hard",
                    instructions="Write a function `count_frequencies(words: list[str]) -> dict[str, int]` counting occurrences of each word.",
                    starter_code="def count_frequencies(words: list[str]) -> dict[str, int]:\n    # Count frequencies\n    pass\n",
                    solution_code="def count_frequencies(words: list[str]) -> dict[str, int]:\n    freq = {}\n    for w in words:\n        freq[w] = freq.get(w, 0) + 1\n    return freq\n",
                    entry_function_name="count_frequencies",
                    test_cases_json=json.dumps([
                        {"input": [["apple", "banana", "apple"]], "expected": {"apple": 2, "banana": 1}, "description": "Word frequencies", "is_hidden": False},
                        {"input": [["cat", "dog", "cat", "bird"]], "expected": {"cat": 2, "dog": 1, "bird": 1}, "description": "Multiple animals", "is_hidden": False},
                        {"input": [[]], "expected": {}, "description": "Empty list", "is_hidden": True}
                    ]),
                    hints_json=json.dumps([
                        "Initialize a dictionary `freq = {}`.",
                        "Use `freq[w] = freq.get(w, 0) + 1`."
                    ]),
                    xp_reward=100,
                    time_limit_seconds=600,
                    sandbox_timeout_seconds=3.0
                )
            ]
            db.add_all(challenges_data)
            db.commit()


def get_db() -> Generator[Session, None, None]:
    """FastAPI Dependency for database sessions."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
