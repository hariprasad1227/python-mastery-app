"""
Comprehensive Core Engine Verification Suite
Covers all production-hardening requirements:
1. Granular health checks (/health, /health/db, /health/sandbox)
2. Real DB authentication, bcrypt hashing, JWT validation, expiration & forgery
3. Server-side challenge unlocking & authorization (403 on locked)
4. Hidden test case concealment (GET detail hides tests, sanitized response)
5. Server-side attempt timer & timeout rejection (400 on expired attempt)
6. Submissions persistence & Single XP transaction (prevent duplicate XP)
7. User isolation (User A progress cannot affect User B)
8. Rate limiting (429 Too Many Requests)
"""

import sys
import os
import time
from datetime import datetime, timedelta
import jwt

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.config import settings
from backend.app.core.security import create_access_token
from backend.app.db.session import SessionLocal
from backend.app.models.entities import User, Profile, Challenge, UserProgress, Attempt, Submission, XPTransaction

client = TestClient(app)


def test_health_checks():
    print("--- 1. Testing Granular Health Checks ---")
    
    res_db = client.get("/health/db")
    assert res_db.status_code == 200, f"/health/db failed: {res_db.text}"
    assert res_db.json()["status"] == "up"
    print("  [PASS] /health/db returns up")

    res_sandbox = client.get("/health/sandbox")
    assert res_sandbox.status_code == 200, f"/health/sandbox failed: {res_sandbox.text}"
    assert res_sandbox.json()["status"] == "up"
    print("  [PASS] /health/sandbox returns up")

    res_health = client.get("/health")
    assert res_health.status_code == 200, f"/health failed: {res_health.text}"
    data = res_health.json()
    assert data["status"] == "healthy"
    assert data["components"]["database"]["status"] == "up"
    assert data["components"]["sandbox"]["status"] == "up"
    print("  [PASS] /health composite check returns healthy with all components up")


def test_auth_and_security_edge_cases():
    print("\n--- 2. Testing Auth, BCrypt, JWT & Security Edge Cases ---")
    ts = int(time.time() * 1000)
    email = f"user_a_{ts}@mastery.io"
    password = "CorrectPassword123!"
    username = f"usera_{ts}"

    # Registration
    res_reg = client.post("/api/auth/signup", json={
        "email": email,
        "password": password,
        "username": username,
        "display_name": "User Alpha"
    })
    assert res_reg.status_code == 200, f"Registration failed: {res_reg.text}"
    token_a = res_reg.json()["access_token"]
    user_a_id = res_reg.json()["user"]["id"]
    print("  [PASS] Registration succeeded and returned signed JWT")

    # Duplicate registration
    res_dup = client.post("/api/auth/signup", json={
        "email": email,
        "password": "OtherPassword123!",
        "username": f"other_{ts}"
    })
    assert res_dup.status_code == 400
    print("  [PASS] Duplicate email registration rejected with 400")

    # Short password rejected
    res_short = client.post("/api/auth/signup", json={
        "email": f"short_{ts}@mastery.io",
        "password": "123",
        "username": f"short_{ts}"
    })
    assert res_short.status_code == 422
    print("  [PASS] Short password rejected by validator (422)")

    # Login correct
    res_login = client.post("/api/auth/login", json={"email": email, "password": password})
    assert res_login.status_code == 200
    print("  [PASS] Login with correct password succeeded")

    # Login incorrect password
    res_bad_pw = client.post("/api/auth/login", json={"email": email, "password": "WrongPassword!"})
    assert res_bad_pw.status_code == 401
    print("  [PASS] Login with wrong password rejected with 401")

    # /me endpoint with valid token
    res_me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token_a}"})
    assert res_me.status_code == 200
    assert res_me.json()["user"]["email"] == email
    print("  [PASS] /api/auth/me succeeded with valid JWT")

    # Missing auth token
    res_no_auth = client.get("/api/auth/me")
    assert res_no_auth.status_code == 401
    print("  [PASS] Missing token returns 401")

    # Forged signature
    forged = token_a[:-4] + "zzzz"
    res_forged = client.get("/api/auth/me", headers={"Authorization": f"Bearer {forged}"})
    assert res_forged.status_code == 401
    print("  [PASS] Forged token signature returns 401")

    # Expired token
    expired_token = create_access_token(data={"sub": user_a_id}, expires_delta=timedelta(seconds=-10))
    res_exp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
    assert res_exp.status_code == 401
    assert "expired" in res_exp.json()["detail"].lower()
    print("  [PASS] Expired token correctly rejected with 401")

    return token_a, user_a_id


