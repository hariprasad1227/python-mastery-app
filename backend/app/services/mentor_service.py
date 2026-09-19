"""
Python Mastery - AI Mentor Service
Delivers Socratic feedback and hints to help learners discover solutions independently.
Supports OpenAI API integration with an offline pedagogical fallback engine.
"""

import httpx
import re
from typing import List, Optional
from backend.app.core.config import settings
from backend.app.schemas.mentor import (
    MentorHintRequest,
    MentorHintResponse,
    MentorChatRequest,
    MentorChatResponse,
)

SOCRATIC_SYSTEM_PROMPT = """
You are an expert, encouraging Python tutor using the Socratic method for an interactive coding platform called Python Mastery.
Your goal is to guide the student toward understanding rather than writing the solution for them.

Guidelines:
1. NEVER output the full working code solution.
2. If hint_level == 1: Give a gentle conceptual nudge or analogy. Point out which part of the instructions to re-read.
3. If hint_level == 2: Point toward specific Python syntax or logic operators (e.g. `%`, `.strip()`, `range()`), without writing the full statement.
4. If hint_level == 3: Break down the required logic into 2-3 plain English pseudocode steps.
5. If there is a runtime or syntax error, explain what that error usually indicates in Python in friendly terms.
6. Always end with a thought-provoking question to help them realize the next step.
"""


async def generate_mentor_hint(req: MentorHintRequest) -> MentorHintResponse:
    """
    Calls OpenAI API if configured, otherwise falls back to smart pedagogical rule engine.
    """
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your-openai-api-key":
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.OPENAI_MODEL,
                        "messages": [
                            {"role": "system", "content": SOCRATIC_SYSTEM_PROMPT},
                            {
                                "role": "user",
                                "content": f"Challenge: {req.challenge_title}\nInstructions: {req.challenge_instructions}\nLearner's Code:\n```python\n{req.learner_code}\n```\nError trace (if any):\n{req.error_message or 'No error trace, but tests did not pass'}\nHint Level requested: {req.hint_level} (1=Nudge, 2=Syntax clue, 3=Step breakdown)"
                            }
                        ],
                        "temperature": 0.5,
                        "max_tokens": 300
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    content = data["choices"][0]["message"]["content"]
                    return MentorHintResponse(
                        hint_level=req.hint_level,
                        hint=content,
                        socratic_question="What do you think happens when Python evaluates that line?",
                        encouragement="You're on the right track! Take a close look at the clues above."
                    )
        except Exception:
            # Fallback to local heuristic engine if API call fails
            pass

    # Heuristic Fallback Engine
    error = req.error_message or ""
    code = req.learner_code

    if "SyntaxError" in error:
        hint = "A SyntaxError means Python encountered characters it didn't expect. Check for matching parentheses, quotes, or a missing colon `:` at the end of `def` or `if`."
        question = "Did every opening bracket `(` or quote `\"` get closed properly?"
    elif "NameError" in error:
        hint = "Python is telling you that a variable or function name is being used before it was defined or spelled differently."
        question = "Does the spelling and capitalization match your function parameters?"
    elif "TypeError" in error:
        hint = "A TypeError indicates an operation was attempted on incompatible data types (for example, adding an integer to a string)."
        question = "Are you trying to combine different types without converting them first?"
    elif "Time Limit Exceeded" in error:
        hint = "Your code seems to be running indefinitely. Make sure any `while` loop has a step that moves toward its exit condition."
        question = "Does your loop variable update on every single iteration?"
    elif req.hint_level == 1:
        hint = f"Take a step back and examine the return requirement for '{req.challenge_title}'. Are you returning a value using `return` or just printing it?"
        question = "What data type does the challenge prompt say the function must produce?"
    elif req.hint_level == 2:
        hint = "Notice how Python handles function outputs. A function ends immediately when it hits a `return` statement."
        question = "Can you trace your logic with pen and paper for the first test input?"
    else:
        hint = "Step 1: Check your input parameters.\nStep 2: Transform or inspect the data.\nStep 3: Return the final evaluated result."
        question = "What is the very first calculation your function needs to make?"

    return MentorHintResponse(
        hint_level=req.hint_level,
        hint=hint,
        socratic_question=question,
        encouragement="Keep going! Debugging is where real programmers are forged."
    )


