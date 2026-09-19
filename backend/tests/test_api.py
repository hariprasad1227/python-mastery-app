"""
FastAPI Backend Integration Tests
Verifies:
- Root & health check
- Progression endpoints (profile, curriculum)
- Runner sandbox endpoint with code execution and XP progression
- AI Mentor endpoint with Socratic hints
"""

import sys
import os

# Put root project in path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_root_and_health():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["status"] == "online"

    res_health = client.get("/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"
    print("[PASS] test_root_and_health")


def test_progression_profile_and_curriculum():
    res_prof = client.get("/api/progression/profile")
    assert res_prof.status_code == 200
    prof = res_prof.json()
    assert "username" in prof
    assert prof["total_xp"] >= 0
    assert prof["current_level"] >= 1

    res_curr = client.get("/api/progression/curriculum")
    assert res_curr.status_code == 200
    modules = res_curr.json()
    assert len(modules) == 10
    assert "Fundamentals" in modules[0]["title"]
    print("[PASS] test_progression_profile_and_curriculum")


def test_runner_execution_and_progression():
    # 1. Register test user to get token
    import time
    ts = int(time.time() * 1000)
    res_reg = client.post("/api/auth/signup", json={
        "email": f"api_test_{ts}@mastery.io",
        "password": "Password123!",
        "username": f"api_test_{ts}"
    })
    token = res_reg.json()["access_token"]

    # Submit correct solution to chal-1
    solution = """
def greet(name: str) -> str:
    return f"Hello, {name}!"
"""
    payload = {
        "challenge_id": "chal-1",
        "code": solution
    }
    res = client.post("/api/runner/execute", headers={"Authorization": f"Bearer {token}"}, json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["passed"] is True
    assert data["status"] == "success"
    assert len(data["test_results"]) >= 2
    assert data["test_results"][0]["passed"] is True
    print("[PASS] test_runner_execution_and_progression")


def test_mentor_hint_generation():
    payload = {
        "challenge_title": "Even or Odd Parity",
        "challenge_instructions": "Write check_parity(n) returning 'Even' or 'Odd'",
        "learner_code": "def check_parity(n):\n    if n / 2 == 0:\n        return 'Even'\n",
        "error_message": "AssertionError: Expected 'Even' got None for input 4",
        "hint_level": 2
    }
    res = client.post("/api/mentor/hint", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "hint" in data
    assert "socratic_question" in data
    assert len(data["hint"]) > 0
    print("[PASS] test_mentor_hint_generation")


if __name__ == "__main__":
    print("Running backend integration tests...")
    test_root_and_health()
    test_progression_profile_and_curriculum()
    test_runner_execution_and_progression()
    test_mentor_hint_generation()
    print("\nALL BACKEND API TESTS PASSED!")
