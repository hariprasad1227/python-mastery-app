"""
Pydantic Schemas for AI Mentor Requests and Responses
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class MentorHintRequest(BaseModel):
    challenge_title: str
    challenge_instructions: str
    learner_code: str
    error_message: Optional[str] = None
    hint_level: int = Field(default=1, description="1: Nudge/Concept, 2: Syntax/Logic clue, 3: Guided step")


class MentorHintResponse(BaseModel):
    hint_level: int
    hint: str
    socratic_question: str
    encouragement: str


class ChatMessage(BaseModel):
    role: str = Field(description="'user', 'assistant', or 'system'")
    content: str


class MentorChatRequest(BaseModel):
    messages: List[ChatMessage]
    current_topic: Optional[str] = None
    code_context: Optional[str] = None
    error_context: Optional[str] = None
    language: Optional[str] = "auto"


class MentorChatResponse(BaseModel):
    reply: str
    suggestions: List[str] = Field(default_factory=list)
    code_snippet: Optional[str] = None
