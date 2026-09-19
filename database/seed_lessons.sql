-- =========================================================
-- Python Mastery - Seed Curriculum Data (Levels 1 to 5)
-- =========================================================

-- Badges
INSERT INTO public.badges (code, name, description, icon, xp_bonus) VALUES
('first_blood', 'First Spark', 'Ran your first Python program successfully.', '⚡', 50),
('level1_master', 'Syntax Initiate', 'Completed Level 1: Variables & Data Types.', '🌱', 100),
('logic_lord', 'Logic Master', 'Conquered Level 2: Conditional Statements.', '🔮', 150),
('loop_luminary', 'Loop Luminary', 'Mastered Level 3: Loops & Iterations.', '🔁', 200),
('function_guru', 'Architect of Functions', 'Completed Level 4: Functions & Scope.', '⚙️', 250),
('collection_captain', 'Data Commander', 'Completed Level 5: Lists & Dictionaries.', '🏆', 300)
ON CONFLICT (code) DO NOTHING;

-- Modules (Levels 1 to 5)
INSERT INTO public.modules (id, slug, title, description, level_number, order_index) VALUES
('11111111-1111-1111-1111-111111111111', 'level-1-basics', 'Level 1: Python Fundamentals', 'Variables, data types, string formatting, and basic operations.', 1, 1),
('22222222-2222-2222-2222-222222222222', 'level-2-control-flow', 'Level 2: Decision Making', 'If-elif-else logic, comparison operators, and boolean algebra.', 2, 2),
('33333333-3333-3333-3333-333333333333', 'level-3-loops', 'Level 3: Loops & Repetition', 'For loops, while loops, break, continue, and ranges.', 3, 3),
('44444444-4444-4444-4444-444444444444', 'level-4-functions', 'Level 4: Reusable Functions', 'Defining functions, arguments, return values, docstrings, and scope.', 4, 4),
('55555555-5555-5555-5555-555555555555', 'level-5-data-structures', 'Level 5: Collections & Maps', 'Lists, tuples, dictionaries, sets, and comprehension patterns.', 5, 5)
ON CONFLICT (slug) DO NOTHING;

-- Lessons
INSERT INTO public.lessons (id, module_id, slug, title, concept_markdown, order_index, xp_reward) VALUES
('a1111111-0000-0000-0000-000000000001', '11111111-1111-1111-1111-111111111111', 'hello-python', 'Variables and Output', '# Welcome to Python!\nIn Python, variables store values without needing type declarations.\n\n```python\nname = "Ada Lovelace"\nage = 36\nprint(f"Hello, my name is {name} and I am {age} years old.")\n```', 1, 25),
('b2222222-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222', 'conditional-branching', 'If, Elif, and Else', '# Branching Logic\nControl execution flow with `if`, `elif`, and `else`:\n\n```python\nscore = 85\nif score >= 90:\n    grade = "A"\nelif score >= 80:\n    grade = "B"\nelse:\n    grade = "C"\n```', 1, 30),
('c3333333-0000-0000-0000-000000000001', '33333333-3333-3333-3333-333333333333', 'for-loops', 'For Loops & Accumulation', '# Loops in Python\nIterate over sequences with `for ... in`:\n\n```python\ntotal = 0\nfor i in range(1, 6):\n    total += i\nprint(total)  # 15\n```', 1, 35),
('d4444444-0000-0000-0000-000000000001', '44444444-4444-4444-4444-444444444444', 'function-definitions', 'Writing Clean Functions', '# Functions\nEncapsulate reusable logic:\n\n```python\ndef calculate_discount(price, percent):\n    return price * (1 - percent / 100)\n```', 1, 40),
('e5555555-0000-0000-0000-000000000001', '55555555-5555-5555-5555-555555555555', 'dictionary-basics', 'Dictionaries & Hash Maps', '# Dictionaries\nStore key-value pairs for fast lookup:\n\n```python\nstats = {"hp": 100, "mana": 50}\nstats["gold"] = 250\n```', 1, 50)
ON CONFLICT (slug) DO NOTHING;