CHAT_SYSTEM_PROMPT = """
You are 'Python Mastery AI Mentor' — an intelligent, friendly, and expert Python tutor.
Your mission is to guide students from beginner basics to advanced Python mastery.
Tone: Encouraging, concise, clear, and pedagogical.
Languages: You fluently understand and explain in both English and Telugu (తెలుగు). If the user speaks or asks in Telugu, reply warmly in Telugu with clear Python code examples and English technical terms in parentheses.
Capabilities:
1. Explain core concepts with real-world analogies.
2. Debug errors (SyntaxError, IndentationError, TypeError, IndexError, etc.) and explain why they occur.
3. Provide clean, idiomatic PEP-8 Python code snippets with clear inline comments.
4. Suggest best practices, time complexity considerations, and next steps.
Keep responses well-structured using markdown headers, bullet points, and fenced code blocks.
"""


def is_telugu_query(text: str) -> bool:
    # Check for Telugu Unicode characters (\u0C00-\u0C7F) or common Telugu transliteration keywords
    if re.search(r"[\u0C00-\u0C7F]", text):
        return True
    telugu_keywords = [
        "telugu", "telugulo", "cheppu", "nerchuko", "ardham", "kaledhu", "chudu",
        "ela", "emiti", "enti", "cheppandi", "sahayam", "kaavali"
    ]
    words = re.findall(r"\b\w+\b", text.lower())
    return any(w in telugu_keywords for w in words)


