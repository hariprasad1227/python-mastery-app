"""
Level Final Tests & Periodic Tests Content Seeder
Seeds 10 Level Final Tests and 6 Periodic Tests (4 Weekly + 2 Monthly)
with multi-type questions (MCQ, Output Prediction, Debugging, Short Answer, Coding).
"""

import json
from sqlalchemy.orm import Session
from backend.app.models.entities import (
    LevelFinalTest, LevelFinalTestQuestion,
    PeriodicTest, PeriodicTestQuestion
)

LEVEL_TESTS_METADATA = [
    {
        "level_number": 1,
        "title": "Level 1 Final Comprehensive Test: Python Foundations",
        "description": "Exhaustive evaluation on variables, data types, type conversions, comments, and input/output.",
        "pass_percentage": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": "Which of the following is an invalid variable name in Python?",
                "options": ["_count", "total_sum", "2nd_value", "value_2"],
                "correct_answer": "2nd_value",
                "explanation": "Variable names in Python cannot begin with a number.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the exact output of this code snippet?",
                "code_snippet": "a = 5\nb = '10'\nprint(str(a) + b)",
                "options": ["15", "510", "Error", "5 10"],
                "correct_answer": "510",
                "explanation": "str(5) is '5', and string concatenation '5' + '10' results in '510'.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "Identify the bug in this code intended to convert user age to an integer:",
                "code_snippet": "age = input('Enter age: ')\nnext_year = age + 1",
                "options": [
                    "input() must be converted with int(age)",
                    "input() must take two arguments",
                    "next_year must be defined first",
                    "No error exists"
                ],
                "correct_answer": "input() must be converted with int(age)",
                "explanation": "input() returns a string; adding 1 directly causes a TypeError.",
                "points": 1
            },
            {
                "question_type": "short_answer",
                "question_text": "What built-in function returns the data type of an object in Python?",
                "code_snippet": "x = 3.14\n# Returns float",
                "options": ["type", "type()", "typeof", "dtype"],
                "correct_answer": "type",
                "explanation": "The type() function returns the class/type of any Python object.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What does bool(0) and bool('') evaluate to in Python?",
                "code_snippet": "print(bool(0), bool(''))",
                "options": ["False False", "True True", "False True", "True False"],
                "correct_answer": "False False",
                "explanation": "In Python, 0 and empty strings are falsy values, so both evaluate to False.",
                "points": 1
            },
            {
                "question_type": "coding",
                "question_text": "What operator computes remainder in integer division?",
                "code_snippet": "rem = 17 % 5",
                "options": ["%", "//", "/", "**"],
                "correct_answer": "%",
                "explanation": "The modulo operator % returns the division remainder (17 % 5 = 2).",
                "points": 1
            }
        ]
    },
    {
        "level_number": 2,
        "title": "Level 2 Final Comprehensive Test: Operators & Decision Making",
        "description": "Rigorous assessment on comparison, logical, assignment operators, and conditional trees.",
        "pass_percentage": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_type": "output_prediction",
                "question_text": "What will this conditional print?",
                "code_snippet": "score = 82\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\nelse:\n    print('C')",
                "options": ["A", "B", "C", "B and C"],
                "correct_answer": "B",
                "explanation": "82 satisfies score >= 80, so 'B' is printed and the remaining elif/else are skipped.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "Which logical operator returns True only if BOTH operands are True?",
                "options": ["and", "or", "not", "xor"],
                "correct_answer": "and",
                "explanation": "The 'and' operator requires both conditions to be truthy.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the value of result?",
                "code_snippet": "x = 10\nresult = 'Even' if x % 2 == 0 else 'Odd'",
                "options": ["Even", "Odd", "True", "False"],
                "correct_answer": "Even",
                "explanation": "10 % 2 is 0, so the ternary expression resolves to 'Even'.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "What is wrong with this equality check?",
                "code_snippet": "if a = 5:\n    print('Five')",
                "options": [
                    "Must use == for comparison instead of assignment =",
                    "Missing parentheses around 5",
                    "Cannot compare numbers in if statements",
                    "Nothing is wrong"
                ],
                "correct_answer": "Must use == for comparison instead of assignment =",
                "explanation": "= is assignment, == is comparison.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "Which operator tests whether two variables point to the exact same memory object?",
                "options": ["is", "==", "in", "equals"],
                "correct_answer": "is",
                "explanation": "The 'is' identity operator compares memory addresses (identity), while '==' checks value equality.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the output of this expression?",
                "code_snippet": "print(True or False and False)",
                "options": ["True", "False", "None", "Error"],
                "correct_answer": "True",
                "explanation": "'and' has higher precedence than 'or': False and False is False; True or False is True.",
                "points": 1
            }
        ]
    },
    {
        "level_number": 3,
        "title": "Level 3 Final Comprehensive Test: Strings & Loops",
        "description": "Covers string indexing, slicing, methods, while loops, for loops, break, and continue.",
        "pass_percentage": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_type": "output_prediction",
                "question_text": "What does string slicing s[::-1] do?",
                "code_snippet": "s = 'Python'\nprint(s[::-1])",
                "options": ["nohtyP", "Python", "P", "Error"],
                "correct_answer": "nohtyP",
                "explanation": "A step of -1 reverses the sequence.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the output of this loop?",
                "code_snippet": "total = 0\nfor i in range(1, 5):\n    total += i\nprint(total)",
                "options": ["10", "15", "6", "4"],
                "correct_answer": "10",
                "explanation": "range(1, 5) produces 1, 2, 3, 4. Sum = 1 + 2 + 3 + 4 = 10.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "Which statement terminates loop execution entirely?",
                "options": ["break", "continue", "pass", "exit"],
                "correct_answer": "break",
                "explanation": "'break' cleanly terminates the closest enclosing loop immediately.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "How do you split a comma-separated string 'apple,banana,cherry' into a list?",
                "code_snippet": "fruits = 'apple,banana,cherry'.split(',')",
                "options": [".split(',')", ".join(',')", ".partition()", ".slice(',')"],
                "correct_answer": ".split(',')",
                "explanation": "str.split(delimiter) splits a string into a list of substrings.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is printed by this continue statement?",
                "code_snippet": "out = []\nfor i in range(4):\n    if i == 2:\n        continue\n    out.append(i)\nprint(out)",
                "options": ["[0, 1, 3]", "[0, 1, 2, 3]", "[2]", "[0, 1]"],
                "correct_answer": "[0, 1, 3]",
                "explanation": "'continue' skips the rest of the current iteration when i == 2.",
                "points": 1
            },
            {
                "question_type": "short_answer",
                "question_text": "Which method converts all characters in a string to lowercase?",
                "code_snippet": "'HELLO'.lower()",
                "options": ["lower", "lower()", "casefold", "to_lower"],
                "correct_answer": "lower",
                "explanation": "The str.lower() method returns a lowercase copy of the string.",
                "points": 1
            }
        ]
    }
]

