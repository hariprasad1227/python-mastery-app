"""
Verification of Complete Exam-Gated Flow against Live Backend API Server
"""

import sys
import os
import requests
import json
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

BASE_URL = "http://127.0.0.1:8000/api"

def run_live_verification():
    print("=========================================================")
    print("LIVE INTEGRATION TEST: TOPIC-WISE EXAM GATED UNLOCK SYSTEM")
    print("=========================================================")

    ts = int(time.time())
    email_a = f"exam_learner_{ts}@test.com"
    pwd = "SecurePassword123!"

    # 1. Register User A
    print("\n[Step 1] Registering User A...")
    res = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email_a,
        "password": pwd,
        "username": f"learner_{ts}",
        "display_name": "Exam Master Learner"
    })
    assert res.status_code == 200, f"Signup failed: {res.text}"
    token_a = res.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}
    print(f"  [OK] User A registered successfully.")

    # 2. Check initial curriculum: chal-1 is available, chal-2 is locked
    print("\n[Step 2] Verifying initial curriculum status...")
    res_curr = requests.get(f"{BASE_URL}/progression/curriculum", headers=headers_a)
    assert res_curr.status_code == 200
    curr_data = res_curr.json()
    
    chal1_meta = next((c for m in curr_data for c in m["challenges"] if c["id"] == "chal-1"), None)
    chal2_meta = next((c for m in curr_data for c in m["challenges"] if c["id"] == "chal-2"), None)
    
    assert chal1_meta is not None and chal1_meta["status"] in ["available", "in_progress"]
    assert chal2_meta is not None and chal2_meta["status"] == "locked"
    print(f"  [OK] Topic 1 status: '{chal1_meta['status']}'")
    print(f"  [OK] Topic 2 status: '{chal2_meta['status']}' (Locked as expected)")

    # 3. Direct URL access to chal-2 must be rejected with 403 Forbidden
    print("\n[Step 3] Verifying server rejection for locked Topic 2...")
    res_chal2_direct = requests.get(f"{BASE_URL}/progression/challenges/chal-2", headers=headers_a)
    assert res_chal2_direct.status_code == 403, f"Expected 403, got {res_chal2_direct.status_code}"
    lock_data = res_chal2_direct.json()["detail"]
    assert lock_data["locked"] is True
    assert lock_data["prerequisite_topic_id"] == "chal-1"
    print(f"  [OK] Server-side 403 Forbidden enforced: \"{lock_data['message']}\"")

    # 4. Check unlock-status endpoint for chal-2
    print("\n[Step 4] Checking unlock-status endpoint for Topic 2...")
    res_status2 = requests.get(f"{BASE_URL}/progression/topics/chal-2/unlock-status", headers=headers_a)
    assert res_status2.status_code == 200
    st2 = res_status2.json()
    assert st2["is_unlocked"] is False
    assert st2["status"] == "locked"
    print(f"  [OK] Unlock-status correctly reports Topic 2 is_unlocked=False")

    # 5. Run Python code for chal-1 to complete practice
    print("\n[Step 5] Running code challenge solution for Topic 1...")
    sol1 = "def greet(name: str) -> str:\n    return f'Hello, {name}!'"
    res_run1 = requests.post(f"{BASE_URL}/runner/execute", headers=headers_a, json={
        "challenge_id": "chal-1",
        "code": sol1
    })
    assert res_run1.status_code == 200
    run_json = res_run1.json()
    assert run_json["passed"] is True
    assert run_json["unlocked_next"] is False  # Must NOT unlock next topic yet!
    print(f"  [OK] Code passed 100%! +{run_json['xp_earned']} XP earned.")
    print(f"  [OK] unlocked_next is False (Exam required for gated unlock)")

    # 6. Complete Lesson for chal-1
    print("\n[Step 6] Completing lesson for Topic 1...")
    res_lesson = requests.post(f"{BASE_URL}/progression/topics/chal-1/complete-lesson", headers=headers_a)
    assert res_lesson.status_code == 200
    les_data = res_lesson.json()
    assert les_data["status"] == "exam_available"
    print(f"  [OK] Lesson completed: topic status transitioned to '{les_data['status']}'")

    # Topic 2 MUST still be locked!
    res_chal2_still_locked = requests.get(f"{BASE_URL}/progression/challenges/chal-2", headers=headers_a)
    assert res_chal2_still_locked.status_code == 403
    print(f"  [OK] Topic 2 remains strictly locked (exam not yet taken)")

    # 7. Fetch Exam for chal-1
    print("\n[Step 7] Fetching Topic 1 Exam...")
    res_exam = requests.get(f"{BASE_URL}/progression/topics/chal-1/exam", headers=headers_a)
    assert res_exam.status_code == 200
    exam = res_exam.json()
    exam_id = exam["id"]
    questions = exam["questions"]
    assert len(questions) == 5, f"Expected 5 questions, got {len(questions)}"
    print(f"  [OK] Exam loaded: '{exam['title']}' ({len(questions)} questions, Pass Mark: {exam['passing_percentage']}%)")
    
    # Verify answers and explanations are stripped from client
    for q in questions:
        assert "correct_answer" not in q
        assert "explanation" not in q
    print(f"  [OK] Security verified: answers & explanations stripped from client payload.")

    # 8. Submit FAILING exam attempt (< 70%)
    print("\n[Step 8] Submitting failing exam attempt (score < 70%)...")
    fail_answers = {q["id"]: "WRONG_ANSWER_CHOICE" for q in questions}
    res_fail_submit = requests.post(f"{BASE_URL}/progression/exams/{exam_id}/submit", headers=headers_a, json={
        "answers": fail_answers
    })
    assert res_fail_submit.status_code == 200
    fail_res = res_fail_submit.json()
    assert fail_res["passed"] is False
    assert fail_res["score"] == 0
    assert fail_res["percentage"] == 0.0
    print(f"  [OK] Exam evaluated: Score={fail_res['score']}/{fail_res['total_points']} ({fail_res['percentage']}%) -> Passed={fail_res['passed']}")

    # Topic 2 MUST still be locked!
    res_chal2_after_fail = requests.get(f"{BASE_URL}/progression/challenges/chal-2", headers=headers_a)
    assert res_chal2_after_fail.status_code == 403
    print(f"  [OK] Topic 2 remains strictly locked after failed exam attempt.")

    # 9. Query DB for correct answers to simulate learner studying and getting passing score
    from backend.app.models.entities import ExamQuestion, ExamAttempt, ExamAnswer
    from backend.app.db.session import SessionLocal
    db = SessionLocal()
    correct_qs = db.query(ExamQuestion).filter(ExamQuestion.exam_id == exam_id).all()
    correct_dict = {q.id: q.correct_answer for q in correct_qs}
    db.close()

    # 10. Submit PASSING exam attempt (100% >= 70%)
    print("\n[Step 9] Submitting passing exam attempt (100% score)...")
    res_pass_submit = requests.post(f"{BASE_URL}/progression/exams/{exam_id}/submit", headers=headers_a, json={
        "answers": correct_dict
    })
    assert res_pass_submit.status_code == 200
    pass_res = res_pass_submit.json()
    assert pass_res["passed"] is True
    assert pass_res["percentage"] == 100.0
    assert pass_res["next_unlocked_topic_id"] == "chal-2"
    assert pass_res["attempt_number"] == 2  # Second attempt
    print(f"  [OK] Exam passed on attempt #2! Score={pass_res['score']}/{pass_res['total_points']} (100%)")
    print(f"  [OK] Next unlocked topic: '{pass_res['next_unlocked_topic_id']}' (+{pass_res['xp_awarded']} XP)")

    # 11. Now Topic 2 MUST be UNLOCKED!
    print("\n[Step 10] Verifying Topic 2 is now unlocked and accessible...")
    res_chal2_unlocked = requests.get(f"{BASE_URL}/progression/challenges/chal-2", headers=headers_a)
    assert res_chal2_unlocked.status_code == 200, f"Failed to access Topic 2: {res_chal2_unlocked.text}"
    chal2_data = res_chal2_unlocked.json()
    assert chal2_data["id"] == "chal-2"
    print(f"  [OK] Topic 2 ('{chal2_data['title']}') successfully unlocked and accessed!")

    # 12. Check User Isolation: User B MUST have Topic 2 LOCKED!
    print("\n[Step 11] Verifying User Isolation (User B must NOT have Topic 2 unlocked)...")
    email_b = f"exam_learner_b_{ts}@test.com"
    res_b = requests.post(f"{BASE_URL}/auth/signup", json={
        "email": email_b,
        "password": pwd,
        "username": f"learner_b_{ts}",
        "display_name": "User B"
    })
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    res_b_chal2 = requests.get(f"{BASE_URL}/progression/challenges/chal-2", headers=headers_b)
    assert res_b_chal2.status_code == 403, "User B should not have Topic 2 unlocked!"
    print(f"  [OK] User Isolation confirmed: Topic 2 is locked (403) for User B.")

    # 13. Verify Database Attempt and Answer Records
    print("\n[Step 12] Verifying DB persistence of attempts and answers...")
    db = SessionLocal()
    attempts = db.query(ExamAttempt).filter(ExamAttempt.exam_id == exam_id).all()
    assert len(attempts) >= 2
    last_att = attempts[-1]
    answers_saved = db.query(ExamAnswer).filter(ExamAnswer.attempt_id == last_att.id).all()
    assert len(answers_saved) == 5
    db.close()
    print(f"  [OK] DB records verified: {len(attempts)} attempts and {len(answers_saved)} answer records persisted.")

    print("\n=========================================================")
    print("ALL 12 TOPIC-WISE EXAM GATING VERIFICATIONS PASSED 100%!")
    print("=========================================================")

if __name__ == "__main__":
    run_live_verification()
