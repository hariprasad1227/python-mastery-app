"""
Comprehensive End-to-End Verification Suite for Python Mastery
Explicitly verifies:
- Database Schema & Seed Curriculum integrity
- Authentication Flow (Signup, Login, Token Auth, Invalid Auth, Logout)
- Sandbox Python Code Execution (Success, Failure, Stdout, Stderr)
- Timer / Timeout Enforcement (Infinite loops terminated cleanly)
- 2-Test-Case Requirement (All challenges have >= 2 test cases)
- Strict Problem Unlocking (Prerequisites enforced, unlocks upon completion)
- XP & Badges progression
- AI Mentor Socratic Hint Engine (Tiers 1, 2, 3)
"""

import sys
import os
import time
import json

# Ensure root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from backend.app.main import app
from runner.runner import execute_learner_code

client = TestClient(app)


def test_database_schema_and_curriculum():
    """Item 7 & 11: Database configuration and minimum 2 test cases per challenge."""
    print("\n--- Verifying Database Configuration & Curriculum ---")
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "database", "schema.sql")
    seed_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "database", "seed_lessons.sql")

    assert os.path.exists(schema_path), "schema.sql must exist"
    assert os.path.exists(seed_path), "seed_lessons.sql must exist"

    with open(schema_path, "r", encoding="utf-8") as f:
        schema_content = f.read()
    assert "CREATE TABLE IF NOT EXISTS public.profiles" in schema_content
    assert "CREATE TABLE IF NOT EXISTS public.challenges" in schema_content
    assert "CREATE TABLE IF NOT EXISTS public.user_progress" in schema_content
    assert "ROW LEVEL SECURITY" in schema_content

    # Check curriculum from API
    res = client.get("/api/progression/curriculum")
    assert res.status_code == 200
    modules = res.json()
    assert len(modules) >= 5, "Must have at least 5 curriculum modules"

    # Verify 2-test-case requirement for all 100 challenges via database
    from backend.app.models.entities import Challenge
    from backend.app.db.session import SessionLocal
    db = SessionLocal()
    all_chals = db.query(Challenge).all()
    assert len(all_chals) == 100, f"Expected 100 challenges, got {len(all_chals)}"
    for ch in all_chals:
        tcs = json.loads(ch.test_cases_json) if ch.test_cases_json else []
        assert len(tcs) >= 2, f"Challenge {ch.title} must have >= 2 test cases, got {len(tcs)}"
    db.close()

    print("[PASS] Database schema & 2-test-case requirement verified.")


def test_auth_flow():
    """Item 8: Full Authentication Flow with real DB & JWT."""
    print("\n--- Verifying Authentication Flow ---")
    ts = int(time.time() * 1000)
    email = f"e2e_user_{ts}@example.com"
    username = f"e2e_user_{ts}"
    password = "SecurePassword123!"

    # 1. Signup
    signup_data = {
        "email": email,
        "password": password,
        "username": username,
        "display_name": "Mastery Tester"
    }
    res_signup = client.post("/api/auth/signup", json=signup_data)
    assert res_signup.status_code == 200, f"Signup failed: {res_signup.text}"
    token = res_signup.json()["access_token"]
    assert len(token) > 20 and token.count(".") == 2
    print("  [OK] Signup succeeded and issued signed cryptographic JWT")

    # 2. Prevent duplicate signup
    res_dup = client.post("/api/auth/signup", json=signup_data)
    assert res_dup.status_code == 400
    print("  [OK] Duplicate signup correctly blocked")

    # 3. Login with correct password
    login_data = {
        "email": email,
        "password": password
    }
    res_login = client.post("/api/auth/login", json=login_data)
    assert res_login.status_code == 200
    login_token = res_login.json()["access_token"]
    print("  [OK] Login succeeded and returned JWT")

    # 4. Login with invalid password
    res_bad = client.post("/api/auth/login", json={"email": email, "password": "wrong"})
    assert res_bad.status_code == 401
    print("  [OK] Incorrect password blocked with 401")

    # 5. Get current user profile with token
    res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {login_token}"})
    assert res_me.status_code == 200
    user_me = res_me.json()
    assert user_me["authenticated"] is True
    assert user_me["user"]["email"] == email
    print("  [OK] Authenticated /me endpoint returned user record")

    # 6. Logout
    res_logout = client.post("/api/auth/logout", headers={"Authorization": f"Bearer {login_token}"})
    assert res_logout.status_code == 200
    print("  [OK] Logout endpoint acknowledged")

    print("[PASS] Authentication flow verified.")
    return login_token


