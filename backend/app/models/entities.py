"""
SQLAlchemy ORM Entities for Python Mastery
Persistent relational models matching the production PostgreSQL schema.
Includes Users, Profiles, Challenges, UserProgress, Submissions, Attempts,
XPTransactions, Badges, and RateLimits.
"""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime, ForeignKey, Float, UniqueConstraint, Index
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    progress = relationship("UserProgress", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")
    attempts = relationship("Attempt", back_populates="user", cascade="all, delete-orphan")
    xp_transactions = relationship("XPTransaction", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    exam_attempts = relationship("ExamAttempt", back_populates="user", cascade="all, delete-orphan")
    level_progress = relationship("LevelProgress", back_populates="user", cascade="all, delete-orphan")
    rank_history = relationship("RankHistory", back_populates="user", cascade="all, delete-orphan")
    performance_snapshots = relationship("PerformanceSnapshot", back_populates="user", cascade="all, delete-orphan")


class Profile(Base):
    __tablename__ = "profiles"

    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    total_xp = Column(Integer, default=0, nullable=False)
    current_level = Column(Integer, default=1, nullable=False)
    current_rank = Column(String(20), default="GOLD", nullable=False) # GOLD, PLATINUM, DIAMOND, MASTER
    performance_score = Column(Float, default=60.0, nullable=False)
    topic_exam_avg = Column(Float, default=60.0, nullable=False)
    coding_performance = Column(Float, default=60.0, nullable=False)
    weekly_test_avg = Column(Float, default=60.0, nullable=False)
    monthly_test_avg = Column(Float, default=60.0, nullable=False)
    consistency_score = Column(Float, default=60.0, nullable=False)
    consecutive_low_performance_count = Column(Integer, default=0, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_active_date = Column(String(10), nullable=True) # YYYY-MM-DD
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(String(36), primary_key=True) # e.g. "chal-1"
    slug = Column(String(100), unique=True, nullable=False)
    title = Column(String(150), nullable=False)
    level_number = Column(Integer, nullable=False, index=True)
    order_index = Column(Integer, nullable=False, index=True)
    difficulty = Column(String(20), default="easy", nullable=False) # easy, medium, hard
    instructions = Column(Text, nullable=False)
    starter_code = Column(Text, nullable=False)
    solution_code = Column(Text, nullable=False)
    entry_function_name = Column(String(100), nullable=True)
    test_cases_json = Column(Text, nullable=False, default="[]") # Official test cases (visible + hidden)
    hints_json = Column(Text, nullable=False, default="[]")
    xp_reward = Column(Integer, default=50, nullable=False)
    time_limit_seconds = Column(Integer, default=300, nullable=False) # Total challenge attempt countdown limit (e.g. 300s = 5m)
    sandbox_timeout_seconds = Column(Float, default=3.0, nullable=False) # Per-execution sandbox run timeout


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), default="locked", nullable=False) # locked, available, in_progress, exam_available, passed
    lesson_completed = Column(Boolean, default=False, nullable=False)
    practice_completed = Column(Boolean, default=False, nullable=False)
    exam_passed = Column(Boolean, default=False, nullable=False)
    attempts_count = Column(Integer, default=0, nullable=False)
    earned_xp = Column(Integer, default=0, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="progress")
    challenge = relationship("Challenge")

    __table_args__ = (
        UniqueConstraint("user_id", "challenge_id", name="uq_user_challenge_progress"),
    )


class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    time_limit_seconds = Column(Integer, default=300, nullable=False)
    status = Column(String(20), default="in_progress", nullable=False) # in_progress, completed, timed_out
    submitted_at = Column(DateTime, nullable=True)
    duration_seconds = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="attempts")
    challenge = relationship("Challenge")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    attempt_id = Column(String(36), ForeignKey("attempts.id", ondelete="SET NULL"), nullable=True)
    code = Column(Text, nullable=False)
    passed = Column(Boolean, default=False, nullable=False)
    passed_tests_count = Column(Integer, default=0, nullable=False)
    total_tests_count = Column(Integer, default=0, nullable=False)
    stdout = Column(Text, nullable=True)
    stderr = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, default=0, nullable=False)
    attempt_duration_seconds = Column(Integer, default=0, nullable=False)
    status = Column(String(30), default="completed", nullable=False) # completed, failed, timed_out, error
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="submissions")
    challenge = relationship("Challenge")


class XPTransaction(Base):
    __tablename__ = "xp_transactions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    challenge_id = Column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=True, index=True)
    amount = Column(Integer, nullable=False)
    source = Column(String(50), nullable=False) # challenge_completion, topic_exam_pass, etc.
    source_type = Column(String(50), nullable=True) # LESSON_COMPLETION, TOPIC_EXAM_PASS, etc.
    source_id = Column(String(50), nullable=True)
    transaction_key = Column(String(120), unique=True, index=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="xp_transactions")