# Generate metadata for Levels 4 to 10
LEVEL_TOPIC_NAMES = {
    4: ("Python Collections", "Lists, Tuples, Sets, and Dictionaries deep dive with methods and nesting."),
    5: ("Functions & Problem Solving", "Def, parameters, return values, *args, **kwargs, lambda, and scope."),
    6: ("Comprehensions, Modules & Errors", "List/dict/set comprehensions, try/except/finally, and standard library."),
    7: ("Files & Object-Oriented Programming", "File I/O (open, csv, json) and OOP (classes, inheritance, polymorphism)."),
    8: ("Advanced Python", "Decorators, generators, context managers, typing, and algorithmic concepts."),
    9: ("Professional Python", "Virtual environments, pytest, logging, HTTP, REST APIs, and SQLite."),
    10: ("Python Mastery", "Asyncio, multiprocessing, design patterns, performance, and software architecture.")
}

for lvl in range(4, 11):
    t_name, t_desc = LEVEL_TOPIC_NAMES[lvl]
    LEVEL_TESTS_METADATA.append({
        "level_number": lvl,
        "title": f"Level {lvl} Final Comprehensive Test: {t_name}",
        "description": t_desc,
        "pass_percentage": 70,
        "time_limit_minutes": 25,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": f"Which core principle is fundamental to {t_name} in Level {lvl}?",
                "options": ["Immutability and deterministic state", "Global mutable variables", "Ignoring exceptions", "Skipping unit tests"],
                "correct_answer": "Immutability and deterministic state",
                "explanation": "Clean Python software emphasizes deterministic state management and robust architecture.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": f"Predict the expected behavior of this Level {lvl} pattern:",
                "code_snippet": f"# Level {lvl} verification snippet\ndef verify_level_{lvl}(items):\n    return len([x for x in items if x])\nprint(verify_level_{lvl}([1, 0, 2, None, 3]))",
                "options": ["3", "5", "2", "Error"],
                "correct_answer": "3",
                "explanation": "1, 2, and 3 are truthy, while 0 and None are falsy, yielding 3 truthy elements.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": f"Identify the common pitfall in this Level {lvl} implementation:",
                "code_snippet": "def append_item(val, target_list=[]):\n    target_list.append(val)\n    return target_list",
                "options": [
                    "Default mutable argument is shared across all function calls",
                    "append does not return the list",
                    "val cannot be appended to lists",
                    "Function requires return None"
                ],
                "correct_answer": "Default mutable argument is shared across all function calls",
                "explanation": "Default argument [] is instantiated once at function definition, mutating across subsequent calls.",
                "points": 1
            },
            {
                "question_type": "short_answer",
                "question_text": "What keyword is used to yield values incrementally from a generator function?",
                "code_snippet": "def gen():\n    yield 42",
                "options": ["yield", "yield()", "return", "generate"],
                "correct_answer": "yield",
                "explanation": "The 'yield' statement pauses execution and yields values to the consumer.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": f"What is the recommended best practice when handling resources in Level {lvl}?",
                "options": [
                    "Use context managers with the 'with' statement",
                    "Manually close files without try/finally",
                    "Rely on garbage collection to close network sockets",
                    "Store file handles in global scope"
                ],
                "correct_answer": "Use context managers with the 'with' statement",
                "explanation": "The 'with' context manager guarantees clean teardown and exception safety.",
                "points": 1
            },
            {
                "question_type": "coding",
                "question_text": "Which method signature denotes an instance constructor in Python OOP?",
                "code_snippet": "class Service:\n    def __init__(self):\n        pass",
                "options": ["__init__", "constructor", "__construct__", "init"],
                "correct_answer": "__init__",
                "explanation": "__init__ is Python's standard object initializer method.",
                "points": 1
            }
        ]
    })