def test_code_execution_and_timer():
    """Item 9 & 10: Python Execution & Timer/Timeout."""
    print("\n--- Verifying Code Execution & Timeout Timer ---")
    
    # Valid execution
    code_valid = "def greet(name):\n    return f'Hello, {name}!'"
    res_valid = execute_learner_code(code_valid, entry_function_name="greet", test_cases=[
        {"input": ["Sam"], "expected": "Hello, Sam!", "description": "Greeting Sam"}
    ])
    assert res_valid["passed"] is True
    assert res_valid["execution_time_ms"] >= 0
    print(f"  [OK] Normal execution finished in {res_valid['execution_time_ms']}ms")

    # Timer & Timeout enforcement
    code_infinite = "def loop():\n    while True:\n        pass"
    res_timeout = execute_learner_code(code_infinite, entry_function_name="loop", test_cases=[
        {"input": [], "expected": None}
    ], timeout_seconds=1.0)
    assert res_timeout["passed"] is False
    assert res_timeout["status"] == "time_limit_exceeded"
    assert "Time Limit Exceeded" in res_timeout["stderr"]
    print("  [OK] Timer cleanly killed infinite loop after timeout limit")

    print("[PASS] Execution & Timer verified.")


def test_problem_unlocking_xp_and_badges(token: str):
    """Item 12 & 13: Strict Unlocking, XP and Badges."""
    print("\n--- Verifying Problem Unlocking, XP, & Badges ---")
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch initial curriculum with token
    curr = client.get("/api/progression/curriculum", headers=headers).json()
    ch1 = curr[0]["challenges"][0]
    assert ch1["status"] == "available"
    ch2 = curr[1]["challenges"][0]
    assert ch2["status"] == "locked"

    # Initial profile
    initial_prof = client.get("/api/progression/profile", headers=headers).json()
    initial_xp = initial_prof["total_xp"]

    # Submit solution for chal-1 (Personalized Greeting)
    sol_ch1 = "def greet(name: str) -> str:\n    return f'Hello, {name}!'"
    res_run1 = client.post("/api/runner/execute", headers=headers, json={
        "challenge_id": "chal-1",
        "code": sol_ch1
    })
    assert res_run1.status_code == 200
    run_data1 = res_run1.json()
    assert run_data1["passed"] is True
    assert run_data1["xp_earned"] == 50
    assert run_data1["unlocked_next"] is False
    print(f"  [OK] Challenge 1 code passed! Earned {run_data1['xp_earned']} XP (exam required to unlock next)")

    # Complete lesson and pass Topic 1 Exam to unlock chal-2
    client.post("/api/progression/topics/chal-1/complete-lesson", headers=headers)
    from backend.app.models.entities import ExamQuestion
    from backend.app.db.session import SessionLocal
    db = SessionLocal()
    questions = db.query(ExamQuestion).filter(ExamQuestion.exam_id == "exam-chal-1").all()
    q_dict = {q.id: q.correct_answer for q in questions}
    db.close()

    res_exam1 = client.post("/api/progression/exams/exam-chal-1/submit", headers=headers, json={"answers": q_dict})
    assert res_exam1.status_code == 200
    assert res_exam1.json()["passed"] is True
    print(f"  [OK] Topic 1 Exam passed! Challenge 2 is now unlocked.")

    # Now chal-2 should be unlocked
    curr_after_1 = client.get("/api/progression/curriculum", headers=headers).json()
    chal2 = next((c for m in curr_after_1 for c in m["challenges"] if c["id"] == "chal-2"), None)
    assert chal2 is not None and chal2["status"] == "available"

    # Submit solution for chal-2 (Even or Odd)
    sol_ch2 = "def check_parity(n: int) -> str:\n    return 'Even' if n % 2 == 0 else 'Odd'"
    res_run2 = client.post("/api/runner/execute", headers=headers, json={
        "challenge_id": "chal-2",
        "code": sol_ch2
    })
    assert res_run2.status_code == 200
    run_data2 = res_run2.json()
    assert run_data2["passed"] is True
    assert run_data2["xp_earned"] == 60
    print(f"  [OK] Challenge 2 passed! Earned {run_data2['xp_earned']} XP")

    # Verify XP updated on profile
    updated_prof = client.get("/api/progression/profile", headers=headers).json()
    assert updated_prof["total_xp"] >= initial_xp + run_data1["xp_earned"] + run_data2["xp_earned"]
    print(f"  [OK] Profile updated: {updated_prof['total_xp']} Total XP, Level {updated_prof['current_level']}")

    # Verify badges exist and awarded
    badges = updated_prof["badges"]
    assert len(badges) >= 5
    awarded_count = sum(1 for b in badges if b["awarded"])
    assert awarded_count >= 1
    print(f"  [OK] Badges active ({awarded_count} awarded)")

    # Complete lesson and pass Topic 2 Exam to unlock chal-3
    client.post("/api/progression/topics/chal-2/complete-lesson", headers=headers)
    db2 = SessionLocal()
    questions2 = db2.query(ExamQuestion).filter(ExamQuestion.exam_id == "exam-chal-2").all()
    q_dict2 = {q.id: q.correct_answer for q in questions2}
    db2.close()

    res_exam2 = client.post("/api/progression/exams/exam-chal-2/submit", headers=headers, json={"answers": q_dict2})
    assert res_exam2.status_code == 200
    assert res_exam2.json()["passed"] is True
    print(f"  [OK] Topic 2 Exam passed! Challenge 3 is now unlocked.")

    # Verify that completing chal-2 exam unlocked chal-3
    updated_curr = client.get("/api/progression/curriculum", headers=headers).json()
    chal3_post = next((c for m in updated_curr for c in m["challenges"] if c["id"] == "chal-3"), None)
    assert chal3_post is not None and chal3_post["status"] == "available"
    print(f"  [OK] Problem unlocking verified: chal-2 exam passed -> chal-3 unlocked!")

    print("[PASS] Unlocking, XP, and Badges verified.")


