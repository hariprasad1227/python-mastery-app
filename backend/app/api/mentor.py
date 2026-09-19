"""
AI Mentor API Router
Endpoint for Socratic hints and guided explanations.
"""

from fastapi import APIRouter
from backend.app.schemas.mentor import (
    MentorHintRequest,
    MentorHintResponse,
    MentorChatRequest,
    MentorChatResponse,
)
from backend.app.services.mentor_service import generate_mentor_hint, generate_mentor_chat

router = APIRouter(prefix="/mentor", tags=["mentor"])


@router.post("/hint", response_model=MentorHintResponse)
async def get_mentor_hint(request: MentorHintRequest):
    """
    Generates tailored, Socratic hints for learner's active code and challenge.
    """
    return await generate_mentor_hint(request)


@router.post("/chat", response_model=MentorChatResponse)
async def chat_with_mentor(request: MentorChatRequest):
    """
    Multi-turn conversational AI Mentor for interactive Python tutoring,
    code explanation, error debugging, and Telugu/English conceptual help.
    """
    return await generate_mentor_chat(request)