PERIODIC_TESTS_METADATA = [
    {
        "id": "weekly-test-1",
        "test_type": "weekly",
        "period_number": 1,
        "title": "Weekly Assessment 1: Fundamentals & Control Flow",
        "description": "Evaluates understanding of basic types, variables, if-statements, and string operations.",
        "pass_percentage": 70,
        "time_limit_minutes": 20,
        "xp_reward": 200,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": "Which expression checks whether 'py' exists in 'python'?",
                "options": ["'py' in 'python'", "'python'.contains('py')", "'py' == 'python'", "has('py', 'python')"],
                "correct_answer": "'py' in 'python'",
                "explanation": "The 'in' membership operator checks for substring existence.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the output of: print(10 // 3, 10 % 3)?",
                "options": ["3 1", "3.33 1", "3 0", "4 1"],
                "correct_answer": "3 1",
                "explanation": "10 // 3 is integer floor 3, and 10 % 3 is remainder 1.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "Find the error: if x = 10: print(x)",
                "options": ["Use == for comparison", "x cannot be 10", "print must be on next line", "No error"],
                "correct_answer": "Use == for comparison",
                "explanation": "= is assignment; conditionals require comparison ==",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "What is the default return type of input()?",
                "options": ["str", "int", "None", "bool"],
                "correct_answer": "str",
                "explanation": "input() always returns a string.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What does print('Python'[1:4]) output?",
                "options": ["yth", "ytho", "Pyt", "th"],
                "correct_answer": "yth",
                "explanation": "Index 1 is 'y', up to index 4 exclusive ('t', 'h') -> 'yth'.",
                "points": 1
            }
        ]
    },
    {
        "id": "weekly-test-2",
        "test_type": "weekly",
        "period_number": 2,
        "title": "Weekly Assessment 2: Collections & Functions",
        "description": "Assesses proficiency with lists, tuples, dictionaries, and functional paradigms.",
        "pass_percentage": 70,
        "time_limit_minutes": 20,
        "xp_reward": 200,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": "Which data structure is immutable in Python?",
                "options": ["tuple", "list", "set", "dict"],
                "correct_answer": "tuple",
                "explanation": "Tuples cannot be modified after creation.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the value of d.get('city', 'Unknown') if 'city' is not in d?",
                "options": ["Unknown", "None", "KeyError", "''"],
                "correct_answer": "Unknown",
                "explanation": "dict.get(key, default) safely returns default if key is absent.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "How do you pass an arbitrary number of keyword arguments to a function?",
                "options": ["**kwargs", "*args", "*kwargs", "kwargs[]"],
                "correct_answer": "**kwargs",
                "explanation": "**kwargs captures arbitrary keyword arguments as a dictionary.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "What does list.sort() return?",
                "options": ["None", "The sorted list", "A new list", "Boolean"],
                "correct_answer": "None",
                "explanation": "list.sort() sorts in-place and returns None.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is [x * 2 for x in [1, 2, 3]]?",
                "options": ["[2, 4, 6]", "[1, 2, 3, 1, 2, 3]", "[2, 2, 2]", "Error"],
                "correct_answer": "[2, 4, 6]",
                "explanation": "List comprehension doubles each element: 1*2, 2*2, 3*2.",
                "points": 1
            }
        ]
    },
    {
        "id": "weekly-test-3",
        "test_type": "weekly",
        "period_number": 3,
        "title": "Weekly Assessment 3: OOP, Exceptions & Modules",
        "description": "Tests object-oriented design, custom exceptions, and module architecture.",
        "pass_percentage": 70,
        "time_limit_minutes": 20,
        "xp_reward": 200,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": "Which clause always executes in a try/except statement?",
                "options": ["finally", "else", "except", "catch"],
                "correct_answer": "finally",
                "explanation": "'finally' block executes regardless of whether an exception occurred.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is printed by class inheritance super() call?",
                "code_snippet": "class A:\n    def greet(self): return 'A'\nclass B(A):\n    def greet(self): return super().greet() + 'B'\nprint(B().greet())",
                "options": ["AB", "B", "A", "Error"],
                "correct_answer": "AB",
                "explanation": "super().greet() returns 'A', then 'B' is concatenated -> 'AB'.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "How do you create a private attribute in a Python class?",
                "options": ["Prefix with two underscores (e.g. __balance)", "private balance", "Use @private decorator", "Prefix with dollar sign $balance"],
                "correct_answer": "Prefix with two underscores (e.g. __balance)",
                "explanation": "Leading double underscore invokes name mangling (_ClassName__attribute).",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "How do you raise a custom ValueError with message 'Invalid'?",
                "options": ["raise ValueError('Invalid')", "throw ValueError('Invalid')", "return ValueError('Invalid')", "raise 'Invalid'"],
                "correct_answer": "raise ValueError('Invalid')",
                "explanation": "Python uses 'raise' to signal exceptions.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the output of isinstance(True, int)?",
                "options": ["True", "False", "None", "Error"],
                "correct_answer": "True",
                "explanation": "In Python, bool is a subclass of int, so isinstance(True, int) is True.",
                "points": 1
            }
        ]
    },
    {
        "id": "weekly-test-4",
        "test_type": "weekly",
        "period_number": 4,
        "title": "Weekly Assessment 4: Advanced Python & Asyncio",
        "description": "Deep-dive into decorators, generators, asyncio event loops, and testing.",
        "pass_percentage": 70,
        "time_limit_minutes": 20,
        "xp_reward": 200,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": "What is a Python decorator fundamentally?",
                "options": ["A function that takes another function and extends its behavior", "A CSS style for terminals", "A syntax error validator", "A type casting method"],
                "correct_answer": "A function that takes another function and extends its behavior",
                "explanation": "Decorators are higher-order functions that wrap another function.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What keyword defines an asynchronous coroutine in Python?",
                "options": ["async def", "coroutine def", "thread def", "async func"],
                "correct_answer": "async def",
                "explanation": "'async def' declares an asynchronous coroutine function.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "Why does await need to be inside an async function?",
                "options": ["await pauses coroutine execution and is only legal within async functions", "await is deprecated", "await can only be used with time.sleep", "No restriction exists"],
                "correct_answer": "await pauses coroutine execution and is only legal within async functions",
                "explanation": "'await' expressions are syntactically valid only within 'async def' blocks.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "Which standard library module is used for unit testing with fixtures and assertions?",
                "options": ["unittest", "testsuite", "assertlib", "pytest_core"],
                "correct_answer": "unittest",
                "explanation": "Python includes 'unittest' in its standard library.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What does any([False, 0, '', True]) evaluate to?",
                "options": ["True", "False", "None", "Error"],
                "correct_answer": "True",
                "explanation": "any() returns True if at least one element is truthy.",
                "points": 1
            }
        ]
    },
    {
        "id": "monthly-test-1",
        "test_type": "monthly",
        "period_number": 1,
        "title": "Monthly Milestone Exam 1: Core Python Competency",
        "description": "Comprehensive evaluation covering Levels 1 through 5 fundamentals and collections.",
        "pass_percentage": 75,
        "time_limit_minutes": 30,
        "xp_reward": 500,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": "What is the time complexity of searching for a key in a Python dictionary?",
                "options": ["O(1) average", "O(n) average", "O(log n)", "O(n^2)"],
                "correct_answer": "O(1) average",
                "explanation": "Dictionaries use hash tables providing O(1) average time lookups.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What will print(list(map(lambda x: x**2, [1, 2, 3]))) output?",
                "options": ["[1, 4, 9]", "[2, 4, 6]", "[1, 8, 27]", "None"],
                "correct_answer": "[1, 4, 9]",
                "explanation": "lambda squares each item: 1**2=1, 2**2=4, 3**2=9.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "How do you merge two dictionaries in Python 3.9+?",
                "options": ["d1 | d2", "d1 + d2", "d1.merge(d2)", "d1 & d2"],
                "correct_answer": "d1 | d2",
                "explanation": "Python 3.9 introduced the union operator | for dictionaries.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "Which statement about Python lists is true?",
                "options": ["Lists are dynamic arrays that allow arbitrary element types", "Lists can only hold one data type", "Lists cannot be nested", "Lists have fixed size"],
                "correct_answer": "Lists are dynamic arrays that allow arbitrary element types",
                "explanation": "Python lists are heterogeneous, dynamically-resized arrays.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What does sorted(['10', '2', '1']) output?",
                "options": ["['1', '10', '2']", "['1', '2', '10']", "['2', '10', '1']", "Error"],
                "correct_answer": "['1', '10', '2']",
                "explanation": "Strings are sorted lexicographically (character-by-character), so '1' < '10' < '2'.",
                "points": 1
            }
        ]
    },
    {
        "id": "monthly-test-2",
        "test_type": "monthly",
        "period_number": 2,
        "title": "Monthly Milestone Exam 2: Professional Mastery & Architecture",
        "description": "Culminating evaluation covering Levels 6 through 10, software design, and resilience.",
        "pass_percentage": 75,
        "time_limit_minutes": 30,
        "xp_reward": 500,
        "questions": [
            {
                "question_type": "mcq",
                "question_text": "What does the GIL (Global Interpreter Lock) in CPython prevent?",
                "options": ["Multiple native OS threads from executing Python bytecode simultaneously", "Multiple processes from running", "File I/O operations", "Garbage collection"],
                "correct_answer": "Multiple native OS threads from executing Python bytecode simultaneously",
                "explanation": "The GIL ensures only one thread executes CPython bytecode at a time.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What is the purpose of @functools.wraps(fn) inside a decorator?",
                "options": ["Preserves the original function's metadata (__name__, __doc__)", "Speeds up execution by 2x", "Makes the function async", "Prevents recursion errors"],
                "correct_answer": "Preserves the original function's metadata (__name__, __doc__)",
                "explanation": "@wraps copies the original function's name and docstring to the wrapper.",
                "points": 1
            },
            {
                "question_type": "debugging",
                "question_text": "How do you achieve true parallel CPU-bound multiprocessing in Python?",
                "options": ["Use the multiprocessing module or ProcessPoolExecutor", "Use the threading module", "Use asyncio.gather", "Use time.sleep"],
                "correct_answer": "Use the multiprocessing module or ProcessPoolExecutor",
                "explanation": "Separate OS processes bypass the GIL and utilize multiple CPU cores.",
                "points": 1
            },
            {
                "question_type": "mcq",
                "question_text": "Which design pattern ensures a class has only one instance and provides global access to it?",
                "options": ["Singleton", "Factory", "Observer", "Strategy"],
                "correct_answer": "Singleton",
                "explanation": "The Singleton pattern restricts instantiation to a single object.",
                "points": 1
            },
            {
                "question_type": "output_prediction",
                "question_text": "What does asyncio.run(coroutine()) do?",
                "options": ["Creates an event loop, runs the coroutine to completion, and closes the loop", "Runs in a separate background thread", "Compiles Python to C", "Calls time.sleep"],
                "correct_answer": "Creates an event loop, runs the coroutine to completion, and closes the loop",
                "explanation": "asyncio.run manages the lifecycle of the asyncio event loop.",
                "points": 1
            }
        ]
    }
]


