"""
中间件系统 - 处理请求前后的逻辑
"""

import time
import traceback
from typing import Callable, List, Any, Dict
from .request import Request
from .response import Response, JSONResponse


class Middleware:
    """中间件基类"""
    
    async def before_request(self, request: Request) -> Request:
        """请求前处理"""
        return request
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """请求后处理"""
        return response
    
    async def on_exception(self, request: Request, exc: Exception) -> Response:
        """异常处理"""
        raise exc


class MiddlewareStack:
    """中间件栈"""
    
    def __init__(self):
        self.middlewares: List[Middleware] = []
    
    def add(self, middleware_class, **kwargs):
        """添加中间件"""
        middleware = middleware_class(**kwargs)
        self.middlewares.append(middleware)
    
    async def process_request(self, request: Request, handler: Callable) -> Response:
        """处理请求通过中间件栈"""
        try:
            # 前置处理
            for middleware in self.middlewares:
                request = await middleware.before_request(request)
            
            # 执行处理器
            response = await handler(request)
            
            # 确保返回Response对象
            if not isinstance(response, Response):
                if isinstance(response, (dict, list)):
                    response = JSONResponse(response)
                elif isinstance(response, str):
                    response = Response(response)
                else:
                    response = Response(str(response))
            
            # 后置处理
            for middleware in reversed(self.middlewares):
                response = await middleware.after_request(request, response)
            
            return response
            
        except Exception as exc:
            # 异常处理
            for middleware in reversed(self.middlewares):
                try:
                    response = await middleware.on_exception(request, exc)
                    if isinstance(response, Response):
                        return response
                except Exception:
                    continue
            
            # 如果没有中间件处理异常，重新抛出
            raise exc


class CORSMiddleware(Middleware):
    """CORS中间件"""
    
    def __init__(
        self,
        allow_origins: List[str] = None,
        allow_methods: List[str] = None,
        allow_headers: List[str] = None,
        allow_credentials: bool = False,
        max_age: int = 600
    ):
        self.allow_origins = allow_origins or ["*"]
        self.allow_methods = allow_methods or ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        self.allow_headers = allow_headers or ["*"]
        self.allow_credentials = allow_credentials
        self.max_age = max_age
    
    async def before_request(self, request: Request) -> Request:
        """CORS预检请求处理"""
        if request.method == "OPTIONS":
            # 这是预检请求，需要特殊处理
            request._is_preflight = True
        return request
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """添加CORS头"""
        origin = request.get_header("origin")
        
        if origin and (self.allow_origins == ["*"] or origin in self.allow_origins):
            response.headers["access-control-allow-origin"] = origin
        elif self.allow_origins == ["*"]:
            response.headers["access-control-allow-origin"] = "*"
        
        if self.allow_credentials:
            response.headers["access-control-allow-credentials"] = "true"
        
        if hasattr(request, '_is_preflight') and request._is_preflight:
            response.headers["access-control-allow-methods"] = ", ".join(self.allow_methods)
            response.headers["access-control-allow-headers"] = ", ".join(self.allow_headers)
            response.headers["access-control-max-age"] = str(self.max_age)
        
        return response


class LoggingMiddleware(Middleware):
    """日志中间件"""
    
    def __init__(self, logger=None):
        self.logger = logger
        
    async def before_request(self, request: Request) -> Request:
        """记录请求开始时间"""
        request._start_time = time.time()
        
        if self.logger:
            self.logger.info(f"{request.method} {request.url.path}")
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {request.method} {request.url.path}")
        
        return request
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """记录请求完成信息"""
        duration = time.time() - getattr(request, '_start_time', time.time())
        
        log_msg = f"{request.method} {request.url.path} - {response.status_code} ({duration:.3f}s)"
        
        if self.logger:
            self.logger.info(log_msg)
        else:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {log_msg}")
        
        return response


class SecurityMiddleware(Middleware):
    """安全中间件"""
    
    def __init__(
        self,
        force_https: bool = False,
        hsts_max_age: int = 31536000,
        content_type_nosniff: bool = True,
        xss_protection: bool = True,
        frame_options: str = "DENY"
    ):
        self.force_https = force_https
        self.hsts_max_age = hsts_max_age
        self.content_type_nosniff = content_type_nosniff
        self.xss_protection = xss_protection
        self.frame_options = frame_options
    
    async def before_request(self, request: Request) -> Request:
        """安全检查"""
        if self.force_https and not request.is_secure:
            # 可以在这里重定向到HTTPS
            pass
        
        return request
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """添加安全头"""
        if request.is_secure and self.hsts_max_age > 0:
            response.headers["strict-transport-security"] = f"max-age={self.hsts_max_age}"
        
        if self.content_type_nosniff:
            response.headers["x-content-type-options"] = "nosniff"
        
        if self.xss_protection:
            response.headers["x-xss-protection"] = "1; mode=block"
        
        if self.frame_options:
            response.headers["x-frame-options"] = self.frame_options
        
        return response


class RateLimitMiddleware(Middleware):
    """简单的速率限制中间件"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_counts: Dict[str, List[float]] = {}
    
    async def before_request(self, request: Request) -> Request:
        """检查速率限制"""
        client_ip = request.client[0] if request.client else "unknown"
        current_time = time.time()
        
        # 清理过期的请求记录
        if client_ip in self.request_counts:
            self.request_counts[client_ip] = [
                req_time for req_time in self.request_counts[client_ip]
                if current_time - req_time < self.window_seconds
            ]
        else:
            self.request_counts[client_ip] = []
        
        # 检查是否超过限制
        if len(self.request_counts[client_ip]) >= self.max_requests:
            from .exceptions import HTTPException
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        
        # 记录当前请求
        self.request_counts[client_ip].append(current_time)
        
        return request


class CompressionMiddleware(Middleware):
    """响应压缩中间件"""
    
    def __init__(self, minimum_size: int = 500):
        self.minimum_size = minimum_size
    
    async def after_request(self, request: Request, response: Response) -> Response:
        """压缩响应"""
        accept_encoding = request.get_header("accept-encoding", "")
        
        if "gzip" in accept_encoding and len(response.content) > self.minimum_size:
            import gzip
            
            if isinstance(response.content, str):
                content = response.content.encode("utf-8")
            else:
                content = response.content
            
            compressed_content = gzip.compress(content)
            
            if len(compressed_content) < len(content):
                response.content = compressed_content
                response.headers["content-encoding"] = "gzip"
                response.headers["content-length"] = str(len(compressed_content))
        
        return response 