"""
Progression API Router
Database-backed endpoints for user profiles, curriculum navigation, challenge details,
submission history, and topic-wise exam gated unlocking.
"""

import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.db.session import get_db
from backend.app.models.entities import (
    User, Challenge, UserProgress, Profile, Badge, UserBadge, Submission,
    Exam, ExamQuestion, ExamAttempt, ExamAnswer, XPTransaction,
    LevelProgress, LevelFinalTest, LevelFinalTestQuestion, LevelFinalTestAttempt, LevelFinalTestAnswer,
    PeriodicTest, PeriodicTestQuestion, PeriodicTestAttempt, RankHistory, PerformanceSnapshot
)
from backend.app.core.security import get_optional_current_user, get_current_user
from backend.app.schemas.progression import UserProfile, ModuleItem, ChallengeSummary, BadgeItem
from backend.app.content.lessons import get_lesson_for_challenge, get_all_track_lessons, TRACK_MASTER_LESSONS
from backend.app.content.structured_lessons import (
    get_structured_lesson_by_challenge,
    get_structured_lesson_by_id,
    list_all_structured_lessons,
)
from backend.app.core.xp_service import award_xp, LEVEL_XP_REQUIREMENTS, XP_REWARDS
from backend.app.core.rank_engine import (
    evaluate_user_rank,
    calculate_performance_components,
    RANKS_ORDER,
    RANK_THRESHOLDS,
)

router = APIRouter(prefix="/progression", tags=["progression"])


