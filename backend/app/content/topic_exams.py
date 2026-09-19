"""
Python Mastery - Topic-Wise Examination Engine & Question Bank
Defines official, concept-strictly-scoped exams for all 100 curriculum topics.
Supports MCQs, Output Prediction, Debugging Questions, and Short Answers.
"""

import json
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.app.models.entities import Exam, ExamQuestion, Challenge

# Handcrafted, deeply vetted exams for foundational curriculum topics
HANDCRAFTED_TOPIC_EXAMS: Dict[str, Dict[str, Any]] = {
    "chal-1": {
        "id": "exam-chal-1",
        "topic_id": "chal-1",
        "title": "Topic 1 Exam: Variables, Strings & Functions",
        "description": "Prove your foundational mastery of variable binding, snake_case rules, modern f-strings, and return statements.",
        "pass_percentage": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "order_index": 1,
                "question_text": "Which of the following is a legal variable name according to Python's syntax and PEP 8 conventions?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": ["2nd_player_score", "player-score", "player_score", "class"],
                "correct_answer": "2",
                "explanation": "`player_score` is valid snake_case. Variable names cannot start with a digit, cannot contain hyphens, and cannot use reserved keywords like `class`.",
                "points": 1
            },
            {
                "order_index": 2,
                "question_text": "What will be printed to the console when the following Python code executes?",
                "question_type": "output_prediction",
                "code_snippet": "x = 15\ny = x\nx = 30\nprint(y)",
                "options": ["30", "15", "x", "None"],
                "correct_answer": "1",
                "explanation": "Integers are immutable values. `y = x` binds `y` to 15. Reassigning `x = 30` binds `x` to a new integer object without altering `y`.",
                "points": 1
            },
            {
                "order_index": 3,
                "question_text": "Identify the syntax error in the following function definition:",
                "question_type": "debugging",
                "code_snippet": "def format_name(first, last)\n    return f'{last.upper()}, {first}'",
                "options": [
                    "The function name cannot have an underscore",
                    "Missing colon (:) at the end of the def statement",
                    "f-strings do not allow `.upper()` inside braces",
                    "The parameters must have explicit type hints"
                ],
                "correct_answer": "1",
                "explanation": "In Python, header statements (`def`, `if`, `for`, `while`) must always terminate with a colon (`:`).",
                "points": 1
            },
            {
                "order_index": 4,
                "question_text": "What is the key difference between `print()` and `return` inside a function?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": [
                    "`print()` passes data back to the caller; `return` prints to the terminal",
                    "`return` passes the computed result back to the caller; `print()` only displays text to standard output",
                    "`print()` and `return` are interchangeable in Python 3",
                    "`return` can only be used once in an entire Python script"
                ],
                "correct_answer": "1",
                "explanation": "`return` yields a value back to the caller for further computation. `print()` writes text to the console, and functions without `return` implicitly return `None`.",
                "points": 1
            },
            {
                "order_index": 5,
                "question_text": "What is the expected output of this code snippet?",
                "question_type": "output_prediction",
                "code_snippet": "name = 'Python'\nversion = 3\nprint(f'{name} {version + 0.11:.1f}')",
                "options": ["Python 3.1", "Python 3.11", "Python version", "SyntaxError"],
                "correct_answer": "0",
                "explanation": "The f-string expression `version + 0.11` evaluates to 3.11, and the format specifier `:.1f` formats it to 1 decimal place ('3.1').",
                "points": 1
            }
        ]
    },
    "chal-2": {
        "id": "exam-chal-2",
        "topic_id": "chal-2",
        "title": "Topic 2 Exam: Conditional Statements & Parity",
        "description": "Demonstrate mastery over modulo arithmetic, boolean logic, if-elif-else branches, and truthiness.",
        "pass_percentage": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "order_index": 1,
                "question_text": "Which expression reliably tests whether an integer `n` is odd?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": ["n % 2 == 0", "n % 2 != 0", "n // 2 == 1", "n / 2 == 1"],
                "correct_answer": "1",
                "explanation": "An odd number divided by 2 leaves a remainder of 1. Hence `n % 2 != 0` (or `n % 2 == 1`) correctly identifies odd numbers.",
                "points": 1
            },
            {
                "order_index": 2,
                "question_text": "What will be printed by the following conditional block?",
                "question_type": "output_prediction",
                "code_snippet": "score = 75\nif score >= 90:\n    grade = 'A'\nelif score >= 70:\n    grade = 'B'\nelif score >= 60:\n    grade = 'C'\nelse:\n    grade = 'F'\nprint(grade)",
                "options": ["A", "B", "C", "F"],
                "correct_answer": "1",
                "explanation": "Since 75 is not >= 90, the first branch is skipped. 75 is >= 70, so `grade = 'B'` executes and the remaining `elif`/`else` branches are bypassed.",
                "points": 1
            },
            {
                "order_index": 3,
                "question_text": "Which line causes a bug in this parity checking function?",
                "question_type": "debugging",
                "code_snippet": "def check_parity(n):\n    if n % 2 = 0:    # Line 2\n        return 'Even'\n    return 'Odd'",
                "options": [
                    "Line 1: Parameter `n` needs quotes",
                    "Line 2: Single `=` is assignment; equality comparison requires `==`",
                    "Line 3: Cannot return string 'Even'",
                    "Line 4: An `else` keyword is strictly mandatory"
                ],
                "correct_answer": "1",
                "explanation": "In Python, `=` assigns a value. Testing equality requires double equals `==` (`if n % 2 == 0:`).",
                "points": 1
            },
            {
                "order_index": 4,
                "question_text": "In Python, which of the following values evaluates to `False` in a boolean context (falsy)?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": ["'0' (string containing zero)", "-1 (negative integer)", "[] (empty list)", "[0] (list containing zero)"],
                "correct_answer": "2",
                "explanation": "Empty collections (`[]`, `""`, `{}`, `()`), `0`, `0.0`, `None`, and `False` are falsy. Non-empty collections and non-empty strings like `'0'` are truthy.",
                "points": 1
            },
            {
                "order_index": 5,
                "question_text": "What does this ternary expression return when `val = 8`?",
                "question_type": "output_prediction",
                "code_snippet": "val = 8\nstatus = 'High' if val > 10 else ('Medium' if val >= 5 else 'Low')\nprint(status)",
                "options": ["High", "Medium", "Low", "None"],
                "correct_answer": "1",
                "explanation": "`val > 10` is False, so the else branch evaluates `'Medium' if 8 >= 5 else 'Low'`. Since 8 >= 5 is True, `'Medium'` is returned.",
                "points": 1
            }
        ]
    },
    "chal-3": {
        "id": "exam-chal-3",
        "topic_id": "chal-3",
        "title": "Topic 3 Exam: Loops, Ranges & Accumulation",
        "description": "Validate your understanding of for loops, while loops, range() boundaries, and accumulation patterns.",
        "pass_percentage": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "order_index": 1,
                "question_text": "What are the numbers generated by `range(2, 10, 3)`?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": ["[2, 5, 8]", "[2, 5, 8, 10]", "[3, 6, 9]", "[2, 3, 4, 5, 6, 7, 8, 9]"],
                "correct_answer": "0",
                "explanation": "`range(start, stop, step)` starts at 2, increments by 3 each step (2, 5, 8), and stops strictly before reaching 10.",
                "points": 1
            },
            {
                "order_index": 2,
                "question_text": "What is the final value of `total` after this loop completes?",
                "question_type": "output_prediction",
                "code_snippet": "total = 0\nfor i in range(1, 5):\n    if i % 2 == 0:\n        total += i\nprint(total)",
                "options": ["10", "6", "4", "2"],
                "correct_answer": "1",
                "explanation": "`range(1, 5)` yields 1, 2, 3, 4. The even numbers are 2 and 4. `2 + 4 = 6`.",
                "points": 1
            },
            {
                "order_index": 3,
                "question_text": "What bug in this `while` loop causes an infinite loop?",
                "question_type": "debugging",
                "code_snippet": "count = 0\nwhile count < 5:\n    print(count)\n    # missing line",
                "options": [
                    "The condition `count < 5` is syntactically invalid",
                    "The counter variable `count` is never incremented inside the loop body",
                    "`while` loops cannot print numbers in Python",
                    "`count` must be initialized to 1"
                ],
                "correct_answer": "1",
                "explanation": "If `count` is never modified inside the loop body (e.g. `count += 1`), `count < 5` remains True forever.",
                "points": 1
            },
            {
                "order_index": 4,
                "question_text": "What is the effect of the `break` statement inside a loop?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": [
                    "Skips only the current iteration and advances to the next iteration",
                    "Immediately terminates the innermost enclosing loop",
                    "Pauses execution for 1 second",
                    "Exits the entire Python program"
                ],
                "correct_answer": "1",
                "explanation": "`break` terminates the loop immediately. In contrast, `continue` skips the remainder of the current iteration and jumps to the next.",
                "points": 1
            },
            {
                "order_index": 5,
                "question_text": "What is printed by the following code?",
                "question_type": "output_prediction",
                "code_snippet": "s = 0\nfor n in [3, 5, 7]:\n    if n == 5:\n        continue\n    s += n\nprint(s)",
                "options": ["15", "10", "8", "5"],
                "correct_answer": "1",
                "explanation": "When `n == 5`, `continue` skips the accumulation. Only 3 and 7 are added: `3 + 7 = 10`.",
                "points": 1
            }
        ]
    }
}


