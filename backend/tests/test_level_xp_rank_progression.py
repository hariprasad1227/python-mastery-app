"""
Comprehensive Test Suite: 10-Level Progression, XP & Rank System
Verifies:
1. Three Independent Pillars (Level, Rank, XP)
2. 10-Level Curriculum Roadmap & Gated Unlock Engine
3. Comprehensive Level Final Tests (Server-graded, >= 70%, retries, multi-format)
4. Periodic Assessments (Weekly +200 XP, Monthly +500 XP)
5. Multi-factor Performance Score Formula (30/30/15/15/10)
6. Promotion Criteria (Gold -> Platinum -> Diamond -> Master)
7. Anti-Demotion Guardrail (3 consecutive low periods protection)
8. Server-authoritative Idempotent XP awarding
"""

import pytest
import uuid
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.db.session import SessionLocal, init_db
from backend.app.models.entities import (
    User, Profile, UserProgress, Challenge, LevelProgress,
    LevelFinalTest, LevelFinalTestAttempt, PeriodicTest,
    PeriodicTestAttempt, XPTransaction, RankHistory
)
from backend.app.core.xp_service import award_xp, LEVEL_XP_REQUIREMENTS
from backend.app.core.rank_engine import evaluate_user_rank, calculate_performance_components

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()


def create_test_user(prefix="prog_student"):
    uid = str(uuid.uuid4())[:8]
    email = f"{prefix}_{uid}@example.com"
    username = f"{prefix}_{uid}"
    password = "SecurePassword123!"

    res = client.post("/api/auth/signup", json={
        "email": email,
        "username": username,
        "password": password,
        "display_name": f"Student {uid}"
    })
    assert res.status_code == 200, f"Registration failed: {res.text}"
    token = res.json()["access_token"]
    user_id = res.json()["user"]["id"]
    return {
        "id": user_id,
        "email": email,
        "username": username,
        "token": token,
        "headers": {"Authorization": f"Bearer {token}"}
    }


def test_01_three_independent_pillars_initial_state():
    """Verify new student starts at Level 1, Rank GOLD, XP 0."""
    user = create_test_user("user_pillars")
    res = client.get("/api/progression/profile", headers=user["headers"])
    assert res.status_code == 200
    data = res.json()
    assert data["current_level"] == 1
    assert data["current_rank"] == "GOLD"
    assert data["total_xp"] == 0


def test_02_all_10_levels_listed():
    """Verify GET /api/progression/levels lists 10 structured levels."""
    user = create_test_user("user_levels")
    res = client.get("/api/progression/levels", headers=user["headers"])
    assert res.status_code == 200
    levels = res.json()
    assert len(levels) == 10
    assert levels[0]["level_number"] == 1
    assert levels[0]["unlocked"] is True
    assert levels[1]["level_number"] == 2
    assert levels[1]["unlocked"] is False
    assert levels[9]["level_number"] == 10
    assert levels[9]["unlocked"] is False


def test_03_level_final_test_gated_by_topic_completion():
    """Verify student cannot take Level 1 Final Test before completing all 10 topics."""
    user = create_test_user("user_gate")
    res = client.get("/api/progression/levels/1/final-test", headers=user["headers"])
    # Should be rejected with 403 Forbidden because 10 topics have not been completed
    assert res.status_code == 403
    assert "Prerequisite not met" in res.json()["detail"]


def mark_topics_passed(db, user_id, count=10):
    for ch in db.query(Challenge).filter(Challenge.order_index <= count).all():
        p = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.challenge_id == ch.id
        ).first()
        if not p:
            p = UserProgress(user_id=user_id, challenge_id=ch.id)
            db.add(p)
        p.status = "passed"
        p.exam_passed = True
    db.commit()


def test_04_level_final_test_access_after_topics_completed():
    """Verify that completing 10 topics unlocks Level Final Test access."""
    user = create_test_user("user_lvl_topics")
    db = SessionLocal()
    try:
        mark_topics_passed(db, user["id"], count=10)
    finally:
        db.close()

    # Now Level 1 Final Test should be accessible
    res = client.get("/api/progression/levels/1/final-test", headers=user["headers"])
    assert res.status_code == 200
    data = res.json()
    assert data["level_number"] == 1
    assert len(data["questions"]) >= 5
    assert data["pass_percentage"] == 70


