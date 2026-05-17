import enum

class ErrorCode(enum.IntEnum):

    
    # Client-side errors (4xx)
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    
    # Server-side errors (5xx)
    INTERNAL_SERVER_ERROR = 500
    AI_PROCESSING_ERROR = 501
    SERVICE_UNAVAILABLE = 503