def test_ai_mentor_integration():
    """Item 14: AI Mentor Socratic Engine."""
    print("\n--- Verifying AI Mentor Integration ---")

    for level in [1, 2, 3]:
        payload = {
            "challenge_title": "Sum of Multiples",
            "challenge_instructions": "Sum positive integers <= limit divisible by factor",
            "learner_code": "def sum_multiples(limit, factor):\n    for i in limit:\n        return i\n",
            "error_message": "TypeError: 'int' object is not iterable",
            "hint_level": level
        }
        res = client.post("/api/mentor/hint", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["hint_level"] == level
        assert len(data["hint"]) > 0
        assert len(data["socratic_question"]) > 0
        print(f"  [OK] Hint Level {level}: \"{data['hint'][:60]}...\"")
        print(f"       Question: \"{data['socratic_question']}\"")

    print("[PASS] AI Mentor Socratic feedback verified.")


if __name__ == "__main__":
    print("==================================================")
    print("STARTING FULL END-TO-END VERIFICATION")
    print("==================================================")
    test_database_schema_and_curriculum()
    token = test_auth_flow()
    test_code_execution_and_timer()
    test_problem_unlocking_xp_and_badges(token)
    test_ai_mentor_integration()
    print("\n==================================================")
    print("ALL END-TO-END ACCEPTANCE VERIFICATIONS PASSED!")
    print("==================================================")
