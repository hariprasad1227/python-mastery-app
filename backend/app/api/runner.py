"""
Production Runner API Router
Executes learner code against official server-side test cases, enforces challenge unlocking,
tracks attempt duration, and persists submissions, XP, and badges to the database.
"""

import json
import time
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import (
    User, Challenge, UserProgress, Attempt, Submission,
    XPTransaction, Badge, UserBadge
)
from backend.app.core.security import get_current_user, check_rate_limit
from backend.app.schemas.runner import ExecuteRequest, ExecuteResponse, TestResultItem
from runner.runner import execute_learner_code
from backend.app.core.xp_service import award_xp
from backend.app.core.rank_engine import evaluate_user_rank

router = APIRouter(tags=["runner"])


async def handle_code_execution(
    request: ExecuteRequest,
    current_user: User,
    db: Session
) -> ExecuteResponse:
    """
    Core handler for executing learner code with strict server-side validation:
    1. Rate limit check.
    2. Authenticates learner via JWT.
    3. Loads official challenge from database.
    4. Enforces problem unlocking rules (returns 403 if locked).
    5. Enforces attempt time limit (returns 400 if expired).
    6. Runs code with official server-controlled test cases & sandbox timeout.
    7. Persists submission audit log and updates XP, streak, and badges.
    """
    # 1. Rate limiting check
    check_rate_limit(db, key=current_user.id, action="code_execution", max_requests=40, window_seconds=60)

    # 2. Retrieve official challenge
    challenge = db.query(Challenge).filter(Challenge.id == request.challenge_id).first()
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Challenge '{request.challenge_id}' not found."
        )

    # 3. Enforce server-side unlocking rules
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.challenge_id == challenge.id
    ).first()

    if not progress or progress.status == "locked":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Challenge '{challenge.title}' is locked. You must complete prerequisite challenges first."
        )

    # 4. Handle attempt and server-side timer validation
    attempt: Optional[Attempt] = None
    now = datetime.utcnow()
    attempt_duration = 0

    if request.attempt_id:
        attempt = db.query(Attempt).filter(
            Attempt.id == request.attempt_id,
            Attempt.user_id == current_user.id
        ).first()

    if not attempt:
        # Check if there is an active in_progress attempt
        attempt = db.query(Attempt).filter(
            Attempt.user_id == current_user.id,
            Attempt.challenge_id == challenge.id,
            Attempt.status == "in_progress"
        ).order_by(Attempt.started_at.desc()).first()

    if attempt:
        elapsed = (now - attempt.started_at).total_seconds()
        attempt_duration = int(elapsed)
        if attempt.time_limit_seconds > 0 and elapsed > attempt.time_limit_seconds:
            attempt.status = "expired"
            attempt.duration_seconds = attempt_duration
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Attempt timed out. Allowed time: {attempt.time_limit_seconds}s, elapsed: {attempt_duration}s."
            )
        attempt.status = "completed"
        attempt.submitted_at = now
        attempt.duration_seconds = attempt_duration
    elif request.attempt_started_at:
        attempt_duration = max(0, int(time.time() - request.attempt_started_at))

    # 5. Retrieve official server test cases and server-controlled timeout
    official_test_cases = json.loads(challenge.test_cases_json) if challenge.test_cases_json else []
    entry_function_name = challenge.entry_function_name
    timeout_seconds = challenge.sandbox_timeout_seconds or 3.0

    # 6. Execute in isolated sandbox
    raw_result = execute_learner_code(
        code=request.code,
        entry_function_name=entry_function_name,
        test_cases=official_test_cases,
        timeout_seconds=timeout_seconds
    )

    passed = raw_result.get("passed", False)
    stdout_text = raw_result.get("stdout", "")
    stderr_text = raw_result.get("stderr", "")
    execution_time_ms = raw_result.get("execution_time_ms", 0)
    raw_tests = raw_result.get("test_results", [])

    passed_count = sum(1 for tr in raw_tests if tr.get("passed", False))
    total_count = len(raw_tests)

    # 7. Format test result items, SANITIZING hidden tests so secrets/assertions do not leak
    formatted_results = []
    for tr in raw_tests:
        is_hidden = tr.get("is_hidden", False)
        if is_hidden:
            formatted_results.append(
                TestResultItem(
                    test_index=tr.get("test_index", 0),
                    description="Hidden Verification Test",
                    is_hidden=True,
                    passed=tr.get("passed", False),
                    input="[Hidden Input]",
                    expected="[Hidden Expected Value]",
                    actual="[Passed]" if tr.get("passed") else "[Failed]",
                    error=None if tr.get("passed") else "Hidden test assertion failed"
                )
            )
        else:
            formatted_results.append(
                TestResultItem(
                    test_index=tr.get("test_index", 0),
                    description=tr.get("description", ""),
                    is_hidden=False,
                    passed=tr.get("passed", False),
                    input=tr.get("input"),
                    expected=tr.get("expected"),
                    actual=tr.get("actual"),
                    error=tr.get("error")
                )
            )

    # 8. Persist submission into database
    submission = Submission(
        user_id=current_user.id,
        challenge_id=challenge.id,
        attempt_id=attempt.id if attempt else None,
        code=request.code,
        passed=passed,
        passed_tests_count=passed_count,
        total_tests_count=total_count,
        status=raw_result.get("status", "completed"),
        stdout=stdout_text,
        stderr=stderr_text,
        execution_time_ms=execution_time_ms,
        attempt_duration_seconds=attempt_duration
    )
    db.add(submission)
    progress.attempts_count += 1

    xp_earned = 0
    unlocked_next = False
    new_badges: List[str] = []
    profile = current_user.profile

    # 9. Update progression and XP on code pass
    if passed:
        progress.practice_completed = True
        if progress.status != "passed":
            if progress.lesson_completed:
                progress.status = "exam_available"
            else:
                progress.status = "in_progress"

        # Single XP award check via idempotent award_xp
        xp_earned, _ = award_xp(
            db=db,
            user_id=current_user.id,
            source_type="challenge_completion",
            source_id=challenge.id,
            amount=challenge.xp_reward,
            idempotency_key=f"xp:{current_user.id}:challenge:{challenge.id}:pass",
            challenge_id=challenge.id
        )
        if xp_earned > 0:
            progress.earned_xp += xp_earned

        # Streak calculation
        today_str = now.strftime("%Y-%m-%d")
        if profile.last_active_date != today_str:
            profile.current_streak += 1
            if profile.current_streak > profile.longest_streak:
                profile.longest_streak = profile.current_streak
            profile.last_active_date = today_str

        # Note: Unlocking the subsequent topic is strictly gated on PASSING the Topic Exam!
        unlocked_next = False

        # Check and award badges
        # Badge: First Spark
        first_blood_badge = db.query(Badge).filter(Badge.code == "first_blood").first()
        if first_blood_badge:
            has_badge = db.query(UserBadge).filter(
                UserBadge.user_id == current_user.id,
                UserBadge.badge_id == first_blood_badge.id
            ).first()
            if not has_badge:
                db.add(UserBadge(user_id=current_user.id, badge_id=first_blood_badge.id))
                profile.total_xp += first_blood_badge.xp_bonus
                new_badges.append(first_blood_badge.name)

    # Evaluate rank and performance score after coding submission
    new_rank, _, _ = evaluate_user_rank(db, current_user.id, f"challenge_{challenge.title}")

    db.commit()
    db.refresh(submission)
    db.refresh(profile)

    return ExecuteResponse(
        submission_id=submission.id,
        passed=passed,
        stdout=stdout_text,
        stderr=stderr_text,
        execution_time_ms=execution_time_ms,
        attempt_duration_seconds=attempt_duration,
        passed_tests_count=passed_count,
        total_tests_count=total_count,
        test_results=formatted_results,
        status=raw_result.get("status", "completed"),
        xp_earned=xp_earned,
        total_xp=profile.total_xp,
        current_level=profile.current_level,
        current_rank=profile.current_rank,
        performance_score=profile.performance_score,
        new_streak=profile.current_streak,
        unlocked_next=unlocked_next,
        badges_awarded=new_badges
    )


@router.post("/runner/execute", response_model=ExecuteResponse)
async def runner_execute(
    request: ExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await handle_code_execution(request, current_user, db)


@router.post("/submissions", response_model=ExecuteResponse)
async def create_submission(
    request: ExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await handle_code_execution(request, current_user, db)

