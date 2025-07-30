"""
HTTP异常处理类
"""


class HTTPException(Exception):
    """HTTP异常基类"""
    
    def __init__(self, status_code: int, detail: str = ""):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


class BadRequest(HTTPException):
    """400 Bad Request"""
    
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(400, detail)


class Unauthorized(HTTPException):
    """401 Unauthorized"""
    
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(401, detail)


class Forbidden(HTTPException):
    """403 Forbidden"""
    
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(403, detail)


class NotFound(HTTPException):
    """404 Not Found"""
    
    def __init__(self, detail: str = "Not Found"):
        super().__init__(404, detail)


class MethodNotAllowed(HTTPException):
    """405 Method Not Allowed"""
    
    def __init__(self, detail: str = "Method Not Allowed"):
        super().__init__(405, detail)


class InternalServerError(HTTPException):
    """500 Internal Server Error"""
    
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(500, detail) 