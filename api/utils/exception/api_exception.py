from utils.contants.error_code import ErrorCode
from utils.contants.error_message import ErrorMessage

class ApiException(Exception):
    def __init__(self, error_code: ErrorCode, message: str = None, fields: dict = None):
        self.error_code = error_code
        # Map error code to default message if not provided
        if message is None:
            message = getattr(ErrorMessage, error_code.name, ErrorMessage.GENERAL_ERROR)
        
        self.message = message
        self.fields = fields
        super().__init__(self.message)
