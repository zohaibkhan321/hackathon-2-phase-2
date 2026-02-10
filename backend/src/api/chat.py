from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from uuid import UUID
from typing import Dict, Any
import os
from pydantic import BaseModel

from ..config.database import get_session
from ..services.auth import get_current_user
from ..models.conversation import ChatMessage, ChatResponse
from ..services.ai_service import AIService

router = APIRouter()

# Initialize AI service (OpenAI key optional for local rule-based AI)
ai_service = AIService(openai_api_key=os.getenv("OPENAI_API_KEY"))

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: UUID,
    chat_message: ChatMessage,
    db: Session = Depends(get_session),
    current_user_id: str = Depends(get_current_user)
) -> ChatResponse:
    """
    Chat endpoint for AI-powered todo management.
    
    Args:
        user_id: ID of the user making the request
        chat_message: The message from the user
        db: Database session
        current_user: Authenticated user from JWT token
    
    Returns:
        ChatResponse with AI response and optional tool results
    
    Raises:
        HTTPException: For authentication or authorization errors
    """
    
    # Verify user authorization
    if str(current_user_id) != str(user_id):
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's chat"
        )
    
    try:
        # Process the message with AI service
        result = await ai_service.process_message(
            db=db,
            user_id=user_id,
            message=chat_message.message
        )
        
        return ChatResponse(
            response=result["response"],
            tool_results=result.get("tool_results"),
            conversation_id=result.get("conversation_id")
        )
        
    except Exception as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Chat endpoint error: {str(e)}")
        
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your message"
        )