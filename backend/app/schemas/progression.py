"""
Pydantic Schemas for Progression, Curriculum, and User Profiles
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class BadgeItem(BaseModel):
    code: str
    name: str
    description: str
    icon: str
    xp_bonus: int
    awarded: bool = False


class UserProfile(BaseModel):
    id: str
    username: str
    display_name: str
    total_xp: int
    current_level: int
    current_rank: str = "GOLD"
    performance_score: float = 60.0
    current_streak: int
    longest_streak: int
    badges: List[BadgeItem] = Field(default_factory=list)


class ChallengeSummary(BaseModel):
    id: str
    slug: str
    title: str
    instructions: str
    starter_code: str
    entry_function_name: Optional[str] = None
    xp_reward: int
    status: str  # locked, available, completed
    attempts_count: int = 0
    hints: List[str] = Field(default_factory=list)


class ModuleItem(BaseModel):
    id: str
    slug: str
    title: str
    description: str
    level_number: int
    order_index: int
    is_locked: bool
    challenges: List[ChallengeSummary] = Field(default_factory=list)
