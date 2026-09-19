"""
Python Mastery - End-to-End System Integration & Feature Verification
Tests:
1. Health check & database connection
2. Full 10-track 100-level curriculum navigation
3. 4 Practical Projects catalog & automated verification harness
4. 10 DSA Interview Arena catalog & automated edge-case submission harness
5. Authoritative submission runner with sandbox execution
"""

import urllib.request
import json
import sys

BASE = "http://127.0.0.1:8000"

def test_all():
    print("--- Starting Python Mastery Complete Verification ---")

    # 1. Health check
    res = urllib.request.urlopen(f"{BASE}/health")
    health = json.loads(res.read().decode())
    assert health["status"] == "healthy", f"Health failed: {health}"
    print("[PASS] 1. Health Check (/health): status=healthy")

    # 2. Database Health
    res = urllib.request.urlopen(f"{BASE}/health/db")
    db_health = json.loads(res.read().decode())
    assert db_health["database"] == "connected"
    print("[PASS] 2. Database Health (/health/db): connected")

    # 3. Sandbox Health
    res = urllib.request.urlopen(f"{BASE}/health/sandbox")
    sb_health = json.loads(res.read().decode())
    assert sb_health["sandbox"] == "operational"
    print("[PASS] 3. Sandbox Health (/health/sandbox): operational")

    # 4. Curriculum
    res = urllib.request.urlopen(f"{BASE}/api/progression/curriculum")
    curr = json.loads(res.read().decode())
    total_challenges = sum(len(m["challenges"]) for m in curr)
    assert len(curr) == 10, f"Expected 10 tracks, got {len(curr)}"
    assert total_challenges == 100, f"Expected 100 challenges, got {total_challenges}"
    print(f"[PASS] 4. Curriculum (/api/progression/curriculum): 10 Tracks, 100 Levels verified")

    # 5. Projects Catalog
    res = urllib.request.urlopen(f"{BASE}/api/projects")
    projs = json.loads(res.read().decode())
    assert len(projs) == 4, f"Expected 4 projects, got {len(projs)}"
    print(f"[PASS] 5. Practical Projects (/api/projects): 4 Capstones loaded")

    # 6. Projects Verification Test (CLI Task Manager)
    p1 = projs[0]
    payload = json.dumps({"project_id": p1["id"], "code": p1["starter_code"]}).encode()
    req = urllib.request.Request(
        f"{BASE}/api/projects/{p1['id']}/verify",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    v_res = json.loads(res.read().decode())
    assert v_res["passed"] is True, f"Project 1 verification failed: {v_res}"
    print(f"[PASS] 6. Project Verification (/api/projects/proj-1/verify): TaskManager verified in sandbox")

    # 7. Interview Arena Catalog
    res = urllib.request.urlopen(f"{BASE}/api/interview/problems")
    interviews = json.loads(res.read().decode())
    assert len(interviews) == 10, f"Expected 10 interview problems, got {len(interviews)}"
    print(f"[PASS] 7. Interview Arena (/api/interview/problems): 10 Top-Tier DSA Problems loaded")

    # 8. Interview Problem Submission Test (Two Sum)
    i1 = interviews[0]
    payload = json.dumps({"problem_id": i1["id"], "code": i1["starter_code"]}).encode()
    req = urllib.request.Request(
        f"{BASE}/api/interview/{i1['id']}/submit",
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(req)
    i_res = json.loads(res.read().decode())
    assert i_res["passed"] is True, f"Interview 1 verification failed: {i_res}"
    print(f"[PASS] 8. Interview Submission (/api/interview/interview-1/submit): Two Sum verified against edge cases")

    # 9. Curriculum Challenge Submission Test with JWT Authentication
    auth_req = urllib.request.Request(
        f"{BASE}/api/auth/signup",
        data=json.dumps({
            "email": "integration_tester@example.com",
            "password": "SecurePassword123!",
            "username": "integration_tester",
            "display_name": "Integration Tester"
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    try:
        auth_res = urllib.request.urlopen(auth_req)
        token = json.loads(auth_res.read().decode())["access_token"]
    except urllib.error.HTTPError:
        # Already registered, log in
        login_req = urllib.request.Request(
            f"{BASE}/api/auth/login",
            data=json.dumps({
                "email": "integration_tester@example.com",
                "password": "SecurePassword123!"
            }).encode(),
            headers={"Content-Type": "application/json"}
        )
        auth_res = urllib.request.urlopen(login_req)
        token = json.loads(auth_res.read().decode())["access_token"]

    payload = json.dumps({
        "challenge_id": "chal-1",
        "code": "def greet(name: str) -> str:\n    return f'Hello, {name}!'"
    }).encode()
    req = urllib.request.Request(
        f"{BASE}/api/runner/execute",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    )
    res = urllib.request.urlopen(req)
    c_res = json.loads(res.read().decode())
    assert c_res["passed"] is True, f"Challenge 1 verification failed: {c_res}"
    print(f"[PASS] 9. Runner Execution (/api/runner/execute): chal-1 verified in AST-guarded sandbox with JWT auth")

    print("\n==================================================")
    print("ALL 9 VERIFICATION GATES PASSED WITH 100% SUCCESS!")
    print("==================================================")

if __name__ == "__main__":
    test_all()
