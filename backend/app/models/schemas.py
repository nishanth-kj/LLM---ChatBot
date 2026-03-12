from pydantic import BaseModel, Field
from typing import List, Tuple


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str = Field(..., min_length=1, description="User's question")


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(..., description="Bot's answer")
    question: str = Field(..., description="Original question")


class HealthResponse(BaseModel):
    """Response model for health check endpoint"""
    status: str
    app_name: str
    version: str
    model_loaded: bool
