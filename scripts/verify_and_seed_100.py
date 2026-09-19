import json
import os
import sys

# Ensure root in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from runner.runner import execute_learner_code
from backend.app.db.session import SessionLocal
from backend.app.models.entities import Challenge, User, UserProgress

def load_all_100():
    all_challenges = []
    files = [
        "scripts/track1.json",
        "scripts/track2_3.json",
        "scripts/track4_5.json",
        "scripts/track6_7.json",
        "scripts/track8.json",
        "scripts/track9.json",
        "scripts/track10.json"
    ]
    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
            all_challenges.extend(data)
    return all_challenges

def main():
    challenges = load_all_100()
    print(f"Loaded {len(challenges)} total curriculum challenges.")
    assert len(challenges) == 100, f"Expected 100 challenges, got {len(challenges)}"

    print("Verifying all 100 canonical solutions against their test cases in the sandbox...")
    failed_count = 0
    for idx, ch in enumerate(challenges, start=1):
        sol = ch["solution_code"]
        func = ch["entry_function_name"]
        tests = ch["test_cases"]
        res = execute_learner_code(code=sol, entry_function_name=func, test_cases=tests, timeout_seconds=3.0)
        if not res.get("passed"):
            print(f"  [FAIL] Challenge {idx} ({ch['title']}) failed verification: {res.get('stderr')}")
            failed_count += 1
        else:
            if idx % 10 == 0:
                print(f"  [OK] Verified {idx}/100 challenges passed cleanly...")

    if failed_count > 0:
        print(f"ABORTING: {failed_count} challenges failed their own tests!")
        sys.exit(1)

    print("\nALL 100 CANONICAL SOLUTIONS VERIFIED SUCCESSFULLY IN SANDBOX!")
    print("Seeding all 100 challenges into the database...")

    with SessionLocal() as db:
        # Upsert challenges
        for ch in challenges:
            existing = db.query(Challenge).filter(Challenge.id == ch["id"]).first()
            if existing:
                existing.slug = ch["slug"]
                existing.title = ch["title"]
                existing.level_number = ch["level_number"]
                existing.order_index = ch["order_index"]
                existing.difficulty = ch["difficulty"]
                existing.instructions = ch["instructions"]
                existing.starter_code = ch["starter_code"]
                existing.solution_code = ch["solution_code"]
                existing.entry_function_name = ch["entry_function_name"]
                existing.test_cases_json = json.dumps(ch["test_cases"])
                existing.hints_json = json.dumps(ch["hints"])
                existing.xp_reward = ch["xp_reward"]
                existing.time_limit_seconds = ch["time_limit_seconds"]
                existing.sandbox_timeout_seconds = ch["sandbox_timeout_seconds"]
            else:
                db_ch = Challenge(
                    id=ch["id"],
                    slug=ch["slug"],
                    title=ch["title"],
                    level_number=ch["level_number"],
                    order_index=ch["order_index"],
                    difficulty=ch["difficulty"],
                    instructions=ch["instructions"],
                    starter_code=ch["starter_code"],
                    solution_code=ch["solution_code"],
                    entry_function_name=ch["entry_function_name"],
                    test_cases_json=json.dumps(ch["test_cases"]),
                    hints_json=json.dumps(ch["hints"]),
                    xp_reward=ch["xp_reward"],
                    time_limit_seconds=ch["time_limit_seconds"],
                    sandbox_timeout_seconds=ch["sandbox_timeout_seconds"]
                )
                db.add(db_ch)
        db.commit()

        # Update all existing users with user_progress entries for all 100 challenges
        users = db.query(User).all()
        for u in users:
            existing_cids = {p.challenge_id for p in db.query(UserProgress).filter(UserProgress.user_id == u.id).all()}
            for ch in challenges:
                if ch["id"] not in existing_cids:
                    db.add(UserProgress(
                        user_id=u.id,
                        challenge_id=ch["id"],
                        status="locked",
                        attempts_count=0,
                        earned_xp=0
                    ))
        db.commit()
        count = db.query(Challenge).count()
        print(f"SUCCESS: Database now contains {count} active curriculum challenges!")

if __name__ == "__main__":
    main()
