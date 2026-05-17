from typing import Any, Optional
from pydantic import BaseModel
from utils.contants.api_status import ApiStatus
from utils.contants.error_code import ErrorCode
from utils.contants.error_message import ErrorMessage

class ErrorDetail(BaseModel):
    code: int
    message: str
    field: Optional[Any] = None

class ApiResponse(BaseModel):
    status: int  # 1 for success, 0 for error
    error: Optional[ErrorDetail] = None
    data: Optional[Any] = None

    @classmethod
    def success(cls, data: Any = None):
        return cls(
            status=ApiStatus.SUCCESS,
            error=None,
            data=data
        )

    @classmethod
    def fail(cls, error_code: int, message: str, field: Any = None, data: Any = None):
        return cls(
            status=ApiStatus.ERROR,
            error=ErrorDetail(
                code=error_code,
                message=message,
                field=field
            ),
            data=data
        )
