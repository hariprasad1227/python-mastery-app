"""
Rank & Performance Calculation Engine for Python Mastery
Independent 4-tier rank system (Gold, Platinum, Diamond, Master)
driven by a 5-component performance score with anti-demotion guardrails.
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.app.models.entities import (
    User, Profile, ExamAttempt, Submission, Challenge,
    PeriodicTestAttempt, RankHistory, PerformanceSnapshot
)

RANKS_ORDER = ["GOLD", "PLATINUM", "DIAMOND", "MASTER"]

RANK_THRESHOLDS = {
    "GOLD": 60.0,
    "PLATINUM": 75.0,
    "DIAMOND": 85.0,
    "MASTER": 95.0,
}


def calculate_performance_components(db: Session, user_id: str) -> Dict[str, float]:
    """
    Calculates the 5 sub-scores for the student:
    1. Topic Exam Average (30%)
    2. Coding Performance (30%)
    3. Weekly Test Average (15%)
    4. Monthly Test Average (15%)
    5. Consistency Score (10%)
    """
    # 1. Topic Exam Average
    exam_attempts = db.query(ExamAttempt).filter(
        ExamAttempt.user_id == user_id
    ).all()

    if exam_attempts:
        # Take the best score per topic to reward mastery
        topic_best: Dict[str, float] = {}
        for att in exam_attempts:
            topic_best[att.topic_id] = max(topic_best.get(att.topic_id, 0.0), att.percentage)
        topic_exam_avg = sum(topic_best.values()) / max(1, len(topic_best))
    else:
        topic_exam_avg = 60.0  # Initial baseline for new students

    # 2. Coding Performance
    submissions = db.query(Submission).filter(Submission.user_id == user_id).all()
    if submissions:
        total_subs = len(submissions)
        passed_subs = sum(1 for s in submissions if s.passed)
        # Distinct challenges passed
        passed_challenges = len({s.challenge_id for s in submissions if s.passed})
        attempted_challenges = len({s.challenge_id for s in submissions})

        accuracy_ratio = (passed_challenges / max(1, attempted_challenges))
        pass_rate = (passed_subs / max(1, total_subs))

        coding_perf = min(100.0, (accuracy_ratio * 70.0) + (pass_rate * 30.0))
    else:
        coding_perf = 60.0

    # 3. Weekly Test Average
    weekly_attempts = db.query(PeriodicTestAttempt).filter(
        PeriodicTestAttempt.user_id == user_id,
        PeriodicTestAttempt.test_type == "weekly"
    ).all()

    if weekly_attempts:
        weekly_test_avg = sum(a.percentage for a in weekly_attempts) / len(weekly_attempts)
    else:
        weekly_test_avg = 60.0

    # 4. Monthly Test Average
    monthly_attempts = db.query(PeriodicTestAttempt).filter(
        PeriodicTestAttempt.user_id == user_id,
        PeriodicTestAttempt.test_type == "monthly"
    ).all()

    if monthly_attempts:
        monthly_test_avg = sum(a.percentage for a in monthly_attempts) / len(monthly_attempts)
    else:
        monthly_test_avg = 60.0

    # 5. Consistency Score
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    streak = profile.current_streak if profile else 0
    consistency_score = min(100.0, 60.0 + (streak * 2.5))

    # Overall Performance Score Formula:
    # Topic Exam Average × 30% + Coding Performance × 30% + Weekly Test Average × 15% + Monthly Test Average × 15% + Consistency Score × 10%
    performance_score = round(
        (topic_exam_avg * 0.30) +
        (coding_perf * 0.30) +
        (weekly_test_avg * 0.15) +
        (monthly_test_avg * 0.15) +
        (consistency_score * 0.10),
        1
    )
    performance_score = max(0.0, min(100.0, performance_score))

    return {
        "topic_exam_avg": round(topic_exam_avg, 1),
        "coding_performance": round(coding_perf, 1),
        "weekly_test_avg": round(weekly_test_avg, 1),
        "monthly_test_avg": round(monthly_test_avg, 1),
        "consistency_score": round(consistency_score, 1),
        "performance_score": performance_score
    }


def evaluate_user_rank(
    db: Session,
    user_id: str,
    event_reason: str = "performance_evaluation"
) -> Tuple[str, bool, Optional[str]]:
    """
    Evaluates learner's performance score, checks promotion/demotion conditions,
    updates profile, creates performance snapshot, and records rank history if changed.
    Returns (new_rank, rank_changed, change_type).
    """
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if not profile:
        return "GOLD", False, None

    metrics = calculate_performance_components(db, user_id)
    perf_score = metrics["performance_score"]
    current_rank = profile.current_rank or "GOLD"
    consecutive_low = profile.consecutive_low_performance_count or 0

    # Update profile metric fields
    profile.performance_score = perf_score
    profile.topic_exam_avg = metrics["topic_exam_avg"]
    profile.coding_performance = metrics["coding_performance"]
    profile.weekly_test_avg = metrics["weekly_test_avg"]
    profile.monthly_test_avg = metrics["monthly_test_avg"]
    profile.consistency_score = metrics["consistency_score"]

    now = datetime.utcnow()
    new_rank = current_rank
    rank_changed = False
    change_type = None

    # Helper data for promotion rules
    passed_topic_exams_count = db.query(
        func.count(func.distinct(ExamAttempt.topic_id))
    ).filter(
        ExamAttempt.user_id == user_id,
        ExamAttempt.passed == True
    ).scalar() or 0

    latest_weekly = db.query(PeriodicTestAttempt).filter(
        PeriodicTestAttempt.user_id == user_id,
        PeriodicTestAttempt.test_type == "weekly"
    ).order_by(PeriodicTestAttempt.started_at.desc()).first()
    latest_weekly_pct = latest_weekly.percentage if latest_weekly else 0.0

    latest_monthly = db.query(PeriodicTestAttempt).filter(
        PeriodicTestAttempt.user_id == user_id,
        PeriodicTestAttempt.test_type == "monthly"
    ).order_by(PeriodicTestAttempt.started_at.desc()).first()
    latest_monthly_pct = latest_monthly.percentage if latest_monthly else 0.0

    # -------------------------------------------------------------
    # PROMOTION RULES
    # -------------------------------------------------------------
    # GOLD -> PLATINUM
    if current_rank == "GOLD":
        if (
            perf_score >= 75.0 and
            passed_topic_exams_count >= 2 and
            latest_weekly_pct >= 70.0
        ):
            new_rank = "PLATINUM"
            rank_changed = True
            change_type = "promotion"

    # PLATINUM -> DIAMOND
    elif current_rank == "PLATINUM":
        if (
            perf_score >= 85.0 and
            metrics["coding_performance"] >= 80.0 and
            latest_monthly_pct >= 75.0
        ):
            new_rank = "DIAMOND"
            rank_changed = True
            change_type = "promotion"

    # DIAMOND -> MASTER
    elif current_rank == "DIAMOND":
        # Check if capstone or any project completed
        has_capstone = db.query(Submission).filter(
            Submission.user_id == user_id,
            Submission.passed == True,
            Submission.challenge_id.like("chal-9%") | Submission.challenge_id.like("chal-100") | Submission.challenge_id.like("proj-%")
        ).first() is not None

        if (
            perf_score >= 95.0 and
            metrics["coding_performance"] >= 90.0 and
            latest_monthly_pct >= 90.0 and
            has_capstone
        ):
            new_rank = "MASTER"
            rank_changed = True
            change_type = "promotion"

    # -------------------------------------------------------------
    # DEMOTION RULES (Requires 3 consecutive evaluated periods with score < 70)
    # -------------------------------------------------------------
    if not rank_changed:
        if perf_score < 70.0:
            consecutive_low += 1
            if consecutive_low >= 3:
                curr_idx = RANKS_ORDER.index(current_rank)
                if curr_idx > 0:
                    new_rank = RANKS_ORDER[curr_idx - 1]
                    rank_changed = True
                    change_type = "demotion"
                    consecutive_low = 0  # Reset counter upon demotion
        else:
            consecutive_low = 0  # Reset if performance recovered

    profile.consecutive_low_performance_count = consecutive_low

    if rank_changed:
        profile.current_rank = new_rank
        # Record in rank history
        history_record = RankHistory(
            user_id=user_id,
            old_rank=current_rank,
            new_rank=new_rank,
            performance_score=perf_score,
            reason=f"{change_type.capitalize()}: {event_reason} (Performance: {perf_score})",
            changed_at=now
        )
        db.add(history_record)

    # Save performance snapshot
    snapshot = PerformanceSnapshot(
        user_id=user_id,
        topic_exam_avg=metrics["topic_exam_avg"],
        coding_performance=metrics["coding_performance"],
        weekly_test_avg=metrics["weekly_test_avg"],
        monthly_test_avg=metrics["monthly_test_avg"],
        consistency_score=metrics["consistency_score"],
        performance_score=perf_score,
        rank=new_rank,
        consecutive_low_count=consecutive_low,
        evaluated_at=now
    )
    db.add(snapshot)
    db.flush()

    return new_rank, rank_changed, change_type