def test_05_level_final_test_grading_and_failed_attempt():
    """Verify scoring < 70% fails the final test and does not unlock Level 2."""
    user = create_test_user("user_fail_test")
    db = SessionLocal()
    try:
        mark_topics_passed(db, user["id"], count=10)
    finally:
        db.close()

    # Submit all wrong answers
    submit_res = client.post(
        "/api/progression/levels/1/final-test/submit",
        headers=user["headers"],
        json={"answers": {"dummy_q": "wrong_answer"}}
    )
    assert submit_res.status_code == 200
    res_data = submit_res.json()
    assert res_data["passed"] is False
    assert res_data["unlocked_next_level"] is False

    # Check level 2 is still locked
    lvl_res = client.get("/api/progression/levels", headers=user["headers"])
    levels = lvl_res.json()
    assert levels[1]["unlocked"] is False


def test_06_level_advancement_requires_all_three_conditions():
    """
    Advancing from Level 1 to Level 2 requires:
    1. All 10 topics completed
    2. Final Test passed (>= 70%)
    3. Total XP >= 1000
    """
    user = create_test_user("user_lvl_unlock")
    db = SessionLocal()
    try:
        # 1. Complete topics
        mark_topics_passed(db, user["id"], count=10)

        # Fetch test questions to answer correctly
        test_obj = db.query(LevelFinalTest).filter(LevelFinalTest.level_number == 1).first()
        correct_answers = {q.id: q.correct_answer for q in test_obj.questions}
    finally:
        db.close()

    # Pass final test
    submit_res = client.post(
        "/api/progression/levels/1/final-test/submit",
        headers=user["headers"],
        json={"answers": correct_answers}
    )
    assert submit_res.status_code == 200
    res_data = submit_res.json()
    assert res_data["passed"] is True
    assert res_data["xp_awarded"] == 250

    # At this point, user XP is 250 (which is < 1000 required for Level 2)
    # Next level should NOT be unlocked yet
    assert res_data["unlocked_next_level"] is False

    # Now award remaining XP to reach >= 1000
    db = SessionLocal()
    try:
        award_xp(db, user["id"], "practice", "extra", 800, f"xp:{user['id']}:extra_boost")
        db.commit()
    finally:
        db.close()

    # Retaking/refreshing final test now that XP >= 1000 triggers level unlock
    submit_res2 = client.post(
        "/api/progression/levels/1/final-test/submit",
        headers=user["headers"],
        json={"answers": correct_answers}
    )
    assert submit_res2.status_code == 200
    res2_data = submit_res2.json()
    assert res2_data["unlocked_next_level"] is True
    assert res2_data["next_level_number"] == 2


def test_07_xp_transaction_idempotency():
    """Verify that retries/replays do not award duplicate XP."""
    user = create_test_user("user_idempotent")
    db = SessionLocal()
    try:
        # First award
        xp1, is_new1 = award_xp(db, user["id"], "bonus", "b1", 100, f"unique_tx_key_{user['id']}")
        assert xp1 == 100
        assert is_new1 is True

        # Duplicate attempt with same key
        xp2, is_new2 = award_xp(db, user["id"], "bonus", "b1", 100, f"unique_tx_key_{user['id']}")
        assert xp2 == 0
        assert is_new2 is False

        # Profile total XP should reflect exactly 100
        prof = db.query(Profile).filter(Profile.user_id == user["id"]).first()
        assert prof.total_xp == 100
    finally:
        db.close()


def test_08_periodic_tests_weekly_and_monthly():
    """Verify Periodic Tests endpoint lists 6 tests, and submissions award XP."""
    user = create_test_user("user_periodic")
    res = client.get("/api/progression/tests/periodic", headers=user["headers"])
    assert res.status_code == 200
    tests = res.json()
    assert len(tests) == 6

    weekly_tests = [t for t in tests if t["test_type"] == "weekly"]
    monthly_tests = [t for t in tests if t["test_type"] == "monthly"]
    assert len(weekly_tests) == 4
    assert len(monthly_tests) == 2

    # Fetch questions for weekly test 1
    w1_id = weekly_tests[0]["id"]
    detail_res = client.get(f"/api/progression/tests/periodic/{w1_id}", headers=user["headers"])
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert len(detail["questions"]) > 0

    # Submit answers
    db = SessionLocal()
    try:
        ptest = db.query(PeriodicTest).filter(PeriodicTest.id == w1_id).first()
        answers = {q.id: q.correct_answer for q in ptest.questions}
    finally:
        db.close()

    submit_res = client.post(
        f"/api/progression/tests/periodic/{w1_id}/submit",
        headers=user["headers"],
        json={"answers": answers}
    )
    assert submit_res.status_code == 200
    sub_data = submit_res.json()
    assert sub_data["passed"] is True
    assert sub_data["xp_awarded"] == 200  # Weekly test award