def test_hidden_test_cases_concealment(token: str):
    print("\n--- 3. Testing Hidden Test Cases Concealment ---")
    # GET /challenges/chal-1 must NOT return hidden tests
    res = client.get("/api/progression/challenges/chal-1")
    assert res.status_code == 200
    ch_data = res.json()
    assert "test_cases" in ch_data
    public_tests = ch_data["test_cases"]
    for tc in public_tests:
        assert tc.get("is_hidden") is False, "Hidden test was leaked in challenge detail!"
    print(f"  [PASS] Public challenge detail contains only public tests ({len(public_tests)} tests)")


def test_challenge_authorization_and_server_attempt_timer(token: str, user_id: str):
    print("\n--- 4. Testing Challenge Authorization & Attempt Timer ---")

    # chal-2 is locked for user A initially
    res_locked = client.post(
        "/api/runner/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={"challenge_id": "chal-2", "code": "def check_parity(n): return 'Even'"}
    )
    assert res_locked.status_code == 403
    print("  [PASS] Locked challenge rejected with 403 Forbidden")

    # Starting a locked challenge must also be rejected
    res_start_locked = client.post(
        "/api/progression/challenges/chal-2/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res_start_locked.status_code == 403
    print("  [PASS] Starting locked challenge rejected with 403 Forbidden")

    # Start attempt for chal-1 (available)
    res_start = client.post(
        "/api/progression/challenges/chal-1/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res_start.status_code == 200
    attempt_info = res_start.json()
    attempt_id = attempt_info["attempt_id"]
    assert attempt_info["status"] == "in_progress"
    print(f"  [PASS] Challenge attempt started in DB: ID={attempt_id}")

    # Test expired attempt rejection
    # Manually backdate the attempt in DB to simulate timeout expiration
    with SessionLocal() as db:
        att = db.query(Attempt).filter(Attempt.id == attempt_id).first()
        att.started_at = datetime.utcnow() - timedelta(seconds=att.time_limit_seconds + 10)
        db.commit()

    res_expired_submit = client.post(
        "/api/runner/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "challenge_id": "chal-1",
            "attempt_id": attempt_id,
            "code": "def greet(name):\n    return f'Hello, {name}!'"
        }
    )
    assert res_expired_submit.status_code == 400
    assert "timed out" in res_expired_submit.json()["detail"].lower()
    print("  [PASS] Expired attempt submission strictly rejected with HTTP 400")

    # Start a fresh valid attempt
    res_fresh = client.post(
        "/api/progression/challenges/chal-1/start",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res_fresh.status_code == 200
    fresh_attempt_id = res_fresh.json()["attempt_id"]

    # Submit valid solution
    res_exec = client.post(
        "/api/runner/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "challenge_id": "chal-1",
            "attempt_id": fresh_attempt_id,
            "code": "def greet(name: str) -> str:\n    return f'Hello, {name}!'"
        }
    )
    assert res_exec.status_code == 200
    data = res_exec.json()
    assert data["passed"] is True
    assert data["xp_earned"] == 50
    # In exam-gated progression, code alone does not unlock next topic until exam is passed
    assert data["unlocked_next"] is False
    assert data["passed_tests_count"] > 0
    assert data["total_tests_count"] >= 2
    # Verify hidden test in response is sanitized
    hidden_tests = [tr for tr in data["test_results"] if tr["is_hidden"]]
    assert len(hidden_tests) > 0, "Challenge 1 should have at least 1 hidden test"
    for ht in hidden_tests:
        assert ht["input"] == "[Hidden Input]"
        assert ht["expected"] == "[Hidden Expected Value]"
    print("  [PASS] Valid attempt passed! Hidden test assertions sanitized in response.")

    # Now pass Topic 1 Exam to unlock Challenge 2
    from backend.app.models.entities import ExamQuestion
    db = SessionLocal()
    questions = db.query(ExamQuestion).filter(ExamQuestion.exam_id == "exam-chal-1").all()
    q_dict = {q.id: q.correct_answer for q in questions}
    db.close()

    res_exam = client.post(
        "/api/progression/exams/exam-chal-1/submit",
        json={"answers": q_dict},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res_exam.status_code == 200
    assert res_exam.json()["passed"] is True
    print("  [PASS] Topic 1 Exam passed! Challenge 2 is now unlocked.")

    return fresh_attempt_id


def test_submissions_persistence_and_no_duplicate_xp(token: str, user_id: str):
    print("\n--- 5. Testing Submissions Persistence & Duplicate XP Prevention ---")
    
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        initial_xp = user.profile.total_xp
        tx_count_before = db.query(XPTransaction).filter(XPTransaction.user_id == user_id).count()

    # Re-submit the exact same challenge solution
    res_resubmit = client.post(
        "/api/runner/execute",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "challenge_id": "chal-1",
            "code": "def greet(name: str) -> str:\n    return f'Hello, {name}!'"
        }
    )
    assert res_resubmit.status_code == 200
    data = res_resubmit.json()
    assert data["passed"] is True
    # MUST award 0 XP for duplicate completion!
    assert data["xp_earned"] == 0, f"Expected 0 XP on replay, got {data['xp_earned']}"
    assert data["total_xp"] == initial_xp

    with SessionLocal() as db:
        tx_count_after = db.query(XPTransaction).filter(XPTransaction.user_id == user_id).count()
        assert tx_count_after == tx_count_before, "Duplicate XPTransaction was created!"
        
        # Verify 2 submissions persisted in submissions table
        subs = db.query(Submission).filter(Submission.user_id == user_id, Submission.challenge_id == "chal-1").all()
        assert len(subs) >= 2
        for s in subs:
            assert s.passed_tests_count > 0
            assert s.total_tests_count > 0
    print("  [PASS] Submissions properly persisted; duplicate XP strictly prevented (0 XP on replay).")


def test_user_isolation(token_a: str, user_a_id: str):
    print("\n--- 6. Testing User Isolation ---")
    ts = int(time.time() * 1000)
    email_b = f"user_b_{ts}@mastery.io"
    res_b = client.post("/api/auth/signup", json={
        "email": email_b,
        "password": "Password123!",
        "username": f"userb_{ts}"
    })
    token_b = res_b.json()["access_token"]
    user_b_id = res_b.json()["user"]["id"]

    # User A completed chal-1, so chal-2 is unlocked for User A
    with SessionLocal() as db:
        p_a = db.query(UserProgress).filter(UserProgress.user_id == user_a_id, UserProgress.challenge_id == "chal-2").first()
        assert p_a.status == "available"

        # For User B, chal-2 MUST STILL BE LOCKED!
        p_b = db.query(UserProgress).filter(UserProgress.user_id == user_b_id, UserProgress.challenge_id == "chal-2").first()
        assert p_b.status == "locked"

    # User B attempting chal-2 must be 403 Forbidden
    res_exec_b = client.post(
        "/api/runner/execute",
        headers={"Authorization": f"Bearer {token_b}"},
        json={"challenge_id": "chal-2", "code": "def check_parity(n): return 'Even'"}
    )
    assert res_exec_b.status_code == 403
    print("  [PASS] User A progress does NOT unlock challenges for User B (User Isolation verified).")


def test_rate_limiting():
    print("\n--- 7. Testing Database-Backed Rate Limiting ---")
    ts = int(time.time() * 1000)
    flood_email = f"rate_limit_{ts}@mastery.io"

    # Call login repeatedly until rate limit triggers (limit is 15 requests/min)
    got_429 = False
    for i in range(25):
        res = client.post("/api/auth/login", json={"email": flood_email, "password": "WrongPassword!"})
        if res.status_code == 429:
            got_429 = True
            assert "Retry-After" in res.headers
            break

    assert got_429, "Rate limiter did not trigger HTTP 429 after 25 rapid requests!"
    print("  [PASS] Rate limiter triggered HTTP 429 Too Many Requests with Retry-After header.")


if __name__ == "__main__":
    print("=" * 60)
    print("COMPREHENSIVE CORE ENGINE ACCEPTANCE TEST")
    print("=" * 60)
    test_health_checks()
    token_a, user_a_id = test_auth_and_security_edge_cases()
    test_hidden_test_cases_concealment(token_a)
    test_challenge_authorization_and_server_attempt_timer(token_a, user_a_id)
    test_submissions_persistence_and_no_duplicate_xp(token_a, user_a_id)
    test_user_isolation(token_a, user_a_id)
    test_rate_limiting()
    print("\n" + "=" * 60)
    print("ALL CORE ENGINE PRODUCTION ACCEPTANCE TESTS PASSED!")
    print("=" * 60)
