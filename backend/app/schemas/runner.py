"""
Pydantic Schemas for Runner execution requests and responses
Strictly enforces that test cases and timeouts are NEVER accepted from client.
"""

from typing import List, Any, Optional
from pydantic import BaseModel, Field


class TestResultItem(BaseModel):
    test_index: int
    description: str
    is_hidden: bool
    passed: bool
    input: Any
    expected: Any
    actual: Any
    error: Optional[str] = None


class ExecuteRequest(BaseModel):
    challenge_id: str
    code: str
    attempt_id: Optional[str] = None
    attempt_started_at: Optional[float] = None


class ExecuteResponse(BaseModel):
    submission_id: str
    passed: bool
    stdout: str
    stderr: str
    execution_time_ms: int
    attempt_duration_seconds: int
    passed_tests_count: int = 0
    total_tests_count: int = 0
    test_results: List[TestResultItem] = Field(default_factory=list)
    status: str
    xp_earned: int = 0
    total_xp: int = 0
    current_level: int = 1
    current_rank: Optional[str] = "GOLD"
    performance_score: Optional[float] = 60.0
    new_streak: Optional[int] = None
    unlocked_next: bool = False
    badges_awarded: List[str] = Field(default_factory=list)