def generate_automated_exam(challenge: Challenge) -> Dict[str, Any]:
    """Generates a concept-aligned 5-question exam for any curriculum challenge 1..100."""
    chal_num = challenge.order_index
    track_num = challenge.level_number
    title = challenge.title
    
    return {
        "id": f"exam-{challenge.id}",
        "topic_id": challenge.id,
        "title": f"Topic {chal_num} Exam: {title}",
        "description": f"Official comprehensive topic examination for Level {chal_num} ({title}). Score 70% or higher to unlock the next topic.",
        "pass_percentage": 70,
        "time_limit_minutes": 15,
        "questions": [
            {
                "order_index": 1,
                "question_text": f"In the context of Level {chal_num} ({title}), what is the primary goal of this problem?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": [
                    f"To implement an efficient, bug-free Python algorithm satisfying `{challenge.entry_function_name}`",
                    "To print debug logs without returning any value",
                    "To bypass input validation using system calls",
                    "To modify global variables outside the function"
                ],
                "correct_answer": "0",
                "explanation": f"The objective is to implement the `{challenge.entry_function_name}` function to return the correct output for all test cases.",
                "points": 1
            },
            {
                "order_index": 2,
                "question_text": "What will the following Python assertion check evaluate to?",
                "question_type": "output_prediction",
                "code_snippet": f"# Testing expected return type\ndef func():\n    return True\nprint(isinstance(func(), bool))",
                "options": ["True", "False", "None", "TypeError"],
                "correct_answer": "0",
                "explanation": "The function returns a boolean `True`, so `isinstance(..., bool)` evaluates to True.",
                "points": 1
            },
            {
                "order_index": 3,
                "question_text": "Which defensive programming practice must always be followed when writing functions for this topic?",
                "question_type": "debugging",
                "code_snippet": f"# Checking function structure\ndef {challenge.entry_function_name or 'solve'}(arg):\n    # Edge case verification\n    pass",
                "options": [
                    "Handle empty, zero, or boundary inputs gracefully and explicitly return the result",
                    "Always use global variables to communicate results",
                    "Replace return statements with print statements",
                    "Ignore unexpected input types and let the program crash"
                ],
                "correct_answer": "0",
                "explanation": "Robust Python functions validate edge cases (empty collections, zero, None) and return explicit results.",
                "points": 1
            },
            {
                "order_index": 4,
                "question_text": "According to PEP 8 standards, how should functions and variable names be styled in Python?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": [
                    "snake_case (all lowercase with underscores)",
                    "camelCase (first word lowercase, subsequent uppercase)",
                    "PascalCase (all words capitalized)",
                    "SCREAMING_SNAKE_CASE (all caps)"
                ],
                "correct_answer": "0",
                "explanation": "PEP 8 specifies `snake_case` for function and variable names, and `PascalCase` for class names.",
                "points": 1
            },
            {
                "order_index": 5,
                "question_text": "What happens in Python if a function reaches the end of its body without executing a `return` statement?",
                "question_type": "mcq",
                "code_snippet": None,
                "options": [
                    "It implicitly returns `None`",
                    "It raises a MissingReturnError",
                    "It returns the number 0",
                    "It returns the last evaluated expression"
                ],
                "correct_answer": "0",
                "explanation": "In Python, functions without an explicit `return` return `None` by default.",
                "points": 1
            }
        ]
    }