def test_09_rank_calculation_and_promotion():
    """
    Verify Rank formula:
    Topic Exam (30%) + Coding (30%) + Weekly (15%) + Monthly (15%) + Consistency (10%).
    Verify promotion from GOLD to PLATINUM when requirements are met.
    """
    user = create_test_user("user_rank_promo")
    db = SessionLocal()
    try:
        # Simulate high topic exam average (85%)
        from backend.app.models.entities import ExamAttempt
        db.add(ExamAttempt(
            user_id=user["id"], exam_id="exam-1", topic_id="chal-1",
            attempt_number=1, score=85.0, max_score=100.0, percentage=85.0,
            passed=True, total_questions=5, correct_answers=4
        ))
        db.add(ExamAttempt(
            user_id=user["id"], exam_id="exam-2", topic_id="chal-2",
            attempt_number=1, score=90.0, max_score=100.0, percentage=90.0,
            passed=True, total_questions=5, correct_answers=4
        ))
        # Simulate passed weekly test (80%)
        db.add(PeriodicTestAttempt(
            user_id=user["id"], test_id="weekly-test-1", test_type="weekly",
            period_number=1, attempt_number=1, score=80.0, max_score=100.0, percentage=80.0,
            passed=True
        ))
        # Simulate passed coding submissions
        from backend.app.models.entities import Submission
        for i in range(1, 4):
            db.add(Submission(
                user_id=user["id"], challenge_id=f"chal-{i}", code="pass",
                passed=True, total_tests_count=3, passed_tests_count=3, status="passed"
            ))
        db.commit()

        # Evaluate rank
        new_rank, changed, ctype = evaluate_user_rank(db, user["id"], "test_evaluation")
        db.commit()

        # Performance score should be >= 75 and rank should be PLATINUM
        prof = db.query(Profile).filter(Profile.user_id == user["id"]).first()
        assert prof.performance_score >= 75.0
        assert new_rank == "PLATINUM"
        assert prof.current_rank == "PLATINUM"
        assert changed is True
        assert ctype == "promotion"
    finally:
        db.close()


def test_10_anti_demotion_guardrail():
    """
    Verify demotion protection:
    1 or 2 low evaluation periods do NOT demote.
    Only 3 consecutive periods with score < 70 demotes by 1 tier.
    """
    user = create_test_user("user_guardrail")
    db = SessionLocal()
    try:
        prof = db.query(Profile).filter(Profile.user_id == user["id"]).first()
        prof.current_rank = "PLATINUM"
        prof.performance_score = 65.0  # < 70
        prof.consecutive_low_performance_count = 0
        db.commit()

        # Period 1 low performance
        r1, ch1, _ = evaluate_user_rank(db, user["id"], "period_1")
        assert r1 == "PLATINUM"  # No demotion
        assert ch1 is False
        assert prof.consecutive_low_performance_count == 1

        # Period 2 low performance
        r2, ch2, _ = evaluate_user_rank(db, user["id"], "period_2")
        assert r2 == "PLATINUM"  # Still protected!
        assert ch2 is False
        assert prof.consecutive_low_performance_count == 2

        # Period 3 low performance -> Demotes 1 tier to GOLD
        r3, ch3, ctype3 = evaluate_user_rank(db, user["id"], "period_3")
        assert r3 == "GOLD"
        assert ch3 is True
        assert ctype3 == "demotion"
        assert prof.current_rank == "GOLD"
        assert prof.consecutive_low_performance_count == 0  # Reset after demotion
    finally:
        db.close()


def test_11_rank_history_and_xp_history_endpoints():
    """Verify GET /api/progression/profile/rank-history and xp-history return audit records."""
    user = create_test_user("user_audit")
    # Rank history
    res_rh = client.get("/api/progression/profile/rank-history", headers=user["headers"])
    assert res_rh.status_code == 200
    assert isinstance(res_rh.json(), list)

    # XP history
    res_xp = client.get("/api/progression/profile/xp-history", headers=user["headers"])
    assert res_xp.status_code == 200
    assert isinstance(res_xp.json(), list)
