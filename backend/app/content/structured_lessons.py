"""
Python Mastery - Structured Educational Lessons System
Comprehensive beginner-to-advanced lessons with expandable subtopics,
real-life analogies, syntax breakdowns, line-by-line explanations,
incorrect vs correct comparisons, and concept check quizzes.
"""

from typing import Dict, Any, List, Optional

STRUCTURED_LESSONS: List[Dict[str, Any]] = [
    {
        "id": "lesson-1",
        "challenge_id": "chal-1",
        "level_number": 1,
        "track_number": 1,
        "track_title": "Python Fundamentals",
        "title": "Python Variables, Strings & Functions",
        "introduction": "Welcome to Python! In this lesson, you will learn the absolute foundational building blocks of programming: how Python remembers data using variables, how text is stored as strings, and how to write reusable functions.",
        "learning_objectives": [
            "Understand what variables are and how Python stores data in memory",
            "Learn Python's strict variable naming conventions and best practices",
            "Master strings and how to format text dynamically using modern f-strings",
            "Define custom functions with inputs and return values"
        ],
        "subtopics": [
            {
                "id": "sub-1-1",
                "title": "1. What is a Variable?",
                "order": 1,
                "explanation": "In computer programming, a variable is like a labeled storage box in a warehouse. When you assign a value to a variable, you place an item into that box and stick a label on it so you can find it later. In Python, you do not need to build the box beforehand; simply giving it a name and a value creates it instantly.",
                "analogy": "Imagine moving into a new home. You pack kitchen plates into a cardboard box and write 'Plates' on the outside. Whenever you need a plate, you look for the box labeled 'Plates' instead of searching the entire house. In Python, `plates = 4` places the number 4 into a labeled box named `plates`.",
                "syntax": {
                    "code": "variable_name = value",
                    "breakdown": [
                        {"part": "variable_name", "meaning": "The unique label you choose to identify your data."},
                        {"part": "=", "meaning": "The assignment operator. It means 'store the right-hand value into the left-hand name'."},
                        {"part": "value", "meaning": "The actual data being saved (a number, word, or collection)."}
                    ]
                },
                "examples": [
                    {
                        "title": "Basic Variable Assignment",
                        "code": "player_name = 'Alex'\nplayer_level = 1\nis_online = True\n\nprint(player_name)\nprint(player_level)",
                        "expected_output": "Alex\n1",
                        "line_by_line": [
                            {"line": "player_name = 'Alex'", "explanation": "Creates a variable named `player_name` and assigns it the text string 'Alex'."},
                            {"line": "player_level = 1", "explanation": "Creates `player_level` and assigns it the integer number 1."},
                            {"line": "is_online = True", "explanation": "Creates a boolean variable indicating active status."},
                            {"line": "print(player_name)", "explanation": "Retrieves the value inside `player_name` ('Alex') and displays it on the screen."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Confusing Assignment (=) with Equality (==)",
                        "incorrect_code": "age == 25  # Throws NameError if age doesn't exist yet",
                        "correct_code": "age = 25   # Correct: assigns 25 to age",
                        "why_it_fails": "A single `=` assigns a value. Double `==` asks a question: 'Are these two things equal?'"
                    }
                ]
            },
            {
                "id": "sub-1-2",
                "title": "2. Variable Naming Rules & Conventions",
                "order": 2,
                "explanation": "Python has strict rules for naming variables. If you violate these rules, Python will refuse to run your code with a SyntaxError. Furthermore, Python developers follow a community style guide called PEP 8: variable names should always be written in snake_case (lowercase words separated by underscores).",
                "analogy": "Think of variable names like legal usernames. A username cannot begin with a number or contain spaces, but underscores and letters are completely valid.",
                "syntax": {
                    "code": "user_score = 100  # Valid snake_case",
                    "breakdown": [
                        {"part": "Must start with", "meaning": "A letter (a-z, A-Z) or an underscore (_). Never a number."},
                        {"part": "Can contain", "meaning": "Letters, numbers, and underscores only. No hyphens (-), spaces, or symbols."},
                        {"part": "Case-sensitive", "meaning": "`score`, `Score`, and `SCORE` are three completely different variables!"}
                    ]
                },
                "examples": [
                    {
                        "title": "Valid vs Invalid Names",
                        "code": "# Valid variable names\ntotal_score = 95\nuser_1 = 'DeepMind'\n_secret_token = 'xyz123'\n\nprint(total_score)",
                        "expected_output": "95",
                        "line_by_line": [
                            {"line": "total_score = 95", "explanation": "Correct snake_case naming."},
                            {"line": "user_1 = 'DeepMind'", "explanation": "Numbers are allowed as long as they are NOT the very first character."},
                            {"line": "_secret_token = 'xyz123'", "explanation": "Leading underscores are legal and commonly denote internal variables."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Starting a variable name with a number or using spaces",
                        "incorrect_code": "1st_place = 'Gold'\nuser name = 'Sam'",
                        "correct_code": "first_place = 'Gold'\nuser_name = 'Sam'",
                        "why_it_fails": "Python parser cannot distinguish variable names starting with digits from raw numeric literals."
                    }
                ]
            },
            {
                "id": "sub-1-3",
                "title": "3. Understanding Strings & Modern F-Strings",
                "order": 3,
                "explanation": "A string is any sequence of text enclosed in single quotes `'...'` or double quotes `\"...\"`. Modern Python 3.6+ introduced formatted string literals (f-strings). By prefixing a string with the letter `f`, you can embed variables and calculations directly inside curly braces `{}`.",
                "analogy": "Think of a fill-in-the-blank certificate: 'Congratulations, {NAME}! You achieved level {LEVEL}!'. An f-string automatically fills in those blanks dynamically.",
                "syntax": {
                    "code": 'f"Hello, {variable_name}!"',
                    "breakdown": [
                        {"part": "f", "meaning": "Tells Python to treat this string as a template with expressions to evaluate."},
                        {"part": '""', "meaning": "Delimits the text boundary."},
                        {"part": "{variable}", "meaning": "Any valid Python variable or expression evaluated and converted into text."}
                    ]
                },
                "examples": [
                    {
                        "title": "Dynamic Greeting with F-Strings",
                        "code": "name = 'Ada'\nrole = 'Engineer'\ngreeting = f\"Hello, {name}! Welcome, {role}.\"\n\nprint(greeting)",
                        "expected_output": "Hello, Ada! Welcome, Engineer.",
                        "line_by_line": [
                            {"line": "name = 'Ada'", "explanation": "Sets string variable `name`."},
                            {"line": "role = 'Engineer'", "explanation": "Sets string variable `role`."},
                            {"line": "greeting = f\"...\"", "explanation": "Python substitutes {name} with 'Ada' and {role} with 'Engineer'."},
                            {"line": "print(greeting)", "explanation": "Prints the assembled sentence."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Forgetting the 'f' prefix in front of the quotes",
                        "incorrect_code": 'name = "Zara"\nmsg = "Hello, {name}!"  # Prints literally: Hello, {name}!',
                        "correct_code": 'name = "Zara"\nmsg = f"Hello, {name}!"  # Correct: Hello, Zara!',
                        "why_it_fails": "Without the 'f' prefix, Python does not evaluate the curly braces as variables."
                    }
                ]
            },
            {
                "id": "sub-1-4",
                "title": "4. Writing Functions and the Return Statement",
                "order": 4,
                "explanation": "A function is a packaged recipe that takes zero or more inputs (called parameters or arguments), performs actions, and sends back an output using the `return` keyword. Using `print()` prints text to the screen, but only `return` passes data back to the program so other code can use it.",
                "analogy": "Imagine a blender. You put in fruits (inputs/arguments), press blend (internal function logic), and pour out a smoothie (the return value). If the blender only displayed a picture of a smoothie on an LCD screen (print), you wouldn't actually have a smoothie to drink!",
                "syntax": {
                    "code": "def function_name(param1: str) -> str:\n    result = f\"Hello, {param1}\"\n    return result",
                    "breakdown": [
                        {"part": "def", "meaning": "Keyword stating: 'We are defining a new function here'."},
                        {"part": "function_name", "meaning": "The identifier used to call this function."},
                        {"part": "(param1: str)", "meaning": "Input parameters the caller must provide."},
                        {"part": ":", "meaning": "Colon required at the end of the def line; starts the indented code block."},
                        {"part": "return", "meaning": "Sends the final output value back to the caller."}
                    ]
                },
                "examples": [
                    {
                        "title": "Creating a Personalized Greeting Function",
                        "code": "def greet(name: str) -> str:\n    return f\"Hello, {name}!\"\n\nmessage = greet('Maya')\nprint(message)",
                        "expected_output": "Hello, Maya!",
                        "line_by_line": [
                            {"line": "def greet(name: str) -> str:", "explanation": "Defines function `greet` taking one argument `name`."},
                            {"line": "return f\"Hello, {name}!\"", "explanation": "Constructs the greeting and sends it back to the caller."},
                            {"line": "message = greet('Maya')", "explanation": "Calls `greet('Maya')` and saves the returned value into `message`."},
                            {"line": "print(message)", "explanation": "Displays 'Hello, Maya!'."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Using print() instead of return in a function",
                        "incorrect_code": "def greet(name):\n    print(f\"Hello, {name}!\")\n\nval = greet('Sam')  # val is None!",
                        "correct_code": "def greet(name):\n    return f\"Hello, {name}!\"\n\nval = greet('Sam')  # val is 'Hello, Sam!'",
                        "why_it_fails": "If a function doesn't execute a `return` statement, Python automatically returns `None`."
                    }
                ]
            }
        ],
        "quiz": [
            {
                "id": "q-1-1",
                "question": "Which of the following is a valid, PEP 8 compliant Python variable name?",
                "options": [
                    "2nd_user",
                    "user_score",
                    "user-score",
                    "class"
                ],
                "correct_index": 1,
                "explanation": "`user_score` is valid snake_case. `2nd_user` is invalid because it starts with a number; `user-score` has a hyphen (subtraction symbol); and `class` is a reserved Python keyword."
            },
            {
                "id": "q-1-2",
                "question": "What will `f'Welcome, {name}!'` output if `name = 'Jordan'`?",
                "options": [
                    "Welcome, {name}!",
                    "Welcome, Jordan!",
                    "Welcome, name!",
                    "SyntaxError"
                ],
                "correct_index": 1,
                "explanation": "Because the string is prefixed with 'f', Python replaces `{name}` with the value inside the `name` variable ('Jordan')."
            },
            {
                "id": "q-1-3",
                "question": "Why must challenge solutions use `return` instead of `print()` inside functions?",
                "options": [
                    "print() is not allowed in Python",
                    "return terminates the entire computer program",
                    "return sends data back to the testing engine to verify correctness, whereas print() only displays text and returns None",
                    "return is only used for numbers, not strings"
                ],
                "correct_index": 2,
                "explanation": "The automated test engine checks the output value returned by your function. `print()` only outputs characters to stdout, leaving the function output as `None`."
            }
        ],
        "xp_reward": 25
    },
    {
        "id": "lesson-2",
        "challenge_id": "chal-2",
        "level_number": 2,
        "track_number": 1,
        "track_title": "Python Fundamentals",
        "title": "Conditional Logic: Even or Odd Parity",
        "introduction": "In this lesson, you will learn how computers make decisions using conditional statements (if, else), how to test true/false conditions, and how the modulo operator `%` calculates remainders.",
        "learning_objectives": [
            "Understand boolean truth values (True, False) and comparison operators",
            "Master the modulo remainder operator `%`",
            "Write `if` and `else` decision branches",
            "Learn Python's elegant ternary one-line conditional expression"
        ],
        "subtopics": [
            {
                "id": "sub-2-1",
                "title": "1. What is Parity and the Modulo Operator?",
                "order": 1,
                "explanation": "In mathematics, parity refers to whether an integer is even or odd. An even number divides evenly by 2 with no remainder (remainder 0). An odd number leaves a remainder of 1. In Python, the modulo operator `%` calculates the remainder of division.",
                "analogy": "Imagine sharing cookies equally between two friends. If you have 6 cookies, each friend gets 3 and 0 cookies are left over (6 % 2 == 0). If you have 7 cookies, each friend gets 3 and 1 cookie is left over (7 % 2 == 1).",
                "syntax": {
                    "code": "remainder = number % divisor",
                    "breakdown": [
                        {"part": "number", "meaning": "The dividend being divided."},
                        {"part": "%", "meaning": "Modulo operator: returns only the remainder left over after integer division."},
                        {"part": "divisor", "meaning": "The number you are dividing by (e.g. 2 for parity)."}
                    ]
                },
                "examples": [
                    {
                        "title": "Checking Remainders",
                        "code": "print(10 % 2)  # 0 (Even)\nprint(11 % 2)  # 1 (Odd)\nprint(14 % 5)  # 4 (Remainder when dividing 14 by 5)",
                        "expected_output": "0\n1\n4",
                        "line_by_line": [
                            {"line": "print(10 % 2)", "explanation": "10 divided by 2 is exactly 5 with remainder 0."},
                            {"line": "print(11 % 2)", "explanation": "11 divided by 2 is 5 with remainder 1."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Confusing division (/) with modulo (%)",
                        "incorrect_code": "if n / 2 == 0:  # Division gives quotient 5.0, not remainder!",
                        "correct_code": "if n % 2 == 0:  # Correct: checks if remainder is 0",
                        "why_it_fails": "`10 / 2` evaluates to `5.0`. `10 % 2` evaluates to `0`."
                    }
                ]
            },
            {
                "id": "sub-2-2",
                "title": "2. Conditional Branches: if and else",
                "order": 2,
                "explanation": "An `if` statement evaluates a condition. If the condition is True, the indented block below it runs. If False, the `else` block runs instead.",
                "analogy": "Like a fork in the road: 'If the traffic light is green, proceed; Else, stop.'",
                "syntax": {
                    "code": "if condition:\n    # runs when True\nelse:\n    # runs when False",
                    "breakdown": [
                        {"part": "if", "meaning": "Evaluates boolean condition."},
                        {"part": ":", "meaning": "Required colon after if and else."},
                        {"part": "Indentation (4 spaces)", "meaning": "Python uses indentation to define code blocks."}
                    ]
                },
                "examples": [
                    {
                        "title": "Checking Parity with If-Else",
                        "code": "def check_parity(n: int) -> str:\n    if n % 2 == 0:\n        return 'Even'\n    else:\n        return 'Odd'\n\nprint(check_parity(42))\nprint(check_parity(7))",
                        "expected_output": "Even\nOdd",
                        "line_by_line": [
                            {"line": "if n % 2 == 0:", "explanation": "Tests if remainder of n divided by 2 is 0."},
                            {"line": "return 'Even'", "explanation": "Executes only when n is even."},
                            {"line": "return 'Odd'", "explanation": "Executes for all other numbers."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Forgetting the colon or incorrect capitalization of 'Even' / 'Odd'",
                        "incorrect_code": "if n % 2 == 0\n    return 'even'",
                        "correct_code": "if n % 2 == 0:\n    return 'Even'",
                        "why_it_fails": "Colons are required syntax in Python, and string test cases are strictly case-sensitive."
                    }
                ]
            }
        ],
        "quiz": [
            {
                "id": "q-2-1",
                "question": "What is the value of `15 % 4` in Python?",
                "options": [
                    "3",
                    "3.75",
                    "0",
                    "4"
                ],
                "correct_index": 0,
                "explanation": "4 goes into 15 three times (4 * 3 = 12), leaving a remainder of 3. So `15 % 4 == 3`."
            },
            {
                "id": "q-2-2",
                "question": "Which single-line expression returns 'Even' when `n` is divisible by 2, and 'Odd' otherwise?",
                "options": [
                    "'Even' if n % 2 == 0 else 'Odd'",
                    "if n % 2 == 0 return 'Even' else 'Odd'",
                    "n % 2 == 0 ? 'Even' : 'Odd'",
                    "return 'Even' or 'Odd'"
                ],
                "correct_index": 0,
                "explanation": "Python's ternary expression syntax is `<value_if_true> if <condition> else <value_if_false>`."
            }
        ],
        "xp_reward": 25
    },
    {
        "id": "lesson-3",
        "challenge_id": "chal-3",
        "level_number": 3,
        "track_number": 1,
        "track_title": "Python Fundamentals",
        "title": "Loops & Accumulators: Sum of Multiples",
        "introduction": "In this lesson, you will learn how to automate repetitive tasks using loops (`for` loops) and how to accumulate running totals using the `range()` generator and addition operators.",
        "learning_objectives": [
            "Understand how loops iterate over numbers and sequences",
            "Master the `range(start, stop, step)` built-in function",
            "Use accumulator variables to compute running sums",
            "Discover Python's built-in `sum()` function"
        ],
        "subtopics": [
            {
                "id": "sub-3-1",
                "title": "1. What is the range() Function?",
                "order": 1,
                "explanation": "`range()` generates a sequence of numbers. It accepts three parameters: `range(start, stop, step)`. Note that `stop` is exclusive — Python stops right before reaching the stop number.",
                "analogy": "Think of setting a countdown or stepping stones: `range(0, 10, 2)` means start at stone 0, hop forward 2 stones at a time, and stop BEFORE reaching stone 10 (producing 0, 2, 4, 6, 8).",
                "syntax": {
                    "code": "range(start, stop, step)",
                    "breakdown": [
                        {"part": "start", "meaning": "Starting integer (inclusive, default 0)."},
                        {"part": "stop", "meaning": "Stopping threshold (exclusive — not included!)."},
                        {"part": "step", "meaning": "Interval increment between each step (e.g. 3 for multiples of 3)."}
                    ]
                },
                "examples": [
                    {
                        "title": "Generating Multiples with range()",
                        "code": "# Multiples of 3 up to (not including) 15\nmultiples = list(range(3, 15, 3))\nprint(multiples)",
                        "expected_output": "[3, 6, 9, 12]",
                        "line_by_line": [
                            {"line": "range(3, 15, 3)", "explanation": "Generates 3, 6, 9, 12. 15 is excluded."},
                            {"line": "list(...)", "explanation": "Converts the range generator into a concrete list."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Forgetting that the stop boundary is exclusive",
                        "incorrect_code": "range(1, 5)  # Produces 1, 2, 3, 4 (5 is missing!)",
                        "correct_code": "range(1, 6)  # Produces 1, 2, 3, 4, 5",
                        "why_it_fails": "To include number N, your stop argument must be N + 1."
                    }
                ]
            },
            {
                "id": "sub-3-2",
                "title": "2. Accumulating a Sum in a Loop",
                "order": 2,
                "explanation": "An accumulator is a variable initialized before a loop (usually to 0) that gets incrementally increased with each iteration using the `+=` operator.",
                "analogy": "Like a piggy bank: start with 0 coins. Every time you find a multiple, you drop it into the piggy bank until you reach the limit.",
                "syntax": {
                    "code": "total = 0\nfor x in iterable:\n    total += x",
                    "breakdown": [
                        {"part": "total = 0", "meaning": "Initialize accumulator to zero."},
                        {"part": "+=", "meaning": "Shorthand for `total = total + x`."}
                    ]
                },
                "examples": [
                    {
                        "title": "Summing Multiples",
                        "code": "def sum_multiples(limit: int, factor: int) -> int:\n    total = 0\n    for num in range(factor, limit, factor):\n        total += num\n    return total\n\nprint(sum_multiples(10, 2)) # 2 + 4 + 6 + 8 = 20",
                        "expected_output": "20",
                        "line_by_line": [
                            {"line": "total = 0", "explanation": "Initializes running total."},
                            {"line": "for num in range(factor, limit, factor):", "explanation": "Steps through multiples of factor strictly below limit."},
                            {"line": "total += num", "explanation": "Adds each multiple to total."},
                            {"line": "return total", "explanation": "Returns accumulated sum."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Resetting the total inside the loop body",
                        "incorrect_code": "for num in range(10):\n    total = 0  # Resets to 0 every time!\n    total += num",
                        "correct_code": "total = 0\nfor num in range(10):\n    total += num",
                        "why_it_fails": "If you initialize inside the loop, the variable resets on every pass."
                    }
                ]
            }
        ],
        "quiz": [
            {
                "id": "q-3-1",
                "question": "What does `list(range(5, 20, 5))` evaluate to?",
                "options": [
                    "[5, 10, 15, 20]",
                    "[5, 10, 15]",
                    "[0, 5, 10, 15]",
                    "[5, 20]"
                ],
                "correct_index": 1,
                "explanation": "The stop value (20) is exclusive, so the sequence terminates after 15."
            }
        ],
        "xp_reward": 25
    },
    {
        "id": "lesson-11",
        "challenge_id": "chal-11",
        "level_number": 11,
        "track_number": 2,
        "track_title": "Data Structures Deep Dive",
        "title": "Lists & Deduplication Preserving Order",
        "introduction": "In Track 2, you step into Python Data Structures. In this lesson, you will master Python Lists and Sets, and learn how to remove duplicate items from a list while keeping the original order intact.",
        "learning_objectives": [
            "Understand differences between Lists (ordered, duplicate-friendly) and Sets (unordered, unique-only)",
            "Learn why naive `list(set(items))` scrambles ordering",
            "Implement order-preserving deduplication using a tracking set",
            "Achieve optimal O(n) time complexity"
        ],
        "subtopics": [
            {
                "id": "sub-11-1",
                "title": "1. Lists vs Sets in Python",
                "order": 1,
                "explanation": "A Python List maintains exact insertion order and permits duplicates (`[1, 2, 2, 3]`). A Set stores only unique values and has O(1) instant lookup time (`x in seen_set`). Converting a list directly to a set and back removes duplicates, BUT it destroys the original ordering!",
                "analogy": "Imagine a queue of people at a ticket counter. A list remembers who arrived first, second, and third. A set only cares about who is in the room, disregarding who arrived first.",
                "syntax": {
                    "code": "seen = set()\nresult = []\nfor item in items:\n    if item not in seen:\n        seen.add(item)\n        result.append(item)",
                    "breakdown": [
                        {"part": "seen = set()", "meaning": "A hash set providing O(1) instant duplicate checks."},
                        {"part": "item not in seen", "meaning": "Checks if we have already encountered this item in O(1) time."},
                        {"part": "seen.add(item)", "meaning": "Remembers the item for subsequent iterations."},
                        {"part": "result.append(item)", "meaning": "Appends the first occurrence in order."}
                    ]
                },
                "examples": [
                    {
                        "title": "Order-Preserving Deduplication",
                        "code": "def remove_duplicates(items: list) -> list:\n    seen = set()\n    result = []\n    for x in items:\n        if x not in seen:\n            seen.add(x)\n            result.append(x)\n    return result\n\nprint(remove_duplicates([3, 1, 2, 1, 3, 4]))",
                        "expected_output": "[3, 1, 2, 4]",
                        "line_by_line": [
                            {"line": "seen = set()", "explanation": "Initializes empty tracking set."},
                            {"line": "result = []", "explanation": "Initializes output list preserving order."},
                            {"line": "if x not in seen:", "explanation": "Tests uniqueness in O(1) time."},
                            {"line": "return result", "explanation": "Returns [3, 1, 2, 4] with original order intact."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Using list(set(items)) when order matters",
                        "incorrect_code": "return list(set(items))  # Scrambles order!",
                        "correct_code": "seen = set()\nreturn [x for x in items if not (x in seen or seen.add(x))]",
                        "why_it_fails": "Sets are hashed collections; converting to set does not preserve element positions."
                    }
                ]
            }
        ],
        "quiz": [
            {
                "id": "q-11-1",
                "question": "What is the average time complexity of checking `x in my_set` compared to `x in my_list`?",
                "options": [
                    "Set is O(1) constant time, List is O(n) linear search",
                    "List is faster than Set",
                    "Both are O(n) linear time",
                    "Set is O(log n)"
                ],
                "correct_index": 0,
                "explanation": "Sets use hash tables, allowing Python to verify presence in average O(1) time without scanning all elements."
            }
        ],
        "xp_reward": 25
    },
    {
        "id": "lesson-41",
        "challenge_id": "chal-41",
        "level_number": 41,
        "track_number": 5,
        "track_title": "Object-Oriented Programming",
        "title": "Classes, Constructors & Encapsulation",
        "introduction": "In Track 5, you master Object-Oriented Programming (OOP). In this lesson, you will learn how to create your own custom types using the `class` keyword, instantiate objects, and encapsulate internal state.",
        "learning_objectives": [
            "Understand classes as blueprints and objects as concrete instances",
            "Master the `__init__` constructor method",
            "Understand what the `self` parameter represents",
            "Encapsulate state and enforce business rules with methods"
        ],
        "subtopics": [
            {
                "id": "sub-41-1",
                "title": "1. What is a Class and Object?",
                "order": 1,
                "explanation": "A class is a blueprint for creating objects. An object is a concrete instance of that class possessing attributes (data/state) and methods (functions/behavior).",
                "analogy": "A class is like an architectural blueprint for a house. The blueprint itself is not a physical house; you use the blueprint to build multiple concrete houses, each with its own address and painted walls.",
                "syntax": {
                    "code": "class BankAccount:\n    def __init__(self, owner: str, balance: float = 0.0):\n        self.owner = owner\n        self.balance = balance\n\n    def deposit(self, amount: float) -> float:\n        self.balance += amount\n        return self.balance",
                    "breakdown": [
                        {"part": "class BankAccount:", "meaning": "Declares a new class type in PascalCase."},
                        {"part": "def __init__(self, ...):", "meaning": "The constructor method called whenever `BankAccount(...)` is instantiated."},
                        {"part": "self.balance", "meaning": "Instance attribute stored on this specific instance."}
                    ]
                },
                "examples": [
                    {
                        "title": "Creating and Using BankAccount",
                        "code": "account = BankAccount('Alice', 100.0)\naccount.deposit(50.0)\nprint(account.balance)",
                        "expected_output": "150.0",
                        "line_by_line": [
                            {"line": "account = BankAccount('Alice', 100.0)", "explanation": "Calls `__init__`, initializing owner='Alice' and balance=100.0."},
                            {"line": "account.deposit(50.0)", "explanation": "Passes `account` as `self` and increases balance by 50.0."},
                            {"line": "print(account.balance)", "explanation": "Prints current balance (150.0)."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Forgetting the self parameter in method definitions",
                        "incorrect_code": "class User:\n    def get_name():  # TypeError: get_name() takes 0 positional arguments but 1 was given\n        return 'User'",
                        "correct_code": "class User:\n    def get_name(self):\n        return 'User'",
                        "why_it_fails": "Python automatically passes the calling instance as the first argument to instance methods."
                    }
                ]
            }
        ],
        "quiz": [
            {
                "id": "q-41-1",
                "question": "What is the purpose of `__init__` in a Python class?",
                "options": [
                    "To delete the object from memory",
                    "To initialize instance attributes when an object is created",
                    "To print the class definition",
                    "To convert the class into a string"
                ],
                "correct_index": 1,
                "explanation": "`__init__` is the constructor method in Python. It runs automatically when you instantiate a class to set up initial attributes."
            }
        ],
        "xp_reward": 25
    }
]


def get_structured_lesson_by_challenge(challenge_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves structured lesson by challenge_id, or creates an automated one for that track."""
    for lesson in STRUCTURED_LESSONS:
        if lesson["challenge_id"] == challenge_id:
            return lesson

    # Fallback to automated structured lesson based on challenge number
    from backend.app.content.lessons import TRACK_MASTER_LESSONS
    import re
    
    num_match = re.search(r"\d+", challenge_id)
    chal_num = int(num_match.group(0)) if num_match else 1
    track_num = ((chal_num - 1) // 10) + 1
    track_guide = TRACK_MASTER_LESSONS.get(track_num, TRACK_MASTER_LESSONS[1])

    return {
        "id": f"lesson-{chal_num}",
        "challenge_id": challenge_id,
        "level_number": chal_num,
        "track_number": track_num,
        "track_title": track_guide["title"],
        "title": f"Mastery Lesson: Level {chal_num}",
        "introduction": f"In this lesson, you explore the core concepts of Track {track_num}: {track_guide['title']}. Study the syntax, code examples, and common pitfalls before attempting Challenge {chal_num}.",
        "learning_objectives": [
            f"Understand the mechanics of {track_guide['title']}",
            "Study real-world code patterns and syntax rules",
            "Examine common traps and anti-patterns to avoid in your code",
            "Validate your understanding through concept check quizzes"
        ],
        "subtopics": [
            {
                "id": f"sub-{chal_num}-{idx+1}",
                "title": concept["name"],
                "order": idx + 1,
                "explanation": concept["explanation"],
                "analogy": f"In software engineering, {concept['name']} acts as an essential pattern that makes your code predictable, modular, and maintainable.",
                "syntax": {
                    "code": concept.get("example_code", "").split("\n")[0] if concept.get("example_code") else "# Python Syntax",
                    "breakdown": [
                        {"part": "Syntax Rule", "meaning": "Follow standard Python formatting, typing, and naming conventions."},
                        {"part": "Best Practice", "meaning": "Keep functions focused on a single responsibility with explicit return values."}
                    ]
                },
                "examples": [
                    {
                        "title": f"Demonstration: {concept['name']}",
                        "code": concept["example_code"],
                        "expected_output": "Executed successfully",
                        "line_by_line": [
                            {"line": "Code Logic", "explanation": "Applies the pattern with idiomatic Python syntax."}
                        ]
                    }
                ],
                "common_mistakes": [
                    {
                        "description": "Common syntax or logic trap",
                        "incorrect_code": "# Unoptimized or buggy pattern",
                        "correct_code": "# Clean, idiomatic implementation",
                        "why_it_fails": "Always verify argument types, edge cases (empty inputs, zero values), and return statements."
                    }
                ]
            }
            for idx, concept in enumerate(track_guide["core_concepts"])
        ],
        "quiz": [
            {
                "id": f"q-{chal_num}-1",
                "question": f"Which of the following is true regarding {track_guide['title']} in Python?",
                "options": [
                    "It is supported natively in Python with standard syntax and conventions",
                    "It is deprecated in modern Python versions",
                    "It requires third-party C++ libraries to run",
                    "It cannot be tested automatically"
                ],
                "correct_index": 0,
                "explanation": "Python provides native, idiomatic syntax and standard library support for this feature."
            },
            {
                "id": f"q-{chal_num}-2",
                "question": "What is the key benefit of following idiomatic Python conventions?",
                "options": [
                    "Code is more readable, maintainable, and less prone to runtime bugs",
                    "Code runs 1000x faster than assembly",
                    "It eliminates the need to test edge cases",
                    "It automatically writes solutions without programmer input"
                ],
                "correct_index": 0,
                "explanation": "Idiomatic Python (The Zen of Python) emphasizes readability, clarity, and predictable behavior."
            }
        ],
        "xp_reward": 25
    }


def get_structured_lesson_by_id(lesson_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves structured lesson by its lesson_id (e.g., 'lesson-1', 'lesson-25')."""
    for lesson in STRUCTURED_LESSONS:
        if lesson["id"] == lesson_id:
            return lesson

    import re
    num_match = re.search(r"\d+", lesson_id)
    if num_match:
        chal_num = int(num_match.group(0))
        return get_structured_lesson_by_challenge(f"chal-{chal_num}")
    return None


def list_all_structured_lessons() -> List[Dict[str, Any]]:
    """Returns summaries of structured lessons for all 100 challenges."""
    summaries = []
    for chal_num in range(1, 101):
        lesson = get_structured_lesson_by_challenge(f"chal-{chal_num}")
        if lesson:
            summaries.append({
                "id": lesson["id"],
                "challenge_id": lesson["challenge_id"],
                "level_number": lesson["level_number"],
                "track_number": lesson["track_number"],
                "track_title": lesson["track_title"],
                "title": lesson["title"],
                "subtopics_count": len(lesson.get("subtopics", [])),
                "quiz_questions_count": len(lesson.get("quiz", [])),
                "xp_reward": lesson.get("xp_reward", 25)
            })
    return summaries