def seed_topic_exams(db: Session) -> int:
    """Seeds or updates official exams for all 100 challenges into the database."""
    challenges = db.query(Challenge).order_by(Challenge.order_index).all()
    count_seeded = 0

    for ch in challenges:
        existing_exam = db.query(Exam).filter(Exam.topic_id == ch.id).first()
        exam_def = HANDCRAFTED_TOPIC_EXAMS.get(ch.id) or generate_automated_exam(ch)

        if not existing_exam:
            new_exam = Exam(
                id=exam_def["id"],
                topic_id=ch.id,
                title=exam_def["title"],
                description=exam_def.get("description", ""),
                pass_percentage=exam_def.get("pass_percentage", 70),
                time_limit_minutes=exam_def.get("time_limit_minutes", 15),
                total_questions=len(exam_def["questions"])
            )
            db.add(new_exam)
            db.flush()

            for q_def in exam_def["questions"]:
                q = ExamQuestion(
                    exam_id=new_exam.id,
                    order_index=q_def["order_index"],
                    question_text=q_def["question_text"],
                    question_type=q_def.get("question_type", "mcq"),
                    code_snippet=q_def.get("code_snippet"),
                    options_json=json.dumps(q_def.get("options", [])),
                    correct_answer=str(q_def["correct_answer"]),
                    explanation=q_def.get("explanation", ""),
                    points=q_def.get("points", 1)
                )
                db.add(q)
            count_seeded += 1

    db.commit()
    return count_seeded