def seed_level_and_periodic_tests(db: Session):
    """Seeds the 10 Level Final Tests and 6 Periodic Tests if not present."""
    # 1. Level Final Tests
    for test_meta in LEVEL_TESTS_METADATA:
        lvl_num = test_meta["level_number"]
        test_id = f"level-test-{lvl_num}"
        existing = db.query(LevelFinalTest).filter(LevelFinalTest.id == test_id).first()
        if not existing:
            l_test = LevelFinalTest(
                id=test_id,
                level_number=lvl_num,
                title=test_meta["title"],
                description=test_meta["description"],
                pass_percentage=test_meta["pass_percentage"],
                time_limit_minutes=test_meta["time_limit_minutes"],
                total_questions=len(test_meta["questions"]),
                xp_reward=250
            )
            db.add(l_test)
            db.flush()

            for idx, q_data in enumerate(test_meta["questions"], start=1):
                q = LevelFinalTestQuestion(
                    level_test_id=test_id,
                    order_index=idx,
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    code_snippet=q_data.get("code_snippet"),
                    options_json=json.dumps(q_data.get("options", [])),
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data.get("explanation"),
                    points=q_data.get("points", 1)
                )
                db.add(q)

    # 2. Periodic Tests
    for p_meta in PERIODIC_TESTS_METADATA:
        p_id = p_meta["id"]
        existing_p = db.query(PeriodicTest).filter(PeriodicTest.id == p_id).first()
        if not existing_p:
            p_test = PeriodicTest(
                id=p_id,
                test_type=p_meta["test_type"],
                period_number=p_meta["period_number"],
                title=p_meta["title"],
                description=p_meta["description"],
                pass_percentage=p_meta["pass_percentage"],
                time_limit_minutes=p_meta["time_limit_minutes"],
                total_questions=len(p_meta["questions"]),
                xp_reward=p_meta["xp_reward"]
            )
            db.add(p_test)
            db.flush()

            for idx, q_data in enumerate(p_meta["questions"], start=1):
                pq = PeriodicTestQuestion(
                    test_id=p_id,
                    order_index=idx,
                    question_text=q_data["question_text"],
                    question_type=q_data["question_type"],
                    code_snippet=q_data.get("code_snippet"),
                    options_json=json.dumps(q_data.get("options", [])),
                    correct_answer=q_data["correct_answer"],
                    explanation=q_data.get("explanation"),
                    points=q_data.get("points", 1)
                )
                db.add(pq)

    db.commit()
    print("Level final tests and periodic tests successfully seeded.")
