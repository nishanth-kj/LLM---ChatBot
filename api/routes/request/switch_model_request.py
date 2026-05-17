from pydantic import BaseModel

class SwitchModelRequest(BaseModel):
    model_filename: str
