"""
XP Service for Python Mastery
Server-authoritative, idempotent point management with unique transaction keys.
Prevents duplicate XP awards from retries, replays, or client tampering.
"""

from typing import Optional, Dict, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from backend.app.models.entities import User, Profile, XPTransaction

# Cumulative XP thresholds required to be eligible to unlock each level
LEVEL_XP_REQUIREMENTS: Dict[int, int] = {
    1: 0,
    2: 1000,
    3: 2500,
    4: 4500,
    5: 7000,
    6: 10000,
    7: 14000,
    8: 18500,
    9: 24000,
    10: 30000,
}

# Standard XP reward constants
XP_REWARDS = {
    "SUBTOPIC_COMPLETION": 10,
    "LESSON_COMPLETION": 50,
    "PRACTICE_COMPLETION": 25,
    "TOPIC_EXAM_PASS": 100,
    "TOPIC_EXAM_FIRST_ATTEMPT_BONUS": 50,
    "LEVEL_FINAL_TEST_PASS": 250,
    "WEEKLY_TEST_PASS": 200,
    "MONTHLY_TEST_PASS": 500,
    "CHALLENGE_EASY": 50,
    "CHALLENGE_MEDIUM": 100,
    "CHALLENGE_HARD": 200,
    "CHALLENGE_EXPERT": 350,
    "STREAK_3_DAY": 30,
    "STREAK_7_DAY": 100,
    "STREAK_14_DAY": 250,
    "STREAK_30_DAY": 500,
}


def award_xp(
    db: Session,
    user_id: str,
    source_type: str,
    source_id: str,
    amount: int,
    idempotency_key: str,
    challenge_id: Optional[str] = None
) -> Tuple[int, bool]:
    """
    Awards XP strictly once per unique idempotency key.
    Returns (xp_awarded, is_new_transaction).
    If idempotency_key already exists in DB, awards 0 and returns (0, False).
    """
    # 1. Check for existing transaction key
    existing = db.query(XPTransaction).filter(
        XPTransaction.transaction_key == idempotency_key
    ).first()

    if existing:
        return 0, False

    # Also check legacy constraint (user_id, challenge_id, source) if challenge_id is set
    if challenge_id:
        existing_legacy = db.query(XPTransaction).filter(
            XPTransaction.user_id == user_id,
            XPTransaction.challenge_id == challenge_id,
            XPTransaction.source == source_type
        ).first()
        if existing_legacy:
            return 0, False

    now = datetime.utcnow()

    # 2. Record transaction
    tx = XPTransaction(
        user_id=user_id,
        challenge_id=challenge_id,
        amount=amount,
        source=source_type,
        source_type=source_type,
        source_id=source_id,
        transaction_key=idempotency_key,
        created_at=now
    )
    db.add(tx)

    # 3. Update user profile total XP
    profile = db.query(Profile).filter(Profile.user_id == user_id).first()
    if profile:
        profile.total_xp += amount
        profile.updated_at = now

    db.flush()
    return amount, True


def get_next_level_xp_requirement(current_level: int) -> int:
    """Returns the cumulative XP required to unlock the next level."""
    next_lvl = min(10, current_level + 1)
    return LEVEL_XP_REQUIREMENTS.get(next_lvl, 30000)
