from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependency to get the LLM service instance
# In a real app, you might use a dependency injection container
# For now, we'll assume it's initialized in main.py and available globally or via a getter

def get_llm_service():
    from app.main import llm_service
    return llm_service

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, llm: LLMService = Depends(get_llm_service)):
    """Chat endpoint for conversing with the healthcare bot"""
    if llm is None or not llm.is_initialized:
        raise HTTPException(
            status_code=503,
            detail="LLM service is not initialized. Please check server logs."
        )
    
    try:
        answer = llm.get_response(request.question)
        return ChatResponse(
            answer=answer,
            question=request.question
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )

@router.post("/reset")
async def reset_conversation(llm: LLMService = Depends(get_llm_service)):
    """Reset conversation history"""
    if llm is None or not llm.is_initialized:
        raise HTTPException(
            status_code=503,
            detail="LLM service is not initialized"
        )
    
    try:
        llm.reset_memory()
        return {"message": "Conversation history reset successfully"}
    except Exception as e:
        logger.error(f"Error resetting conversation: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error resetting conversation: {str(e)}"
        )
