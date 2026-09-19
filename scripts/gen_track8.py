import json

challenges = []

def add_chal(cid, idx, mod, slug, title, diff, inst, starter, sol, func, tests, hints, xp=110):
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

# --- TRACK 8: Text Processing & String Manipulation (71-80) ---
add_chal("chal-71", 71, 8, "challenge-caesar-cipher", "Caesar Cipher Encryption", "medium",
         "Write `caesar_cipher(text: str, shift: int) -> str` shifting ASCII letters by shift positions (preserving case, ignoring non-letters).",
         "def caesar_cipher(text: str, shift: int) -> str:\n    pass\n",
         "def caesar_cipher(text: str, shift: int) -> str:\n    res = []\n    for ch in text:\n        if 'a' <= ch <= 'z':\n            res.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))\n        elif 'A' <= ch <= 'Z':\n            res.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))\n        else:\n            res.append(ch)\n    return ''.join(res)\n",
         "caesar_cipher",
         [{"input": ["abc", 3], "expected": "def", "description": "Shift 3", "is_hidden": False},
          {"input": ["Hello, World!", 1], "expected": "Ifmmp, Xpsme!", "description": "Preserve punctuation", "is_hidden": False},
          {"input": ["xyz", 2], "expected": "zab", "description": "Wrap around z", "is_hidden": True}],
         ["Use ord() and chr().", "Modulo 26 for wrap-around."], 100)

add_chal("chal-72", 72, 8, "challenge-extract-hashtags", "Extract Hashtags from Text", "easy",
         "Write `extract_hashtags(text: str) -> list[str]` extracting all unique lowercase hashtags in order of appearance.",
         "def extract_hashtags(text: str) -> list[str]:\n    pass\n",
         "def extract_hashtags(text: str) -> list[str]:\n    seen = set()\n    res = []\n    for word in text.split():\n        if word.startswith('#') and len(word) > 1:\n            cleaned = ''.join(c.lower() for c in word[1:] if c.isalnum())\n            if cleaned and cleaned not in seen:\n                seen.add(cleaned)\n                res.append(cleaned)\n    return res\n",
         "extract_hashtags",
         [{"input": ["Learning #Python and #Coding in #python!"], "expected": ["python", "coding"], "description": "Duplicate lowercase", "is_hidden": False},
          {"input": ["No tags here"], "expected": [], "description": "No hashtags", "is_hidden": False},
          {"input": ["#AI #ML #DL"], "expected": ["ai", "ml", "dl"], "description": "Multiple tags", "is_hidden": True}],
         ["Split by whitespace.", "Check word.startswith('#')."], 85)

add_chal("chal-73", 73, 8, "challenge-mask-credit-card", "Mask Credit Card Digits", "easy",
         "Write `mask_credit_card(card: str) -> str` keeping first 4 and last 4 characters visible and replacing all middle characters with '*'. If length <= 8, return unchanged.",
         "def mask_credit_card(card: str) -> str:\n    pass\n",
         "def mask_credit_card(card: str) -> str:\n    if len(card) <= 8:\n        return card\n    return card[:4] + ('*' * (len(card) - 8)) + card[-4:]\n",
         "mask_credit_card",
         [{"input": ["1234567812345678"], "expected": "1234********5678", "description": "16-digit card", "is_hidden": False},
          {"input": ["12345678"], "expected": "12345678", "description": "Length <= 8 returns card", "is_hidden": False},
          {"input": ["4111222233334444"], "expected": "4111********4444", "description": "Another 16-digit", "is_hidden": True}],
         ["Slice card[:4] + ('*' * (len - 8)) + card[-4:]."], 85)

add_chal("chal-74", 74, 8, "challenge-count-letters", "Count Vowels and Consonants", "easy",
         "Write `count_letters(s: str) -> dict[str, int]` returning {'vowels': count, 'consonants': count} ignoring non-alphabet characters and case.",
         "def count_letters(s: str) -> dict[str, int]:\n    pass\n",
         "def count_letters(s: str) -> dict[str, int]:\n    vowels = set('aeiou')\n    v_count, c_count = 0, 0\n    for ch in s.lower():\n        if 'a' <= ch <= 'z':\n            if ch in vowels:\n                v_count += 1\n            else:\n                c_count += 1\n    return {'vowels': v_count, 'consonants': c_count}\n",
         "count_letters",
         [{"input": ["Hello World!"], "expected": {"vowels": 3, "consonants": 7}, "description": "Hello World", "is_hidden": False},
          {"input": ["12345"], "expected": {"vowels": 0, "consonants": 0}, "description": "Numbers only", "is_hidden": False},
          {"input": ["Python"], "expected": {"vowels": 1, "consonants": 5}, "description": "Python", "is_hidden": True}],
         ["Check if ch.isalpha().", "Check ch in 'aeiou'."], 80)

add_chal("chal-75", 75, 8, "challenge-format-currency", "Format Numbers as Currency", "easy",
         "Write `format_currency(amount: float) -> str` formatting a float as '$1,234.56' with comma separators and exactly 2 decimal places.",
         "def format_currency(amount: float) -> str:\n    pass\n",
         "def format_currency(amount: float) -> str:\n    return f'${amount:,.2f}'\n",
         "format_currency",
         [{"input": [1234.56], "expected": "$1,234.56", "description": "Thousands separator", "is_hidden": False},
          {"input": [0.0], "expected": "$0.00", "description": "Zero currency", "is_hidden": False},
          {"input": [1000000.5], "expected": "$1,000,000.50", "description": "Million with trailing 0", "is_hidden": True}],
         ["Use format specifier: f'${amount:,.2f}'."], 80)