@router.get("/profile", response_model=UserProfile)
async def fetch_user_profile(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the learner profile with persistent XP, level, streak, badges, rank, and performance score.
    """
    all_badges = db.query(Badge).all()

    if current_user:
        profile = current_user.profile
        awarded_badge_ids = {
            ub.badge_id for ub in db.query(UserBadge).filter(UserBadge.user_id == current_user.id).all()
        }
        badge_models = [
            BadgeItem(
                code=b.code,
                name=b.name,
                description=b.description,
                icon=b.icon,
                xp_bonus=b.xp_bonus,
                awarded=(b.id in awarded_badge_ids)
            )
            for b in all_badges
        ]
        return UserProfile(
            id=current_user.id,
            username=current_user.username,
            display_name=profile.display_name if profile else current_user.username,
            total_xp=profile.total_xp if profile else 0,
            current_level=profile.current_level if profile else 1,
            current_rank=profile.current_rank if (profile and profile.current_rank) else "GOLD",
            performance_score=float(profile.performance_score) if (profile and profile.performance_score is not None) else 60.0,
            current_streak=profile.current_streak if profile else 0,
            longest_streak=profile.longest_streak if profile else 0,
            badges=badge_models
        )
    else:
        # Default guest/demo profile
        badge_models = [
            BadgeItem(
                code=b.code,
                name=b.name,
                description=b.description,
                icon=b.icon,
                xp_bonus=b.xp_bonus,
                awarded=False
            )
            for b in all_badges
        ]
        return UserProfile(
            id="guest",
            username="guest",
            display_name="Guest Explorer",
            total_xp=0,
            current_level=1,
            current_rank="GOLD",
            performance_score=60.0,
            current_streak=0,
            longest_streak=0,
            badges=badge_models
        )


@router.get("/curriculum", response_model=List[ModuleItem])
async def fetch_curriculum(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the full curriculum structure.
    Determines challenge availability based on SERVER-SIDE exam gating:
    Topic N is locked unless Topic N-1's exam has been passed by current_user.
    """
    challenges = db.query(Challenge).order_by(Challenge.order_index).all()

    progress_map: Dict[str, UserProgress] = {}
    if current_user:
        user_progress_rows = db.query(UserProgress).filter(UserProgress.user_id == current_user.id).all()
        for p in user_progress_rows:
            progress_map[p.challenge_id] = p

    # Build server-authoritative status for each topic
    levels_dict: Dict[int, List[ChallengeSummary]] = {}
    prev_passed = True # Topic 1 is always available initially

    for ch in challenges:
        if current_user:
            p = progress_map.get(ch.id)

            if ch.order_index == 1:
                # First topic
                if p:
                    ch_status = p.status
                else:
                    ch_status = "available"
                # Check if passed for next topic
                prev_passed = (p is not None and p.exam_passed)
            else:
                # Gated on previous topic exam
                if not prev_passed:
                    ch_status = "locked"
                else:
                    if p:
                        ch_status = p.status
                    else:
                        ch_status = "available"
                # Update prev_passed for subsequent challenge
                prev_passed = (p is not None and p.exam_passed)
        else:
            # Guest: only Level 1 is available
            ch_status = "available" if ch.order_index == 1 else "locked"

        hints = json.loads(ch.hints_json) if ch.hints_json else []
        attempts_count = progress_map[ch.id].attempts_count if (current_user and ch.id in progress_map) else 0

        summary = ChallengeSummary(
            id=ch.id,
            slug=ch.slug,
            title=ch.title,
            instructions=ch.instructions,
            starter_code=ch.starter_code,
            entry_function_name=ch.entry_function_name,
            xp_reward=ch.xp_reward,
            status=ch_status,
            attempts_count=attempts_count,
            hints=hints
        )
        levels_dict.setdefault(ch.level_number, []).append(summary)

    level_titles = {
        1: ("track-1-fundamentals", "Module 1: Python Fundamentals", "Variables, expressions, basic strings, numbers, and formatting."),
        2: ("track-2-data-structures", "Module 2: Data Structures Deep Dive", "Lists, sets, tuples, dictionaries, matrices, and chunking."),
        3: ("track-3-control-flow", "Module 3: Control Flow & Functional Python", "Comprehensions, lambdas, generators, filters, and transposition."),
        4: ("track-4-functions-closures", "Module 4: Functions & Recursion", "Default arguments, recursive algorithms, memoization, and closures."),
        5: ("track-5-oop", "Module 5: Object-Oriented Programming", "Classes, inheritance, polymorphism, static/class methods, and dunders."),
        6: ("track-6-error-handling", "Module 6: Error Handling & Resilient Code", "Try-except guards, custom exceptions, validation, and safe parsing."),
        7: ("track-7-algorithms", "Module 7: Algorithms & Problem Solving", "Two-pointer, sliding window, binary search, Kadane's, and stacks."),
        8: ("track-8-text-processing", "Module 8: Text Processing & String Manipulation", "Ciphers, formatting, word wrapping, normalization, and tokens."),
        9: ("track-9-stdlib", "Module 9: Python Standard Library Mastery", "Counter, deque, itertools, math, datetime, and query parameters."),
        10: ("track-10-capstones", "Module 10: Advanced Mastery & Real-World Capstones", "Trie prefix search, LRU cache, rate limiters, RPN evaluator, and state machines.")
    }

    modules: List[ModuleItem] = []
    for lvl_num in sorted(levels_dict.keys()):
        slug, title, desc = level_titles.get(lvl_num, (f"level-{lvl_num}", f"Level {lvl_num}", ""))
        chals = levels_dict[lvl_num]
        all_locked = all(c.status == "locked" for c in chals)
        modules.append(
            ModuleItem(
                id=f"mod-{lvl_num}",
                slug=slug,
                title=title,
                description=desc,
                level_number=lvl_num,
                order_index=lvl_num,
                is_locked=all_locked,
                challenges=chals
            )
        )

    return modules


@router.get("/challenges/{challenge_id}")
async def fetch_challenge_detail(
    challenge_id: str,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns details of a challenge.
    SERVER-SIDE GATING: If order_index > 1 and previous topic exam is not passed,
    strictly raises 403 FORBIDDEN with locked details.
    """
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Gating enforcement
    if challenge.order_index > 1:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": "Topic Locked: Please sign in and pass prerequisite topic exams to access this topic.",
                    "locked": True,
                    "prerequisite_topic_id": None,
                    "prerequisite_topic_title": None,
                    "prerequisite_exam_id": None,
                }
            )

        prev_challenge = db.query(Challenge).filter(Challenge.order_index == challenge.order_index - 1).first()
        if prev_challenge:
            prev_prog = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == prev_challenge.id
            ).first()
            if not prev_prog or not prev_prog.exam_passed:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "message": f"Topic Locked: You must pass the '{prev_challenge.title}' exam before accessing '{challenge.title}'.",
                        "locked": True,
                        "prerequisite_topic_id": prev_challenge.id,
                        "prerequisite_topic_title": prev_challenge.title,
                        "prerequisite_exam_id": f"exam-{prev_challenge.id}",
                    }
                )

    test_cases = json.loads(challenge.test_cases_json) if challenge.test_cases_json else []
    public_tests = [
        {
            "test_index": tc.get("test_index", idx + 1),
            "description": tc.get("description", f"Public Test #{idx + 1}"),
            "input": tc.get("input"),
            "expected": tc.get("expected"),
            "is_hidden": False
        }
        for idx, tc in enumerate(test_cases)
        if not tc.get("is_hidden", False)
    ]

    hints = json.loads(challenge.hints_json) if challenge.hints_json else []
    lesson_data = get_lesson_for_challenge(challenge.id, challenge.title, challenge.level_number)

    # Fetch user progress for this challenge
    user_prog = None
    if current_user:
        user_prog = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.challenge_id == challenge.id
        ).first()
        if not user_prog:
            user_prog = UserProgress(
                user_id=current_user.id,
                challenge_id=challenge.id,
                status="available" if challenge.order_index == 1 else "locked"
            )
            db.add(user_prog)
            db.commit()
            db.refresh(user_prog)

    return {
        "id": challenge.id,
        "slug": challenge.slug,
        "title": challenge.title,
        "difficulty": challenge.difficulty,
        "level_number": challenge.level_number,
        "order_index": challenge.order_index,
        "instructions": challenge.instructions,
        "starter_code": challenge.starter_code,
        "entry_function_name": challenge.entry_function_name,
        "xp_reward": challenge.xp_reward,
        "time_limit_seconds": challenge.time_limit_seconds,
        "timeout_seconds": challenge.time_limit_seconds,
        "sandbox_timeout_seconds": challenge.sandbox_timeout_seconds,
        "test_cases": public_tests,
        "hints": hints,
        "lesson": lesson_data,
        "progress": {
            "status": user_prog.status if user_prog else ("available" if challenge.order_index == 1 else "locked"),
            "lesson_completed": user_prog.lesson_completed if user_prog else False,
            "practice_completed": user_prog.practice_completed if user_prog else False,
            "exam_passed": user_prog.exam_passed if user_prog else False
        }
    }


# ==============================================================================
# TOPIC EXAM GATED UNLOCK ENDPOINTS
# ==============================================================================

@router.get("/topics/{topic_id}/unlock-status")
async def get_topic_unlock_status(
    topic_id: str,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Checks whether topic_id is unlocked for the authenticated user.
    Returns status, prerequisite requirement, and current progress.
    """
    challenge = db.query(Challenge).filter(Challenge.id == topic_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Topic not found")

    if challenge.order_index == 1:
        prog = db.query(UserProgress).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.challenge_id == topic_id
        ).first() if current_user else None

        return {
            "topic_id": topic_id,
            "order_index": challenge.order_index,
            "title": challenge.title,
            "is_unlocked": True,
            "status": prog.status if prog else "available",
            "lesson_completed": prog.lesson_completed if prog else False,
            "practice_completed": prog.practice_completed if prog else False,
            "exam_passed": prog.exam_passed if prog else False,
            "required_exam": None
        }

    if not current_user:
        return {
            "topic_id": topic_id,
            "order_index": challenge.order_index,
            "title": challenge.title,
            "is_unlocked": False,
            "status": "locked",
            "required_exam": "Sign in and pass prerequisite topic exams."
        }

    prev_challenge = db.query(Challenge).filter(Challenge.order_index == challenge.order_index - 1).first()
    prev_prog = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.challenge_id == prev_challenge.id
    ).first() if prev_challenge else None

    is_unlocked = (prev_prog is not None and prev_prog.exam_passed)
    prog = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.challenge_id == topic_id
    ).first()

    return {
        "topic_id": topic_id,
        "order_index": challenge.order_index,
        "title": challenge.title,
        "is_unlocked": is_unlocked,
        "status": prog.status if prog else ("available" if is_unlocked else "locked"),
        "lesson_completed": prog.lesson_completed if prog else False,
        "practice_completed": prog.practice_completed if prog else False,
        "exam_passed": prog.exam_passed if prog else False,
        "required_exam": f"Pass the '{prev_challenge.title}' exam" if (not is_unlocked and prev_challenge) else None
    }


