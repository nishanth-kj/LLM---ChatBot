from pydantic import BaseModel
from typing import Optional

class HealthResponse(BaseModel):
    status: str
    app_name: str
    version: str
    model_loaded: bool
    current_model: Optional[str] = None