async def generate_mentor_chat(req: MentorChatRequest) -> MentorChatResponse:
    """
    Handles multi-turn conversational AI mentorship.
    Supports OpenAI API if configured, otherwise employs rich local pedagogical intelligence.
    """
    latest_msg = req.messages[-1].content if req.messages else ""
    wants_telugu = (req.language == "te") or is_telugu_query(latest_msg)

    # 1. Try OpenAI if API key configured
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "your-openai-api-key":
        try:
            openai_messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
            if req.current_topic:
                openai_messages.append({
                    "role": "system",
                    "content": f"Context: Learner is currently on topic '{req.current_topic}'."
                })
            if req.code_context:
                openai_messages.append({
                    "role": "system",
                    "content": f"Learner's current code in editor:\n```python\n{req.code_context}\n```"
                })
            if req.error_context:
                openai_messages.append({
                    "role": "system",
                    "content": f"Recent execution error:\n{req.error_context}"
                })

            for m in req.messages[-6:]:
                openai_messages.append({"role": m.role, "content": m.content})

            async with httpx.AsyncClient(timeout=12.0) as client:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": settings.OPENAI_MODEL,
                        "messages": openai_messages,
                        "temperature": 0.6,
                        "max_tokens": 500
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    reply = data["choices"][0]["message"]["content"]
                    suggestions = (
                        ["తెలుగులో వివరించు", "కోడ్ ఉదాహరణ చూపించు", "ఇంటర్వ్యూ ప్రశ్నలు ఏమిటి?"]
                        if wants_telugu else
                        ["Show a real-world example", "How to optimize this?", "Give me a practice quiz"]
                    )
                    return MentorChatResponse(reply=reply, suggestions=suggestions)
        except Exception:
            pass

    # 2. Intelligent Pedagogical Local Rule Engine (Bilingual English & Telugu)
    query_lower = latest_msg.lower()
    code_ctx = req.code_context or ""
    err_ctx = (req.error_context or "").strip()

    suggestions = []

    # Case A: Debugging an active error
    if "error" in query_lower or "bug" in query_lower or "traceback" in query_lower or err_ctx:
        err = err_ctx or latest_msg
        if "syntaxerror" in err.lower():
            if wants_telugu:
                reply = (
                    "### 🐛 SyntaxError (సింటాక్స్ ఎర్రర్) విశ్లేషణ:\n\n"
                    "పైథాన్ మీ కోడ్‌లో ఊహించని అక్షరాన్ని లేదా తప్పిపోయిన సింబల్‌ను గుర్తించింది.\n\n"
                    "**సాధారణ కారణాలు:**\n"
                    "- `def`, `if`, `for`, `while` ల చివర కోలన్ (`:`) మర్చిపోవడం.\n"
                    "- బ్రాకెట్లు `()` లేదా కొటేషన్లు `\"...\"` సరిగ్గా మూయకపోవడం.\n\n"
                    "```python\n"
                    "# ❌ తప్పు:\n"
                    "# if x > 5\n"
                    "#     print(x)\n\n"
                    "# ✅ సరైన పద్ధతి:\n"
                    "if x > 5:\n"
                    "    print(x)\n"
                    "```"
                )
                suggestions = ["ఇంకొక ఉదాహరణ చూపించు", "ఇండెంటేషన్ ఎర్రర్ అంటే ఏమిటి?", "నా కోడ్ సరిగ్గా ఉందా?"]
            else:
                reply = (
                    "### 🐛 SyntaxError Diagnosis:\n\n"
                    "Python ran into syntax it didn't expect while parsing your code.\n\n"
                    "**Most Common Causes:**\n"
                    "- Missing colon (`:`) at the end of `def`, `if`, `for`, `while`, or `class` statements.\n"
                    "- Unclosed parentheses `()` or quotes `\"` / `'`.\n"
                    "- Invalid operators (e.g., using `=` instead of `==` for comparisons).\n\n"
                    "```python\n"
                    "# ❌ Wrong: missing colon\n"
                    "# if score >= 70\n"
                    "#     print('Pass')\n\n"
                    "# ✅ Correct:\n"
                    "if score >= 70:\n"
                    "    print('Pass')\n"
                    "```"
                )
                suggestions = ["What about IndentationError?", "Check my current code", "Show best practices"]

        elif "indentationerror" in err.lower() or "indent" in err.lower():
            if wants_telugu:
                reply = (
                    "### 📐 IndentationError (ఇండెంటేషన్ ఎర్రర్):\n\n"
                    "పైథాన్‌లో బ్రాకెట్లు `{}` బదులుగా స్పేస్‌ల ద్వారా బ్లాక్స్ (Blocks) గుర్తిస్తారు. లైన్ల స్పేసింగ్ సరిగ్గా లేకపోతే ఈ ఎర్రర్ వస్తుంది.\n\n"
                    "**నియమాలు:**\n"
                    "- ప్రతి కొత్త బ్లాక్ (if, for, def కింద) **4 spaces** ముందుకు ఉండాలి.\n"
                    "- Tabs మరియు Spaces ను కలిపి వాడకండి.\n\n"
                    "```python\n"
                    "def greet(name):\n"
                    "    # 4 spaces indentation\n"
                    "    return f'Hello, {name}!'\n"
                    "```"
                )
                suggestions = ["తెలుగులో మరిన్ని నియమాలు", "Tabs vs Spaces", "నా కోడ్ సరిచేయి"]
            else:
                reply = (
                    "### 📐 IndentationError Fix:\n\n"
                    "Python uses whitespace indentation (standard 4 spaces) to define blocks of code rather than curly braces `{}`.\n\n"
                    "**Fix Checklist:**\n"
                    "- Ensure all code inside a `def`, `if`, or `for` statement is indented by 4 spaces.\n"
                    "- Never mix tabs and spaces in the same file.\n"
                    "- Check that line alignments match within the same block."
                )
                suggestions = ["How to format automatically?", "Explain variables", "Check my current code"]

        elif "typeerror" in err.lower():
            if wants_telugu:
                reply = (
                    "### ⚠️ TypeError (టైప్ ఎర్రర్):\n\n"
                    "ఒక డేటా టైప్‌కు సరిపోని ఆపరేషన్‌ను చేసినప్పుడు ఇది వస్తుంది (ఉదాహరణకు నంబర్‌ను మరియు స్ట్రింగ్‌ను నేరుగా కూడటం).\n\n"
                    "```python\n"
                    "# ❌ TypeError:\n"
                    "# result = 'Age: ' + 25\n\n"
                    "# ✅ సరిదిద్దండి:\n"
                    "result = f'Age: {25}' # లేదా 'Age: ' + str(25)\n"
                    "```"
                )
                suggestions = ["Type conversion ఎలా చేయాలి?", "F-strings వివరించు", "నెక్స్ట్ టాపిక్ ఏంటి?"]
            else:
                reply = (
                    "### ⚠️ TypeError Explanation:\n\n"
                    "You attempted an operation on incompatible data types (such as adding an `int` directly to a `str`).\n\n"
                    "```python\n"
                    "# ❌ TypeError: can only concatenate str to str, not int\n"
                    "# msg = 'Level ' + 5\n\n"
                    "# ✅ Solution: Convert or use f-string\n"
                    "msg = f'Level {5}'\n"
                    "```"
                )
                suggestions = ["How do f-strings work?", "What are type hints?", "Show list operations"]

        else:
            if wants_telugu:
                reply = (
                    f"### 🔍 డీబగ్గింగ్ సహాయం:\n\n"
                    f"ఎర్రర్ వివరాలు: `{err[:120]}`\n\n"
                    "పైథాన్‌లో డీబగ్ చేయడానికి ఈ 3 స్టెప్స్ పాటించండి:\n"
                    "1. **ఎర్రర్ ఏ లైన్‌లో వచ్చిందో చూడండి** (Traceback లో చివరి లైన్).\n"
                    "2. **వేరియబుల్స్ విలువలను `print()` లేదా రిటర్న్ టైప్ చెక్ చేయండి** (`type(var)`).\n"
                    "3. **ఫంక్షన్ ఇన్‌పుట్ మరియు అవుట్‌పుట్ ఆర్గ్యుమెంట్స్ కరెక్ట్‌గా ఉన్నాయా చూసుకోండి**."
                )
                suggestions = ["కోడ్ ఉదాహరణ చూపించు", "ఇంకా అర్థం కాలేదు", "తెలుగులో మళ్ళీ చెప్పు"]
            else:
                reply = (
                    f"### 🔍 Debugging Analysis:\n\n"
                    f"Error detected: `{err[:120]}`\n\n"
                    "**3-Step Troubleshooting Guide:**\n"
                    "1. **Inspect Line Numbers**: Read the bottom-most line of your traceback.\n"
                    "2. **Check Variable Types**: Use `print(type(var))` to verify runtime values.\n"
                    "3. **Check Edge Cases**: Empty lists, `None` values, zero division, or boundary indices."
                )
                suggestions = ["How to inspect types?", "Show common mistakes", "Test edge cases"]

    # Case B: Telugu conceptual explanation
    elif wants_telugu or any(w in query_lower for w in ["telugu", "nerchuko", "cheppu", "ela"]):
        if any(w in query_lower for w in ["variable", "వేరియబుల్", "డేటా"]):
            reply = (
                "### 📦 పైథాన్ వేరియబుల్స్ & డేటా టైప్స్ (Variables in Telugu):\n\n"
                "పైథాన్‌లో వేరియబుల్ అంటే **డేటాను నిల్వ చేసే ఒక లేబుల్ లేదా కంటైనర్**.\n\n"
                "**ప్రధాన డేటా రకాలు:**\n"
                "- `int`: పూర్ణాంకాలు (ఉదా: `age = 25`)\n"
                "- `float`: దశాంశ సంఖ్యలు (ఉదా: `price = 99.50`)\n"
                "- `str`: అక్షరాలు లేదా పదాలు (ఉదా: `name = 'Rahul'`)\n"
                "- `bool`: నిజం/అబద్ధం (`is_active = True`)\n\n"
                "```python\n"
                "# ఉదాహరణ:\n"
                "student_name = 'Sita'\n"
                "marks = 95\n"
                "print(f'{student_name} scored {marks} marks!')\n"
                "```"
            )
            suggestions = ["లిస్ట్‌లు (Lists) అంటే ఏమిటి?", "లూప్స్ (Loops) వివరించు", "నాకు ఒక క్విజ్ ఇవ్వండి"]
        elif any(w in query_lower for w in ["loop", "ఫర్", "వైల్", "లూప్"]):
            reply = (
                "### 🔄 పైథాన్ లూప్స్ (Loops in Python):\n\n"
                "ఒకే పనిని పదే పదే చేయాల్సి వచ్చినప్పుడు మనం లూప్స్ వాడతాము.\n\n"
                "1. **`for` loop**: సీక్వెన్స్ (లిస్ట్, రేంజ్) లోని ప్రతి ఎలిమెంట్ మీద రన్ అవుతుంది.\n"
                "2. **`while` loop**: ఒక కండిషన్ `True` గా ఉన్నంత వరకు రన్ అవుతుంది.\n\n"
                "```python\n"
                "# 1 నుండి 5 వరకు ప్రింట్ చేయడం:\n"
                "for i in range(1, 6):\n"
                "    print(f'Number: {i}')\n"
                "```"
            )
            suggestions = ["while loop ఉదాహరణ", "break మరియు continue", "List Comprehension అంటే ఏమిటి?"]
        elif any(w in query_lower for w in ["function", "ఫంక్షన్", "def"]):
            reply = (
                "### ⚡ పైథాన్ ఫంక్షన్స్ (Functions in Python):\n\n"
                "ఫంక్షన్ అంటే ఒక నిర్దిష్ట పనిని చేసే కోడ్ బ్లాక్. ఒకసారి రాసి అనేక సార్లు వాడుకోవచ్చు (Reusability).\n\n"
                "```python\n"
                "def add_numbers(a, b):\n"
                "    \"\"\"రెండు సంఖ్యలను కూడి రిటర్న్ చేస్తుంది\"\"\"\n"
                "    return a + b\n\n"
                "result = add_numbers(10, 20)\n"
                "print('Result:', result) # Output: 30\n"
                "```"
            )
            suggestions = ["*args, **kwargs అంటే ఏమిటి?", "Lambda ఫంక్షన్స్", "ఒక ప్రాక్టీస్ ప్రశ్న ఇవ్వండి"]
        else:
            reply = (
                "### 🐍 పైథాన్ మాస్టరీ AI అసిస్టెంట్ కి స్వాగతం!\n\n"
                "నేను మీకు పైథాన్ నేర్చుకోవడంలో సహాయం చేయగలను:\n"
                "- 💡 **కాన్సెప్ట్‌లు సులభంగా అర్థమయ్యేలా చెప్పడం**\n"
                "- 🐛 **మీ కోడ్‌లోని ఎర్రర్లను డీబగ్ చేయడం**\n"
                "- 📝 **రియల్-వరల్డ్ ప్రాజెక్ట్ ఉదాహరణలు ఇవ్వడం**\n"
                "- 🎯 **ఇంటర్వ్యూ కోడింగ్ సవాళ్లను వివరించడం**\n\n"
                "మీకు ఏ కాన్సెప్ట్ గురించి తెలుసుకోవాలని ఉంది? అడగండి!"
            )
            suggestions = ["వేరియబుల్స్ అంటే ఏమిటి?", "లూప్స్ గురించి వివరించు", "ఫంక్షన్స్ ఎలా రాయాలి?"]

    # Case C: English Concept & Explanation Engine
    elif any(w in query_lower for w in ["list", "dict", "dictionary", "set", "tuple"]):
        reply = (
            "### 📚 Python Core Data Structures:\n\n"
            "| Structure | Syntax | Ordered? | Mutable? | Unique Only? |\n"
            "|---|---|:---:|:---:|:---:|\n"
            "| **List** | `[1, 2, 3]` | ✅ Yes | ✅ Yes | ❌ No |\n"
            "| **Tuple** | `(1, 2, 3)` | ✅ Yes | ❌ No (Immutable) | ❌ No |\n"
            "| **Set** | `{1, 2, 3}` | ❌ No | ✅ Yes | ✅ Yes (Deduplicated) |\n"
            "| **Dict** | `{'key': 'val'}` | ✅ (3.7+) | ✅ Yes | Keys are unique |\n\n"
            "```python\n"
            "# Quick Idiomatic Example:\n"
            "fruits = ['apple', 'banana', 'apple']\n"
            "unique_fruits = set(fruits)  # {'apple', 'banana'}\n"
            "```"
        )
        suggestions = ["Show list comprehensions", "Dictionary methods guide", "Explain in Telugu"]

    elif any(w in query_lower for w in ["function", "def", "lambda", "args"]):
        reply = (
            "### ⚡ Python Functions & Parameter Handling:\n\n"
            "Functions allow you to encapsulate modular, testable units of logic.\n\n"
            "```python\n"
            "def calculate_total(price, tax_rate=0.08, *discounts, **metadata):\n"
            "    total = price * (1 + tax_rate)\n"
            "    for d in discounts:\n"
            "        total -= d\n"
            "    return round(total, 2)\n\n"
            "print(calculate_total(100, 0.05, 10, customer_id='c123'))  # 95.0\n"
            "```\n\n"
            "- `*args` captures arbitrary positional arguments into a `tuple`.\n"
            "- `**kwargs` captures arbitrary keyword arguments into a `dict`."
        )
        suggestions = ["What are closures?", "Explain recursion", "How does LEGB scope work?"]

    elif any(w in query_lower for w in ["oop", "class", "object", "inheritance"]):
        reply = (
            "### 🏛️ Object-Oriented Programming in Python:\n\n"
            "Python classes bundle data (attributes) and behavior (methods) together cleanly.\n\n"
            "```python\n"
            "class BankAccount:\n"
            "    def __init__(self, owner: str, balance: float = 0.0):\n"
            "        self.owner = owner\n"
            "        self._balance = balance\n\n"
            "    def deposit(self, amount: float) -> float:\n"
            "        if amount <= 0:\n"
            "            raise ValueError('Deposit must be positive')\n"
            "        self._balance += amount\n"
            "        return self._balance\n\n"
            "    def __repr__(self) -> str:\n"
            "        return f'BankAccount(owner={self.owner!r}, balance={self._balance})'\n"
            "```"
        )
        suggestions = ["What is encapsulation?", "Explain dunder methods", "Show inheritance example"]

    else:
        # Default conversational tutor response
        reply = (
            "### 👋 Hello! I am your AI Python Mentor.\n\n"
            "I'm here to help you master Python step-by-step! Here is what I can do:\n\n"
            "- 💡 **Explain Concepts**: From basic variables to decorators and async IO.\n"
            "- 🐛 **Debug Code**: Paste any error or code snippet and I'll break down the solution.\n"
            "- 🎯 **Interactive Quizzes**: Test your knowledge on any topic.\n"
            "- 🗣️ **Bilingual Tutoring**: Ask in English or Telugu (తెలుగు) anytime!\n\n"
            "What would you like to explore today?"
        )
        suggestions = [
            "💡 Explain list comprehension",
            "🗣️ తెలుగులో నేర్పించు (Learn in Telugu)",
            "🐛 Help me fix an error",
            "🎯 Quiz me on Python"
        ]

    return MentorChatResponse(reply=reply, suggestions=suggestions)
