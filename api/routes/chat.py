from fastapi import APIRouter, Request, HTTPException
from models.schemas import ChatRequest, SwitchModelRequest
from utils.api_response import ApiResponse
from utils.logger import logger

router = APIRouter()

@router.post("/chat")
async def process_chat(request: Request, chat_request: ChatRequest):
    """Process a chat message using the currently loaded LLM"""
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    if not llm_service.is_initialized:
        return ApiResponse.fail(400, "No model loaded. Please load a model first.")

    try:
        answer = llm_service.get_response(chat_request.question)
        return ApiResponse.success({"answer": answer})
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return ApiResponse.fail(500, str(e))


@router.get("/models")
async def list_models(request: Request):
    """List available models for the LLM Playground"""
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    models = llm_service.get_available_models()
    return ApiResponse.success({
        "models": models,
        "current_model": llm_service.current_model
    })


@router.post("/models/switch")
async def switch_model(request: Request, switch_request: SwitchModelRequest):
    """Switch the LLM model"""
    llm_service = request.app.state.llm_service
    if not llm_service:
        return ApiResponse.fail(500, "LLM Service is not initialized")
        
    try:
        llm_service.switch_model(switch_request.model_filename)
        return ApiResponse.success({
            "message": f"Successfully switched to {switch_request.model_filename}",
            "current_model": llm_service.current_model
        })
    except FileNotFoundError as e:
        return ApiResponse.fail(404, str(e))
    except Exception as e:
        logger.error(f"Error switching model: {e}")
        return ApiResponse.fail(500, str(e))