class Badge(Base):
    __tablename__ = "badges"

    id = Column(String(36), primary_key=True)
    code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    icon = Column(String(10), nullable=False)
    xp_bonus = Column(Integer, default=100, nullable=False)


class UserBadge(Base):
    __tablename__ = "user_badges"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    badge_id = Column(String(36), ForeignKey("badges.id", ondelete="CASCADE"), nullable=False)
    awarded_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge")

    __table_args__ = (
        UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),
    )


class RateLimitRecord(Base):
    __tablename__ = "rate_limits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String(100), nullable=False, index=True) # IP address or user_id
    action = Column(String(50), nullable=False, index=True) # login, register, execute, mentor
    window_start = Column(Float, nullable=False)
    request_count = Column(Integer, default=1, nullable=False)

    __table_args__ = (
        Index("idx_rate_limit_key_action", "key", "action"),
    )


class Exam(Base):
    __tablename__ = "exams"

    id = Column(String(36), primary_key=True) # e.g. "exam-chal-1"
    topic_id = Column(String(36), ForeignKey("challenges.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    pass_percentage = Column(Integer, default=70, nullable=False)
    time_limit_minutes = Column(Integer, default=15, nullable=False)
    total_questions = Column(Integer, default=5, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Challenge")
    questions = relationship("ExamQuestion", back_populates="exam", cascade="all, delete-orphan", order_by="ExamQuestion.order_index")
    attempts = relationship("ExamAttempt", back_populates="exam", cascade="all, delete-orphan")


class ExamQuestion(Base):
    __tablename__ = "exam_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    exam_id = Column(String(36), ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=1, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(30), default="mcq", nullable=False) # mcq, output_prediction, debugging, short_answer
    code_snippet = Column(Text, nullable=True)
    options_json = Column(Text, default="[]", nullable=False) # JSON list of options for MCQs
    correct_answer = Column(String(255), nullable=False) # e.g. "0" for option index, or exact keyword/number
    explanation = Column(Text, nullable=True)
    points = Column(Integer, default=1, nullable=False)

    exam = relationship("Exam", back_populates="questions")


class ExamAttempt(Base):
    __tablename__ = "exam_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    exam_id = Column(String(36), ForeignKey("exams.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(String(36), nullable=False, index=True)
    attempt_number = Column(Integer, default=1, nullable=False)
    score = Column(Float, default=0.0, nullable=False)
    max_score = Column(Float, default=0.0, nullable=False)
    percentage = Column(Float, default=0.0, nullable=False)
    passed = Column(Boolean, default=False, nullable=False)
    total_questions = Column(Integer, default=0, nullable=False)
    correct_answers = Column(Integer, default=0, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="exam_attempts")
    exam = relationship("Exam", back_populates="attempts")
    answers = relationship("ExamAnswer", back_populates="attempt", cascade="all, delete-orphan")


class ExamAnswer(Base):
    __tablename__ = "exam_answers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = Column(String(36), ForeignKey("exam_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("exam_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    points_awarded = Column(Float, default=0.0, nullable=False)

    attempt = relationship("ExamAttempt", back_populates="answers")
    question = relationship("ExamQuestion")


class LevelProgress(Base):
    __tablename__ = "level_progress"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    level_number = Column(Integer, nullable=False, index=True)
    status = Column(String(20), default="locked", nullable=False) # locked, available, completed
    topics_completed_count = Column(Integer, default=0, nullable=False)
    final_test_passed = Column(Boolean, default=False, nullable=False)
    final_test_score = Column(Float, default=0.0, nullable=False)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="level_progress")

    __table_args__ = (
        UniqueConstraint("user_id", "level_number", name="uq_user_level_progress"),
    )


class LevelFinalTest(Base):
    __tablename__ = "level_final_tests"

    id = Column(String(36), primary_key=True) # e.g. "level-test-1"
    level_number = Column(Integer, unique=True, nullable=False, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    pass_percentage = Column(Integer, default=70, nullable=False)
    time_limit_minutes = Column(Integer, default=25, nullable=False)
    total_questions = Column(Integer, default=6, nullable=False)
    xp_reward = Column(Integer, default=250, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("LevelFinalTestQuestion", back_populates="level_test", cascade="all, delete-orphan", order_by="LevelFinalTestQuestion.order_index")
    attempts = relationship("LevelFinalTestAttempt", back_populates="level_test", cascade="all, delete-orphan")


class LevelFinalTestQuestion(Base):
    __tablename__ = "level_final_test_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    level_test_id = Column(String(36), ForeignKey("level_final_tests.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=1, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(30), default="mcq", nullable=False) # mcq, output_prediction, debugging, short_answer, coding
    code_snippet = Column(Text, nullable=True)
    options_json = Column(Text, default="[]", nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=True)
    points = Column(Integer, default=1, nullable=False)

    level_test = relationship("LevelFinalTest", back_populates="questions")


class LevelFinalTestAttempt(Base):
    __tablename__ = "level_final_test_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    level_test_id = Column(String(36), ForeignKey("level_final_tests.id", ondelete="CASCADE"), nullable=False, index=True)
    level_number = Column(Integer, nullable=False, index=True)
    attempt_number = Column(Integer, default=1, nullable=False)
    score = Column(Float, default=0.0, nullable=False)
    max_score = Column(Float, default=0.0, nullable=False)
    percentage = Column(Float, default=0.0, nullable=False)
    passed = Column(Boolean, default=False, nullable=False)
    total_questions = Column(Integer, default=0, nullable=False)
    correct_answers = Column(Integer, default=0, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = Column(DateTime, nullable=True)

    user = relationship("User")
    level_test = relationship("LevelFinalTest", back_populates="attempts")
    answers = relationship("LevelFinalTestAnswer", back_populates="attempt", cascade="all, delete-orphan")


class LevelFinalTestAnswer(Base):
    __tablename__ = "level_final_test_answers"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = Column(String(36), ForeignKey("level_final_test_attempts.id", ondelete="CASCADE"), nullable=False, index=True)
    question_id = Column(String(36), ForeignKey("level_final_test_questions.id", ondelete="CASCADE"), nullable=False, index=True)
    selected_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, default=False, nullable=False)
    points_awarded = Column(Float, default=0.0, nullable=False)

    attempt = relationship("LevelFinalTestAttempt", back_populates="answers")
    question = relationship("LevelFinalTestQuestion")


class PeriodicTest(Base):
    __tablename__ = "periodic_tests"

    id = Column(String(36), primary_key=True) # e.g. "weekly-test-1", "monthly-test-1"
    test_type = Column(String(20), nullable=False) # weekly, monthly
    period_number = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    pass_percentage = Column(Integer, default=70, nullable=False)
    time_limit_minutes = Column(Integer, default=20, nullable=False)
    total_questions = Column(Integer, default=5, nullable=False)
    xp_reward = Column(Integer, default=200, nullable=False) # weekly: 200, monthly: 500
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship("PeriodicTestQuestion", back_populates="periodic_test", cascade="all, delete-orphan", order_by="PeriodicTestQuestion.order_index")
    attempts = relationship("PeriodicTestAttempt", back_populates="periodic_test", cascade="all, delete-orphan")


class PeriodicTestQuestion(Base):
    __tablename__ = "periodic_test_questions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    test_id = Column(String(36), ForeignKey("periodic_tests.id", ondelete="CASCADE"), nullable=False, index=True)
    order_index = Column(Integer, default=1, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(30), default="mcq", nullable=False)
    code_snippet = Column(Text, nullable=True)
    options_json = Column(Text, default="[]", nullable=False)
    correct_answer = Column(String(255), nullable=False)
    explanation = Column(Text, nullable=True)
    points = Column(Integer, default=1, nullable=False)

    periodic_test = relationship("PeriodicTest", back_populates="questions")


class PeriodicTestAttempt(Base):
    __tablename__ = "periodic_test_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    test_id = Column(String(36), ForeignKey("periodic_tests.id", ondelete="CASCADE"), nullable=False, index=True)
    test_type = Column(String(20), nullable=False)
    period_number = Column(Integer, nullable=False)
    attempt_number = Column(Integer, default=1, nullable=False)
    score = Column(Float, default=0.0, nullable=False)
    max_score = Column(Float, default=0.0, nullable=False)
    percentage = Column(Float, default=0.0, nullable=False)
    passed = Column(Boolean, default=False, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    submitted_at = Column(DateTime, nullable=True)

    user = relationship("User")
    periodic_test = relationship("PeriodicTest", back_populates="attempts")


class RankHistory(Base):
    __tablename__ = "rank_history"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    old_rank = Column(String(20), nullable=False)
    new_rank = Column(String(20), nullable=False)
    performance_score = Column(Float, nullable=False)
    reason = Column(Text, nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="rank_history")


class PerformanceSnapshot(Base):
    __tablename__ = "performance_snapshots"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_exam_avg = Column(Float, default=60.0, nullable=False)
    coding_performance = Column(Float, default=60.0, nullable=False)
    weekly_test_avg = Column(Float, default=60.0, nullable=False)
    monthly_test_avg = Column(Float, default=60.0, nullable=False)
    consistency_score = Column(Float, default=60.0, nullable=False)
    performance_score = Column(Float, default=60.0, nullable=False)
    rank = Column(String(20), default="GOLD", nullable=False)
    consecutive_low_count = Column(Integer, default=0, nullable=False)
    evaluated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="performance_snapshots")