@router.post("/topics/{topic_id}/complete-lesson")
async def complete_topic_lesson(
    topic_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Marks the lesson component of a topic completed.
    Advances topic status to 'exam_available'.
    NOTE: This does NOT unlock the next topic (only passing the exam unlocks).
    """
    challenge = db.query(Challenge).filter(Challenge.id == topic_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Check prerequisite if order_index > 1
    if challenge.order_index > 1:
        prev_ch = db.query(Challenge).filter(Challenge.order_index == challenge.order_index - 1).first()
        if prev_ch:
            prev_p = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == prev_ch.id
            ).first()
            if not prev_p or not prev_p.exam_passed:
                raise HTTPException(status_code=403, detail="Prerequisite topic exam not passed")

    prog = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.challenge_id == topic_id
    ).first()
    if not prog:
        prog = UserProgress(
            user_id=current_user.id,
            challenge_id=topic_id,
            status="available"
        )
        db.add(prog)

    prog.lesson_completed = True
    if prog.status != "passed":
        prog.status = "exam_available"
    prog.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(prog)

    return {
        "topic_id": topic_id,
        "lesson_completed": prog.lesson_completed,
        "practice_completed": prog.practice_completed,
        "exam_passed": prog.exam_passed,
        "status": prog.status
    }


@router.get("/topics/{topic_id}/exam")
async def get_topic_exam(
    topic_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieves the official topic exam and questions for a topic.
    Verifies the topic is unlocked for this user.
    STRICT SECURITY: Strips correct_answer and explanation from response.
    """
    challenge = db.query(Challenge).filter(Challenge.id == topic_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Server check: is topic unlocked?
    if challenge.order_index > 1:
        prev_ch = db.query(Challenge).filter(Challenge.order_index == challenge.order_index - 1).first()
        if prev_ch:
            prev_p = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == prev_ch.id
            ).first()
            if not prev_p or not prev_p.exam_passed:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Topic Locked: Pass the '{prev_ch.title}' exam before accessing this exam."
                )

    exam = db.query(Exam).filter(Exam.topic_id == topic_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found for this topic")

    questions_data = [
        {
            "id": q.id,
            "order_index": q.order_index,
            "prompt": q.question_text,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "code_snippet": q.code_snippet,
            "options": json.loads(q.options_json) if q.options_json else [],
            "points": q.points
        }
        for q in exam.questions
    ]

    return {
        "id": exam.id,
        "topic_id": exam.topic_id,
        "title": exam.title,
        "description": exam.description,
        "passing_percentage": exam.pass_percentage,
        "pass_percentage": exam.pass_percentage,
        "time_limit_minutes": exam.time_limit_minutes,
        "total_questions": len(questions_data),
        "questions": questions_data
    }


class ExamSubmissionRequest(BaseModel):
    answers: Dict[str, str] # question_id -> user_selected_answer


@router.post("/exams/{exam_id}/submit")
async def submit_topic_exam(
    exam_id: str,
    payload: ExamSubmissionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Evaluates topic exam submission server-side.
    1. Authenticates user.
    2. Calculates score & percentage from official DB questions (ignores client scores).
    3. Saves ExamAttempt and question-level ExamAnswer rows.
    4. If percentage >= pass_percentage:
       - marks topic 'passed' (exam_passed = True)
       - unlocks next topic (sets status = 'available')
       - awards +50 Topic Mastery XP
    5. If failed:
       - next topic remains strictly locked
       - allows retry (new ExamAttempt record)
    """
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    challenge = db.query(Challenge).filter(Challenge.id == exam.topic_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Associated topic challenge not found")

    # Security check: verify this topic is actually unlocked for current_user
    if challenge.order_index > 1:
        prev_ch = db.query(Challenge).filter(Challenge.order_index == challenge.order_index - 1).first()
        if prev_ch:
            prev_p = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == prev_ch.id
            ).first()
            if not prev_p or not prev_p.exam_passed:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Prerequisite topic exam not passed")

    now = datetime.utcnow()
    total_score = 0.0
    max_score = 0.0
    correct_count = 0
    question_evals = []

    # 1. Calculate score completely server-side
    for q in exam.questions:
        max_score += q.points
        user_ans = payload.answers.get(q.id, "").strip()
        is_corr = (str(user_ans).lower() == str(q.correct_answer).strip().lower())
        pts = float(q.points) if is_corr else 0.0
        if is_corr:
            total_score += pts
            correct_count += 1

        question_evals.append({
            "question_id": q.id,
            "prompt": q.question_text,
            "question_text": q.question_text,
            "code_snippet": q.code_snippet,
            "user_answer": user_ans,
            "correct_answer": q.correct_answer,
            "is_correct": is_corr,
            "points_awarded": pts,
            "points_earned": pts,
            "max_points": q.points,
            "explanation": q.explanation
        })

    percentage = round((total_score / max_score * 100.0), 1) if max_score > 0 else 0.0
    is_passed = (percentage >= float(exam.pass_percentage))

    # 2. Persist ExamAttempt in database
    prev_attempts_count = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.exam_id == exam.id
    ).count()

    attempt = ExamAttempt(
        user_id=current_user.id,
        exam_id=exam.id,
        topic_id=exam.topic_id,
        attempt_number=prev_attempts_count + 1,
        score=total_score,
        max_score=max_score,
        percentage=percentage,
        passed=is_passed,
        total_questions=len(exam.questions),
        correct_answers=correct_count,
        started_at=now,
        submitted_at=now
    )
    db.add(attempt)
    db.flush()

    # 3. Persist Question-Level ExamAnswers
    for qe in question_evals:
        db.add(ExamAnswer(
            attempt_id=attempt.id,
            question_id=qe["question_id"],
            selected_answer=qe["user_answer"],
            is_correct=qe["is_correct"],
            points_awarded=qe["points_awarded"]
        ))

    # 4. Handle Progression State Transition
    next_topic_title = None
    next_topic_id = None
    xp_awarded = 0

    progress = db.query(UserProgress).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.challenge_id == challenge.id
    ).first()
    if not progress:
        progress = UserProgress(
            user_id=current_user.id,
            challenge_id=challenge.id,
            status="available"
        )
        db.add(progress)

    if is_passed:
        progress.exam_passed = True
        progress.status = "passed"
        progress.completed_at = now

        # UNLOCK NEXT TOPIC IN DATABASE
        next_ch = db.query(Challenge).filter(Challenge.order_index == challenge.order_index + 1).first()
        if next_ch:
            next_p = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == next_ch.id
            ).first()
            if not next_p:
                next_p = UserProgress(
                    user_id=current_user.id,
                    challenge_id=next_ch.id,
                    status="available"
                )
                db.add(next_p)
            elif next_p.status == "locked":
                next_p.status = "available"
            next_topic_title = next_ch.title
            next_topic_id = next_ch.id

        # Award Topic Exam Mastery XP (+100 XP base, +50 XP first attempt bonus) idempotently
        base_awarded, _ = award_xp(
            db=db,
            user_id=current_user.id,
            source_type="topic_exam_pass",
            source_id=exam.id,
            amount=XP_REWARDS.get("TOPIC_EXAM_PASS", 100),
            idempotency_key=f"xp:{current_user.id}:topic_exam:{exam.id}:pass",
            challenge_id=challenge.id
        )
        xp_awarded += base_awarded

        if attempt.attempt_number == 1:
            bonus_awarded, _ = award_xp(
                db=db,
                user_id=current_user.id,
                source_type="topic_exam_first_attempt_bonus",
                source_id=exam.id,
                amount=XP_REWARDS.get("TOPIC_EXAM_FIRST_ATTEMPT_BONUS", 50),
                idempotency_key=f"xp:{current_user.id}:topic_exam:{exam.id}:first_attempt_bonus",
                challenge_id=challenge.id
            )
            xp_awarded += bonus_awarded

        # Update LevelProgress for this level
        level_num = ((challenge.order_index - 1) // 10) + 1
        lvl_prog = db.query(LevelProgress).filter(
            LevelProgress.user_id == current_user.id,
            LevelProgress.level_number == level_num
        ).first()
        if not lvl_prog:
            lvl_prog = LevelProgress(
                user_id=current_user.id,
                level_number=level_num,
                status="available" if level_num == 1 else "locked",
                topics_completed_count=0
            )
            db.add(lvl_prog)
            db.flush()

        passed_topics_in_lvl = db.query(UserProgress).join(Challenge, Challenge.id == UserProgress.challenge_id).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.exam_passed == True,
            Challenge.order_index > (level_num - 1) * 10,
            Challenge.order_index <= level_num * 10
        ).count()
        lvl_prog.topics_completed_count = passed_topics_in_lvl

    # Evaluate rank and performance score after exam
    new_rank, rank_changed, change_type = evaluate_user_rank(
        db, current_user.id, f"topic_exam_{challenge.title}"
    )

    db.commit()

    return {
        "attempt_id": attempt.id,
        "exam_id": exam.id,
        "topic_id": challenge.id,
        "attempt_number": attempt.attempt_number,
        "score": total_score,
        "total_points": max_score,
        "max_score": max_score,
        "percentage": percentage,
        "passing_percentage": exam.pass_percentage,
        "pass_percentage": exam.pass_percentage,
        "passed": is_passed,
        "xp_awarded": xp_awarded,
        "current_rank": new_rank,
        "performance_score": current_user.profile.performance_score if current_user.profile else 60.0,
        "rank_changed": rank_changed,
        "change_type": change_type,
        "next_topic_id": next_topic_id,
        "next_unlocked_topic_id": next_topic_id,
        "next_topic_title": next_topic_title,
        "results": question_evals
    }


@router.get("/exams/{exam_id}/attempts")
async def get_exam_attempts(
    exam_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns attempt history and scores for the authenticated user on this exam.
    """
    attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.exam_id == exam_id
    ).order_by(ExamAttempt.attempt_number.desc()).all()

    return [
        {
            "id": a.id,
            "attempt_number": a.attempt_number,
            "score": a.score,
            "max_score": a.max_score,
            "percentage": a.percentage,
            "passed": a.passed,
            "submitted_at": a.submitted_at.isoformat() if a.submitted_at else None,
            "total_questions": a.total_questions,
            "correct_answers": a.correct_answers
        }
        for a in attempts
    ]


# ==============================================================================
# EXISTING STRUCTURED LESSONS & CHALLENGE ATTEMPTS
# ==============================================================================

@router.get("/lessons")
async def list_all_lessons():
    """Returns the comprehensive tutorial guides for all 10 tracks."""
    return get_all_track_lessons()


@router.get("/lessons/{track_number}")
async def get_track_lesson(track_number: int):
    """Returns the tutorial guide for a specific track."""
    if track_number in TRACK_MASTER_LESSONS:
        return TRACK_MASTER_LESSONS[track_number]
    raise HTTPException(status_code=404, detail="Track lesson not found")


class QuizSubmissionPayload(BaseModel):
    answers: Dict[str, int]


@router.get("/structured-lessons")
async def list_structured_lessons():
    """Returns summaries of all 100 structured lessons across all tracks."""
    return list_all_structured_lessons()


@router.get("/structured-lessons/by-challenge/{challenge_id}")
async def get_structured_lesson_for_challenge(challenge_id: str):
    """Returns the structured lesson for a challenge."""
    lesson = get_structured_lesson_by_challenge(challenge_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Structured lesson not found")
    return lesson


@router.get("/structured-lessons/{lesson_id}")
async def get_structured_lesson(lesson_id: str):
    """Returns structured lesson by lesson ID."""
    lesson = get_structured_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Structured lesson not found")
    return lesson


@router.post("/structured-lessons/{lesson_id}/quiz")
async def submit_lesson_quiz(
    lesson_id: str,
    payload: QuizSubmissionPayload,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """Evaluates quiz answers for a structured lesson."""
    lesson = get_structured_lesson_by_id(lesson_id)
    if not lesson:
        raise HTTPException(status_code=404, detail="Structured lesson not found")

    quiz_questions = lesson.get("quiz", [])
    if not quiz_questions:
        return {"total": 0, "correct": 0, "score_percent": 100, "passed": True, "xp_awarded": 0, "results": []}

    results = []
    correct_count = 0

    for q in quiz_questions:
        qid = q["id"]
        user_answer = payload.answers.get(qid)
        is_correct = (user_answer == q["correct_index"])
        if is_correct:
            correct_count += 1
        results.append({
            "question_id": qid,
            "question": q["question"],
            "user_answer": user_answer,
            "correct_answer": q["correct_index"],
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })

    passed = (correct_count == len(quiz_questions))
    xp_awarded = 0

    if passed and current_user:
        xp_awarded = lesson.get("xp_reward", 25)
        if current_user.profile:
            current_user.profile.total_xp += xp_awarded
            current_user.profile.current_level = int((current_user.profile.total_xp / 100) ** 0.5) + 1
            db.commit()

    return {
        "lesson_id": lesson_id,
        "total": len(quiz_questions),
        "correct": correct_count,
        "score_percent": round((correct_count / len(quiz_questions)) * 100) if quiz_questions else 100,
        "passed": passed,
        "xp_awarded": xp_awarded,
        "results": results
    }


@router.post("/challenges/{challenge_id}/start")
async def start_challenge_attempt(
    challenge_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Starts an official timed challenge attempt.
    """
    from backend.app.models.entities import Attempt
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # Check lock status
    if challenge.order_index > 1:
        prev_ch = db.query(Challenge).filter(Challenge.order_index == challenge.order_index - 1).first()
        if prev_ch:
            prev_p = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == prev_ch.id
            ).first()
            if not prev_p or not prev_p.exam_passed:
                raise HTTPException(status_code=403, detail="Prerequisite topic exam not passed")

    # Cancel previous in_progress attempts
    prev_attempts = db.query(Attempt).filter(
        Attempt.user_id == current_user.id,
        Attempt.challenge_id == challenge_id,
        Attempt.status == "in_progress"
    ).all()
    for prev in prev_attempts:
        prev.status = "abandoned"

    attempt = Attempt(
        user_id=current_user.id,
        challenge_id=challenge_id,
        started_at=datetime.utcnow(),
        time_limit_seconds=challenge.time_limit_seconds,
        status="in_progress",
        duration_seconds=0
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "challenge_id": challenge.id,
        "started_at": attempt.started_at.isoformat(),
        "time_limit_seconds": attempt.time_limit_seconds,
        "status": attempt.status
    }


@router.get("/challenges/{challenge_id}/submissions")
async def fetch_challenge_submissions(
    challenge_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns past submissions for the current authenticated user on this challenge.
    """
    subs = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.challenge_id == challenge_id
    ).order_by(Submission.created_at.desc()).limit(20).all()

    return [
        {
            "id": s.id,
            "passed": s.passed,
            "passed_tests_count": s.passed_tests_count,
            "total_tests_count": s.total_tests_count,
            "status": s.status,
            "execution_time_ms": s.execution_time_ms,
            "attempt_duration_seconds": s.attempt_duration_seconds,
            "created_at": s.created_at.isoformat() if s.created_at else None,
            "code": s.code
        }
        for s in subs
    ]


# =====================================================================
# 10-LEVEL PROGRESSION & LEVEL FINAL TEST ENDPOINTS
# =====================================================================

LEVEL_METADATA = {
    1: {"title": "Python Core Foundations & Execution", "description": "Syntax, variables, memory models, operators, expressions, and string operations."},
    2: {"title": "Control Flow & Decision Logic", "description": "Conditionals, truthiness, loops, iterables, and robust loop control patterns."},
    3: {"title": "Data Structures (Lists, Tuples, Dicts, Sets)", "description": "Sequences, hashing, indexing, slicing, mappings, mutation, and time complexity."},
    4: {"title": "Functions, Scope & Modular Code", "description": "Signatures, args/kwargs, LEGB scope, closures, docstrings, and recursion."},
    5: {"title": "Object-Oriented Programming (OOP)", "description": "Classes, encapsulation, inheritance, polymorphism, dunder methods, and dataclasses."},
    6: {"title": "Functional Programming & Comprehensions", "description": "List/dict comprehensions, generator expressions, map/filter/reduce, and lambdas."},
    7: {"title": "Advanced Python & Metaprogramming", "description": "Decorators, generators, iterators, context managers, and introspection."},
    8: {"title": "File I/O, Serialization & APIs", "description": "File operations, JSON parsing, API interactions, HTTP requests, and serialization."},
    9: {"title": "Concurrency, AsyncIO & Performance", "description": "Multithreading, multiprocessing, event loops, async/await, and profiling."},
    10: {"title": "Architecture, Design Patterns & Capstone", "description": "SOLID principles, design patterns, microservices, testing, and production capstone."}
}


class TestSubmissionPayload(BaseModel):
    answers: Dict[str, str]


@router.get("/levels")
async def list_levels(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns the complete 10-Level progression roadmap with unlock status,
    topic completion count, final test status, and XP requirements.
    """
    levels_data = []
    user_xp = current_user.profile.total_xp if (current_user and current_user.profile) else 0
    user_level = current_user.profile.current_level if (current_user and current_user.profile) else 1

    # Map existing challenges to levels (10 challenges per level)
    for lvl_num in range(1, 11):
        meta = LEVEL_METADATA.get(lvl_num, {"title": f"Level {lvl_num}", "description": ""})
        xp_required = LEVEL_XP_REQUIREMENTS.get(lvl_num, 0)
        next_xp_required = LEVEL_XP_REQUIREMENTS.get(lvl_num + 1, 30000)

        topics_total = 10
        topics_completed = 0
        final_test_passed = False
        final_test_score = None
        is_unlocked = (lvl_num == 1)
        is_completed = False

        if current_user:
            # Count passed topic exams in this level
            topics_completed = db.query(UserProgress).join(Challenge, Challenge.id == UserProgress.challenge_id).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.exam_passed == True,
                Challenge.order_index > (lvl_num - 1) * 10,
                Challenge.order_index <= lvl_num * 10
            ).count()

            lvl_prog = db.query(LevelProgress).filter(
                LevelProgress.user_id == current_user.id,
                LevelProgress.level_number == lvl_num
            ).first()

            if lvl_prog:
                final_test_passed = bool(lvl_prog.final_test_passed)
                final_test_score = lvl_prog.final_test_score
                is_unlocked = (lvl_prog.status in ["available", "completed"]) or (lvl_num <= user_level)
                is_completed = (lvl_prog.status == "completed") or (topics_completed >= topics_total and final_test_passed and user_xp >= next_xp_required)
            else:
                is_unlocked = (lvl_num <= user_level)

        levels_data.append({
            "level_number": lvl_num,
            "title": meta["title"],
            "description": meta["description"],
            "topics_total": topics_total,
            "topics_completed": topics_completed,
            "final_test_passed": final_test_passed,
            "final_test_score": final_test_score,
            "final_test_id": f"lft-lvl-{lvl_num}",
            "xp_required": xp_required,
            "next_level_xp_required": next_xp_required,
            "user_xp": user_xp,
            "unlocked": is_unlocked,
            "completed": is_completed,
            "can_take_final_test": is_unlocked and (topics_completed >= topics_total)
        })

    return levels_data


@router.get("/levels/{level_number}")
async def get_level_details(
    level_number: int,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns granular details of a specific level including all 10 topics and final test readiness.
    """
    if level_number < 1 or level_number > 10:
        raise HTTPException(status_code=404, detail="Level number must be between 1 and 10")

    meta = LEVEL_METADATA.get(level_number, {"title": f"Level {level_number}", "description": ""})
    xp_required = LEVEL_XP_REQUIREMENTS.get(level_number, 0)
    next_level_xp = LEVEL_XP_REQUIREMENTS.get(level_number + 1, 30000)

    # Fetch challenges belonging to this level
    start_order = (level_number - 1) * 10 + 1
    end_order = level_number * 10
    challenges = db.query(Challenge).filter(
        Challenge.order_index >= start_order,
        Challenge.order_index <= end_order
    ).order_by(Challenge.order_index.asc()).all()

    topics = []
    topics_completed = 0

    user_xp = current_user.profile.total_xp if (current_user and current_user.profile) else 0

    for ch in challenges:
        is_exam_passed = False
        is_unlocked = (ch.order_index == 1)
        if current_user:
            prog = db.query(UserProgress).filter(
                UserProgress.user_id == current_user.id,
                UserProgress.challenge_id == ch.id
            ).first()
            if prog:
                is_exam_passed = bool(prog.exam_passed)
                is_unlocked = (prog.status in ["available", "in_progress", "exam_available", "passed"])

            # Check prerequisite topic exam
            if ch.order_index > 1:
                prev_ch = db.query(Challenge).filter(Challenge.order_index == ch.order_index - 1).first()
                if prev_ch:
                    prev_p = db.query(UserProgress).filter(
                        UserProgress.user_id == current_user.id,
                        UserProgress.challenge_id == prev_ch.id
                    ).first()
                    is_unlocked = bool(prev_p and prev_p.exam_passed)

        if is_exam_passed:
            topics_completed += 1

        topics.append({
            "id": ch.id,
            "order_index": ch.order_index,
            "title": ch.title,
            "description": ch.description,
            "xp_reward": ch.xp_reward,
            "unlocked": is_unlocked,
            "exam_passed": is_exam_passed
        })

    # Final test state
    lvl_prog = None
    if current_user:
        lvl_prog = db.query(LevelProgress).filter(
            LevelProgress.user_id == current_user.id,
            LevelProgress.level_number == level_number
        ).first()

    final_test_passed = bool(lvl_prog.final_test_passed) if lvl_prog else False
    final_test_score = lvl_prog.final_test_score if lvl_prog else None
    level_unlocked = (level_number == 1) or (lvl_prog and lvl_prog.status in ["available", "completed"]) or (current_user and current_user.profile and current_user.profile.current_level >= level_number)

    can_unlock_next = (
        topics_completed >= len(challenges) and
        final_test_passed and
        user_xp >= next_level_xp
    )

    return {
        "level_number": level_number,
        "title": meta["title"],
        "description": meta["description"],
        "xp_required": xp_required,
        "next_level_xp_required": next_level_xp,
        "user_xp": user_xp,
        "unlocked": level_unlocked,
        "topics_total": len(challenges),
        "topics_completed": topics_completed,
        "final_test_passed": final_test_passed,
        "final_test_score": final_test_score,
        "can_take_final_test": level_unlocked and (topics_completed >= len(challenges)),
        "can_unlock_next": can_unlock_next,
        "topics": topics
    }


@router.get("/levels/{level_number}/final-test")
async def get_level_final_test(
    level_number: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetches the comprehensive Level Final Test for a level.
    Requires that all topics in the level are completed first.
    Correct answers and explanations are stripped for examination integrity.
    """
    if level_number < 1 or level_number > 10:
        raise HTTPException(status_code=404, detail="Level number must be between 1 and 10")

    # Enforce prerequisite: All topics in this level must have passed exams
    passed_topics = db.query(UserProgress).join(Challenge, Challenge.id == UserProgress.challenge_id).filter(
        UserProgress.user_id == current_user.id,
        UserProgress.exam_passed == True,
        Challenge.order_index > (level_number - 1) * 10,
        Challenge.order_index <= level_number * 10
    ).count()

    if passed_topics < 10:
        raise HTTPException(
            status_code=403,
            detail=f"Prerequisite not met: You have completed {passed_topics}/10 topics in Level {level_number}. Pass all topic exams before taking the Level Final Test."
        )

    test = db.query(LevelFinalTest).filter(LevelFinalTest.level_number == level_number).first()
    if not test:
        raise HTTPException(status_code=404, detail=f"Final Test for Level {level_number} not found")

    questions_data = []
    for q in sorted(test.questions, key=lambda x: x.order_index):
        opts = []
        if q.options_json:
            try:
                opts = json.loads(q.options_json)
            except Exception:
                opts = []

        questions_data.append({
            "id": q.id,
            "order_index": q.order_index,
            "question_type": q.question_type,
            "question_text": q.question_text,
            "code_snippet": q.code_snippet,
            "options": opts,
            "points": q.points
        })

    # Past attempt history
    attempts = db.query(LevelFinalTestAttempt).filter(
        LevelFinalTestAttempt.user_id == current_user.id,
        LevelFinalTestAttempt.level_test_id == test.id
    ).order_by(LevelFinalTestAttempt.attempt_number.desc()).all()

    return {
        "test_id": test.id,
        "level_number": test.level_number,
        "title": test.title,
        "description": test.description,
        "time_limit_minutes": test.time_limit_minutes,
        "pass_percentage": test.pass_percentage,
        "xp_reward": test.xp_reward,
        "total_questions": len(questions_data),
        "questions": questions_data,
        "attempts_count": len(attempts),
        "best_percentage": max([a.percentage for a in attempts], default=None),
        "is_passed": any(a.passed for a in attempts)
    }


@router.post("/levels/{level_number}/final-test/submit")
async def submit_level_final_test(
    level_number: int,
    payload: TestSubmissionPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submits and server-side grades a Level Final Test.
    1. Grades questions (MCQ, prediction, debug, short answer).
    2. Checks >= 70% passing threshold.
    3. Saves LevelFinalTestAttempt and LevelFinalTestAnswer.
    4. If passed:
       - Awards +250 XP idempotently via award_xp.
       - Records final_test_passed = True in LevelProgress.
       - Checks all 3 progression criteria (topics, test >= 70%, cumulative XP).
       - If all 3 met: marks level complete and unlocks Level N+1.
       - Re-evaluates student Rank & Performance Score.
    """
    test = db.query(LevelFinalTest).filter(LevelFinalTest.level_number == level_number).first()
    if not test:
        raise HTTPException(status_code=404, detail="Level Final Test not found")

    now = datetime.utcnow()
    total_score = 0.0
    max_score = 0.0
    correct_count = 0
    question_evals = []

    for q in test.questions:
        max_score += q.points
        user_ans = payload.answers.get(q.id, "").strip()
        is_corr = (str(user_ans).lower() == str(q.correct_answer).strip().lower())
        pts = float(q.points) if is_corr else 0.0
        if is_corr:
            total_score += pts
            correct_count += 1

        question_evals.append({
            "question_id": q.id,
            "question_type": q.question_type,
            "question_text": q.question_text,
            "user_answer": user_ans,
            "correct_answer": q.correct_answer,
            "is_correct": is_corr,
            "points_awarded": pts,
            "max_points": q.points,
            "explanation": q.explanation
        })

    percentage = round((total_score / max_score * 100.0), 1) if max_score > 0 else 0.0
    is_passed = (percentage >= float(test.pass_percentage))

    # Persist attempt record
    prev_attempts_count = db.query(LevelFinalTestAttempt).filter(
        LevelFinalTestAttempt.user_id == current_user.id,
        LevelFinalTestAttempt.level_test_id == test.id
    ).count()

    attempt = LevelFinalTestAttempt(
        user_id=current_user.id,
        level_test_id=test.id,
        level_number=level_number,
        attempt_number=prev_attempts_count + 1,
        score=total_score,
        max_score=max_score,
        percentage=percentage,
        passed=is_passed,
        total_questions=len(test.questions),
        correct_answers=correct_count,
        started_at=now,
        submitted_at=now
    )
    db.add(attempt)
    db.flush()

    for qe in question_evals:
        db.add(LevelFinalTestAnswer(
            attempt_id=attempt.id,
            question_id=qe["question_id"],
            selected_answer=qe["user_answer"],
            is_correct=qe["is_correct"],
            points_awarded=qe["points_awarded"]
        ))

    xp_awarded = 0
    unlocked_next_level = False
    next_level_number = None

    # Get or create LevelProgress
    lvl_prog = db.query(LevelProgress).filter(
        LevelProgress.user_id == current_user.id,
        LevelProgress.level_number == level_number
    ).first()
    if not lvl_prog:
        lvl_prog = LevelProgress(
            user_id=current_user.id,
            level_number=level_number,
            status="available",
            topics_completed_count=10
        )
        db.add(lvl_prog)
        db.flush()

    if is_passed:
        lvl_prog.final_test_passed = True
        lvl_prog.final_test_score = max(lvl_prog.final_test_score or 0.0, percentage)

        # Award Level Final Test Pass XP (+250 XP) idempotently
        awarded, _ = award_xp(
            db=db,
            user_id=current_user.id,
            source_type="level_final_test_pass",
            source_id=test.id,
            amount=test.xp_reward or 250,
            idempotency_key=f"xp:{current_user.id}:level_final:{test.id}:pass"
        )
        xp_awarded = awarded

        # Verify all 3 requirements to unlock next level:
        # 1. All topics in level completed (10/10)
        # 2. Level final test passed (>= 70%)
        # 3. Total XP >= next level threshold
        next_lvl_num = level_number + 1
        req_xp_for_next = LEVEL_XP_REQUIREMENTS.get(next_lvl_num, 30000)

        passed_topics = db.query(UserProgress).join(Challenge, Challenge.id == UserProgress.challenge_id).filter(
            UserProgress.user_id == current_user.id,
            UserProgress.exam_passed == True,
            Challenge.order_index > (level_number - 1) * 10,
            Challenge.order_index <= level_number * 10
        ).count()

        current_total_xp = current_user.profile.total_xp if current_user.profile else 0

        if passed_topics >= 10 and current_total_xp >= req_xp_for_next and level_number < 10:
            lvl_prog.status = "completed"
            lvl_prog.completed_at = now

            # Unlock Level N+1
            next_prog = db.query(LevelProgress).filter(
                LevelProgress.user_id == current_user.id,
                LevelProgress.level_number == next_lvl_num
            ).first()
            if not next_prog:
                next_prog = LevelProgress(
                    user_id=current_user.id,
                    level_number=next_lvl_num,
                    status="available",
                    topics_completed_count=0,
                    unlocked_at=now
                )
                db.add(next_prog)
            else:
                next_prog.status = "available"

            if current_user.profile:
                current_user.profile.current_level = max(current_user.profile.current_level, next_lvl_num)

            unlocked_next_level = True
            next_level_number = next_lvl_num

    # Recalculate rank and performance score
    new_rank, rank_changed, change_type = evaluate_user_rank(
        db, current_user.id, f"level_{level_number}_final_test"
    )

    db.commit()

    return {
        "attempt_id": attempt.id,
        "test_id": test.id,
        "level_number": level_number,
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "pass_percentage": test.pass_percentage,
        "passed": is_passed,
        "xp_awarded": xp_awarded,
        "total_xp": current_user.profile.total_xp if current_user.profile else 0,
        "unlocked_next_level": unlocked_next_level,
        "next_level_number": next_level_number,
        "current_rank": new_rank,
        "performance_score": current_user.profile.performance_score if current_user.profile else 60.0,
        "rank_changed": rank_changed,
        "change_type": change_type,
        "results": question_evals
    }


# =====================================================================
# PERIODIC TESTS (WEEKLY & MONTHLY) ENDPOINTS
# =====================================================================

@router.get("/tests/periodic")
async def list_periodic_tests(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns available Weekly and Monthly Periodic Tests with user's score history.
    """
    tests = db.query(PeriodicTest).order_by(
        PeriodicTest.test_type.asc(),
        PeriodicTest.period_number.asc()
    ).all()

    result = []
    for t in tests:
        attempts_count = 0
        best_score = None
        passed = False

        if current_user:
            user_attempts = db.query(PeriodicTestAttempt).filter(
                PeriodicTestAttempt.user_id == current_user.id,
                PeriodicTestAttempt.test_id == t.id
            ).all()
            attempts_count = len(user_attempts)
            if user_attempts:
                best_score = max(a.percentage for a in user_attempts)
                passed = any(a.passed for a in user_attempts)

        result.append({
            "id": t.id,
            "test_type": t.test_type,
            "period_number": t.period_number,
            "week_or_month_number": t.period_number,
            "title": t.title,
            "description": t.description,
            "time_limit_minutes": t.time_limit_minutes,
            "pass_percentage": t.pass_percentage,
            "xp_reward": t.xp_reward,
            "attempts_count": attempts_count,
            "best_score": best_score,
            "passed": passed
        })

    return result


@router.get("/tests/periodic/{test_id}")
async def get_periodic_test(
    test_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetches periodic test questions (stripped of correct answer and explanation).
    """
    test = db.query(PeriodicTest).filter(PeriodicTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Periodic test not found")

    questions_data = []
    for q in sorted(test.questions, key=lambda x: x.order_index):
        opts = []
        if q.options_json:
            try:
                opts = json.loads(q.options_json)
            except Exception:
                opts = []

        questions_data.append({
            "id": q.id,
            "order_index": q.order_index,
            "question_type": q.question_type,
            "question_text": q.question_text,
            "code_snippet": q.code_snippet,
            "options": opts,
            "points": q.points
        })

    return {
        "id": test.id,
        "test_type": test.test_type,
        "period_number": test.period_number,
        "week_or_month_number": test.period_number,
        "title": test.title,
        "description": test.description,
        "time_limit_minutes": test.time_limit_minutes,
        "pass_percentage": test.pass_percentage,
        "xp_reward": test.xp_reward,
        "total_questions": len(questions_data),
        "questions": questions_data
    }


@router.post("/tests/periodic/{test_id}/submit")
async def submit_periodic_test(
    test_id: str,
    payload: TestSubmissionPayload,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Server-side evaluation of Periodic Tests (Weekly: +200 XP, Monthly: +500 XP).
    Updates user's weekly/monthly average and recalculates performance score and rank.
    """
    test = db.query(PeriodicTest).filter(PeriodicTest.id == test_id).first()
    if not test:
        raise HTTPException(status_code=404, detail="Periodic test not found")

    now = datetime.utcnow()
    total_score = 0.0
    max_score = 0.0
    correct_count = 0
    question_evals = []

    for q in test.questions:
        max_score += q.points
        user_ans = payload.answers.get(q.id, "").strip()
        is_corr = (str(user_ans).lower() == str(q.correct_answer).strip().lower())
        pts = float(q.points) if is_corr else 0.0
        if is_corr:
            total_score += pts
            correct_count += 1

        question_evals.append({
            "question_id": q.id,
            "question_type": q.question_type,
            "question_text": q.question_text,
            "user_answer": user_ans,
            "correct_answer": q.correct_answer,
            "is_correct": is_corr,
            "points_awarded": pts,
            "max_points": q.points,
            "explanation": q.explanation
        })

    percentage = round((total_score / max_score * 100.0), 1) if max_score > 0 else 0.0
    is_passed = (percentage >= float(test.pass_percentage))

    prev_attempts = db.query(PeriodicTestAttempt).filter(
        PeriodicTestAttempt.user_id == current_user.id,
        PeriodicTestAttempt.test_id == test.id
    ).count()

    attempt = PeriodicTestAttempt(
        user_id=current_user.id,
        test_id=test.id,
        test_type=test.test_type,
        period_number=test.period_number,
        attempt_number=prev_attempts + 1,
        score=total_score,
        max_score=max_score,
        percentage=percentage,
        passed=is_passed,
        started_at=now,
        submitted_at=now
    )
    db.add(attempt)
    db.flush()

    xp_awarded = 0
    if is_passed:
        awarded, _ = award_xp(
            db=db,
            user_id=current_user.id,
            source_type=f"periodic_{test.test_type}_pass",
            source_id=test.id,
            amount=test.xp_reward or (200 if test.test_type == "weekly" else 500),
            idempotency_key=f"xp:{current_user.id}:periodic_{test.test_type}:{test.id}:pass"
        )
        xp_awarded = awarded

    # Recalculate rank and performance score
    new_rank, rank_changed, change_type = evaluate_user_rank(
        db, current_user.id, f"periodic_{test.test_type}_test_{test.id}"
    )

    db.commit()

    return {
        "attempt_id": attempt.id,
        "test_id": test.id,
        "test_type": test.test_type,
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "pass_percentage": test.pass_percentage,
        "passed": is_passed,
        "xp_awarded": xp_awarded,
        "current_rank": new_rank,
        "performance_score": current_user.profile.performance_score if current_user.profile else 60.0,
        "rank_changed": rank_changed,
        "change_type": change_type,
        "results": question_evals
    }


# =====================================================================
# RANK PROFILE & AUDIT TRAIL ENDPOINTS
# =====================================================================

@router.get("/profile/rank")
async def get_rank_profile(
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns complete Rank Profile with 5-factor breakdown,
    consecutive low counter, and promotion progress checklist.
    """
    if not current_user or not current_user.profile:
        # Default guest rank profile
        return {
            "current_rank": "GOLD",
            "performance_score": 60.0,
            "components": {
                "topic_exam_avg": 60.0,
                "coding_performance": 60.0,
                "weekly_test_avg": 60.0,
                "monthly_test_avg": 60.0,
                "consistency_score": 60.0,
                "performance_score": 60.0
            },
            "consecutive_low_count": 0,
            "next_rank": "PLATINUM",
            "promotion_criteria": [
                {"name": "Performance Score >= 75.0", "target": 75.0, "current": 60.0, "met": False},
                {"name": "Topic Exams Passed >= 2", "target": 2, "current": 0, "met": False},
                {"name": "Latest Weekly Test >= 70%", "target": 70.0, "current": 0.0, "met": False}
            ]
        }

    # Evaluate current rank to get latest components
    evaluate_user_rank(db, current_user.id, "rank_profile_fetch")
    db.commit()

    profile = current_user.profile
    curr_rank = profile.current_rank or "GOLD"
    curr_score = profile.performance_score or 60.0
    components = calculate_performance_components(db, current_user.id)

    # Calculate criteria for next rank
    next_rank = None
    curr_idx = RANKS_ORDER.index(curr_rank) if curr_rank in RANKS_ORDER else 0
    if curr_idx < len(RANKS_ORDER) - 1:
        next_rank = RANKS_ORDER[curr_idx + 1]

    # Check metrics for promotion checklist
    passed_exams = db.query(
        func.count(func.distinct(ExamAttempt.topic_id))
    ).filter(
        ExamAttempt.user_id == current_user.id,
        ExamAttempt.passed == True
    ).scalar() or 0

    latest_weekly = db.query(PeriodicTestAttempt).filter(
        PeriodicTestAttempt.user_id == current_user.id,
        PeriodicTestAttempt.test_type == "weekly"
    ).order_by(PeriodicTestAttempt.started_at.desc()).first()
    latest_weekly_pct = latest_weekly.percentage if latest_weekly else 0.0

    latest_monthly = db.query(PeriodicTestAttempt).filter(
        PeriodicTestAttempt.user_id == current_user.id,
        PeriodicTestAttempt.test_type == "monthly"
    ).order_by(PeriodicTestAttempt.started_at.desc()).first()
    latest_monthly_pct = latest_monthly.percentage if latest_monthly else 0.0

    has_capstone = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.passed == True,
        Submission.challenge_id.like("chal-9%") | Submission.challenge_id.like("chal-100") | Submission.challenge_id.like("proj-%")
    ).first() is not None

    criteria = []
    if curr_rank == "GOLD":
        criteria = [
            {"name": "Performance Score >= 75.0", "target": 75.0, "current": curr_score, "met": curr_score >= 75.0},
            {"name": "Passed Topic Exams >= 2", "target": 2, "current": passed_exams, "met": passed_exams >= 2},
            {"name": "Latest Weekly Test >= 70%", "target": 70.0, "current": latest_weekly_pct, "met": latest_weekly_pct >= 70.0}
        ]
    elif curr_rank == "PLATINUM":
        criteria = [
            {"name": "Performance Score >= 85.0", "target": 85.0, "current": curr_score, "met": curr_score >= 85.0},
            {"name": "Coding Performance >= 80.0", "target": 80.0, "current": components["coding_performance"], "met": components["coding_performance"] >= 80.0},
            {"name": "Latest Monthly Test >= 75%", "target": 75.0, "current": latest_monthly_pct, "met": latest_monthly_pct >= 75.0}
        ]
    elif curr_rank == "DIAMOND":
        criteria = [
            {"name": "Performance Score >= 95.0", "target": 95.0, "current": curr_score, "met": curr_score >= 95.0},
            {"name": "Coding Performance >= 90.0", "target": 90.0, "current": components["coding_performance"], "met": components["coding_performance"] >= 90.0},
            {"name": "Latest Monthly Test >= 90%", "target": 90.0, "current": latest_monthly_pct, "met": latest_monthly_pct >= 90.0},
            {"name": "Capstone Project Completed", "target": 1, "current": 1 if has_capstone else 0, "met": has_capstone}
        ]
    else:
        criteria = [
            {"name": "Maximum Rank Achieved (MASTER)", "target": 100, "current": curr_score, "met": True}
        ]

    return {
        "current_rank": curr_rank,
        "performance_score": curr_score,
        "components": components,
        "consecutive_low_count": profile.consecutive_low_performance_count or 0,
        "next_rank": next_rank,
        "promotion_criteria": criteria,
        "total_xp": profile.total_xp,
        "current_level": profile.current_level
    }


@router.get("/profile/rank-history")
async def get_rank_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns audit trail of rank promotions and demotions.
    """
    history = db.query(RankHistory).filter(
        RankHistory.user_id == current_user.id
    ).order_by(RankHistory.changed_at.desc()).all()

    return [
        {
            "id": h.id,
            "old_rank": h.old_rank,
            "new_rank": h.new_rank,
            "performance_score": h.performance_score,
            "reason": h.reason,
            "changed_at": h.changed_at.isoformat() if h.changed_at else None
        }
        for h in history
    ]


@router.get("/profile/xp-history")
async def get_xp_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Returns audit log of all server-awarded XP transactions.
    """
    txs = db.query(XPTransaction).filter(
        XPTransaction.user_id == current_user.id
    ).order_by(XPTransaction.created_at.desc()).limit(100).all()

    return [
        {
            "id": tx.id,
            "amount": tx.amount,
            "source": tx.source,
            "source_type": tx.source_type,
            "source_id": tx.source_id,
            "transaction_key": tx.transaction_key,
            "created_at": tx.created_at.isoformat() if tx.created_at else None
        }
        for tx in txs
    ]