add_chal("chal-76", 76, 8, "challenge-longest-common-prefix", "Longest Common Prefix", "medium",
         "Write `longest_common_prefix(strs: list[str]) -> str` finding the longest common prefix string amongst a list of strings (or '' if none).",
         "def longest_common_prefix(strs: list[str]) -> str:\n    pass\n",
         "def longest_common_prefix(strs: list[str]) -> str:\n    if not strs:\n        return ''\n    prefix = strs[0]\n    for s in strs[1:]:\n        while not s.startswith(prefix):\n            prefix = prefix[:-1]\n            if not prefix:\n                return ''\n    return prefix\n",
         "longest_common_prefix",
         [{"input": [["flower", "flow", "flight"]], "expected": "fl", "description": "Prefix fl", "is_hidden": False},
          {"input": [["dog", "racecar", "car"]], "expected": "", "description": "No common prefix", "is_hidden": False},
          {"input": [["interspecies", "interstellar", "interstate"]], "expected": "inters", "description": "Long prefix", "is_hidden": True}],
         ["Shorten prefix until all words match."], 105)

add_chal("chal-77", 77, 8, "challenge-to-snake-case", "CamelCase to SnakeCase Converter", "medium",
         "Write `to_snake_case(s: str) -> str` converting 'camelCase' or 'PascalCase' to 'snake_case'.",
         "def to_snake_case(s: str) -> str:\n    pass\n",
         "def to_snake_case(s: str) -> str:\n    res = []\n    for i, c in enumerate(s):\n        if c.isupper():\n            if i != 0 and s[i-1].isalnum() and not s[i-1].isupper():\n                res.append('_')\n            res.append(c.lower())\n        else:\n            res.append(c)\n    return ''.join(res)\n",
         "to_snake_case",
         [{"input": ["camelCase"], "expected": "camel_case", "description": "camelCase", "is_hidden": False},
          {"input": ["PascalCase"], "expected": "pascal_case", "description": "PascalCase", "is_hidden": False},
          {"input": ["simple"], "expected": "simple", "description": "all lowercase", "is_hidden": True}],
         ["Insert '_' before uppercase chars (except at start)."], 95)

add_chal("chal-78", 78, 8, "challenge-normalize-whitespace", "Normalize Whitespace", "easy",
         "Write `normalize_whitespace(s: str) -> str` trimming leading/trailing spaces and collapsing internal consecutive spaces to a single space.",
         "def normalize_whitespace(s: str) -> str:\n    pass\n",
         "def normalize_whitespace(s: str) -> str:\n    return ' '.join(s.split())\n",
         "normalize_whitespace",
         [{"input": ["  hello   world  "], "expected": "hello world", "description": "Trim and collapse", "is_hidden": False},
          {"input": ["\tmultiple \n lines\t"], "expected": "multiple lines", "description": "Tabs and newlines", "is_hidden": False},
          {"input": [""], "expected": "", "description": "Empty string", "is_hidden": True}],
         ["Use ' '.join(s.split())."], 75)

add_chal("chal-79", 79, 8, "challenge-word-wrap", "Word Wrap Text to Width", "medium",
         "Write `word_wrap(text: str, width: int) -> list[str]` breaking text into lines of at most width characters without splitting words.",
         "def word_wrap(text: str, width: int) -> list[str]:\n    pass\n",
         "def word_wrap(text: str, width: int) -> list[str]:\n    words = text.split()\n    if not words:\n        return []\n    lines = []\n    cur_line = []\n    cur_len = 0\n    for w in words:\n        if cur_len + len(w) + (1 if cur_line else 0) <= width:\n            cur_line.append(w)\n            cur_len += len(w) + (1 if len(cur_line) > 1 else 0)\n        else:\n            if cur_line:\n                lines.append(' '.join(cur_line))\n            cur_line = [w]\n            cur_len = len(w)\n    if cur_line:\n        lines.append(' '.join(cur_line))\n    return lines\n",
         "word_wrap",
         [{"input": ["The quick brown fox jumps over lazy dog", 15], "expected": ["The quick brown", "fox jumps over", "lazy dog"], "description": "Wrap at 15", "is_hidden": False},
          {"input": ["hello world", 20], "expected": ["hello world"], "description": "Fits in single line", "is_hidden": False},
          {"input": ["", 10], "expected": [], "description": "Empty string", "is_hidden": True}],
         ["Accumulate words while line length <= width."], 110)

add_chal("chal-80", 80, 8, "challenge-compress-string", "String Compression Threshold", "medium",
         "Write `compress_string(s: str) -> str` compressing repeating characters ('a2b1c5a3'). Return original s if compressed string is not shorter than s.",
         "def compress_string(s: str) -> str:\n    pass\n",
         "def compress_string(s: str) -> str:\n    if not s:\n        return s\n    res = []\n    cur = s[0]\n    cnt = 1\n    for ch in s[1:]:\n        if ch == cur:\n            cnt += 1\n        else:\n            res.append(f'{cur}{cnt}')\n            cur = ch\n            cnt = 1\n    res.append(f'{cur}{cnt}')\n    compressed = ''.join(res)\n    return compressed if len(compressed) < len(s) else s\n",
         "compress_string",
         [{"input": ["aabcccccaaa"], "expected": "a2b1c5a3", "description": "Compression is shorter", "is_hidden": False},
          {"input": ["abc"], "expected": "abc", "description": "Compression not shorter returns original", "is_hidden": False},
          {"input": ["aaaaaa"], "expected": "a6", "description": "Single repeated char", "is_hidden": True}],
         ["Compare len(compressed) with len(s)."], 105)

with open("scripts/track8.json", "w", encoding="utf-8") as f:
    json.dump(challenges, f, indent=2)
print("Track 8 generated: 10 challenges")