-- Challenges
INSERT INTO public.challenges (id, lesson_id, slug, title, instructions, starter_code, solution_code, entry_function_name, test_cases, hints, xp_reward) VALUES
(
    'ca111111-0000-0000-0000-000000000001',
    'a1111111-0000-0000-0000-000000000001',
    'challenge-greet',
    'Challenge: Personalized Greeting',
    'Write a function `greet(name: str) -> str` that returns `"Hello, " + name + "!"` or using f-strings `f"Hello, {name}!"`.',
    'def greet(name: str) -> str:\n    # Return a greeting string for the given name\n    pass\n',
    'def greet(name: str) -> str:\n    return f"Hello, {name}!"\n',
    'greet',
    '[
        {"input": ["Alice"], "expected": "Hello, Alice!", "is_hidden": false, "description": "Greeting Alice"},
        {"input": ["Bob"], "expected": "Hello, Bob!", "is_hidden": false, "description": "Greeting Bob"},
        {"input": ["Pythonista"], "expected": "Hello, Pythonista!", "is_hidden": true, "description": "Greeting Pythonista"}
    ]'::jsonb,
    '[
        "Remember to use the `return` keyword instead of `print()`.",
        "You can use an f-string: `f\"Hello, {name}!\"`."
    ]'::jsonb,
    50
),
(
    'cb222222-0000-0000-0000-000000000001',
    'b2222222-0000-0000-0000-000000000001',
    'challenge-even-or-odd',
    'Challenge: Even or Odd',
    'Write a function `check_parity(n: int) -> str` that returns `"Even"` if the number is even, and `"Odd"` if the number is odd.',
    'def check_parity(n: int) -> str:\n    # Return "Even" or "Odd"\n    pass\n',
    'def check_parity(n: int) -> str:\n    return "Even" if n % 2 == 0 else "Odd"\n',
    'check_parity',
    '[
        {"input": [4], "expected": "Even", "is_hidden": false, "description": "4 is Even"},
        {"input": [7], "expected": "Odd", "is_hidden": false, "description": "7 is Odd"},
        {"input": [0], "expected": "Even", "is_hidden": true, "description": "0 is Even"},
        {"input": [-3], "expected": "Odd", "is_hidden": true, "description": "Negative numbers work too"}
    ]'::jsonb,
    '[
        "Use the modulo operator `%`. If `n % 2 == 0`, the number has no remainder when divided by 2.",
        "Make sure your return string has exact capitalization: \"Even\" and \"Odd\"."
    ]'::jsonb,
    60
),
(
    'cc333333-0000-0000-0000-000000000001',
    'c3333333-0000-0000-0000-000000000001',
    'challenge-sum-range',
    'Challenge: Sum of Multiples',
    'Write a function `sum_multiples(limit: int, factor: int) -> int` that returns the sum of all positive integers less than or equal to `limit` that are divisible by `factor`.',
    'def sum_multiples(limit: int, factor: int) -> int:\n    # Calculate sum of multiples\n    pass\n',
    'def sum_multiples(limit: int, factor: int) -> int:\n    return sum(i for i in range(factor, limit + 1, factor))\n',
    'sum_multiples',
    '[
        {"input": [10, 3], "expected": 18, "is_hidden": false, "description": "Multiples of 3 up to 10: 3+6+9 = 18"},
        {"input": [20, 5], "expected": 50, "is_hidden": false, "description": "Multiples of 5 up to 20: 5+10+15+20 = 50"},
        {"input": [5, 10], "expected": 0, "is_hidden": true, "description": "No multiples under limit"}
    ]'::jsonb,
    '[
        "Use a `for` loop with `range(1, limit + 1)` and check `i % factor == 0`.",
        "Alternatively, `range(factor, limit + 1, factor)` automatically steps by the factor!"
    ]'::jsonb,
    75
),
(
    'cd444444-0000-0000-0000-000000000001',
    'd4444444-0000-0000-0000-000000000001',
    'challenge-palindrome',
    'Challenge: Palindrome Checker',
    'Write a function `is_palindrome(text: str) -> bool` that returns `True` if the string is a palindrome (ignoring spaces and case), and `False` otherwise.',
    'def is_palindrome(text: str) -> bool:\n    # Return True if text is a palindrome\n    pass\n',
    'def is_palindrome(text: str) -> bool:\n    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())\n    return cleaned == cleaned[::-1]\n',
    'is_palindrome',
    '[
        {"input": ["racecar"], "expected": true, "is_hidden": false, "description": "racecar is a palindrome"},
        {"input": ["A man a plan a canal Panama"], "expected": true, "is_hidden": false, "description": "Ignores case and spaces"},
        {"input": ["python"], "expected": false, "is_hidden": false, "description": "python is not a palindrome"},
        {"input": ["Was it a car or a cat I saw?"], "expected": true, "is_hidden": true, "description": "Sentence with punctuation"}
    ]'::jsonb,
    '[
        "First normalize the string by lowercasing it and keeping only alphanumeric characters (`char.isalnum()`).",
        "Python strings can be reversed using slicing: `cleaned[::-1]`."
    ]'::jsonb,
    90
),
(
    'ce555555-0000-0000-0000-000000000001',
    'e5555555-0000-0000-0000-000000000001',
    'challenge-word-frequency',
    'Challenge: Word Frequency Counter',
    'Write a function `count_frequencies(words: list[str]) -> dict[str, int]` that takes a list of words and returns a dictionary mapping each word to how many times it appeared in the list.',
    'def count_frequencies(words: list[str]) -> dict[str, int]:\n    # Count occurrences of each word\n    pass\n',
    'def count_frequencies(words: list[str]) -> dict[str, int]:\n    freq = {}\n    for w in words:\n        freq[w] = freq.get(w, 0) + 1\n    return freq\n',
    'count_frequencies',
    '[
        {"input": [["apple", "banana", "apple"]], "expected": {"apple": 2, "banana": 1}, "is_hidden": false, "description": "Simple list with repeats"},
        {"input": [["cat", "dog", "bird"]], "expected": {"cat": 1, "dog": 1, "bird": 1}, "is_hidden": false, "description": "All unique"},
        {"input": [[]], "expected": {}, "is_hidden": true, "description": "Empty list returns empty dict"}
    ]'::jsonb,
    '[
        "Initialize an empty dictionary: `freq = {}`.",
        "Iterate through the list and use `dict.get(word, 0) + 1` to increment the count."
    ]'::jsonb,
    100
)
ON CONFLICT (slug) DO NOTHING;
