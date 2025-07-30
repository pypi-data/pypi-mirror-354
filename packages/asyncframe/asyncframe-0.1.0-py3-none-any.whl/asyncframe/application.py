"""
核心应用类 - 实现ASGI接口，现在支持类视图（CBV）
"""

import asyncio
import json
from typing import Dict, List, Callable, Any, Optional
from .routing import Router
from .request import Request
from .response import Response
from .middleware import MiddlewareStack
from .exceptions import HTTPException
from .background import BackgroundTaskManager


class AsyncFrame:
    """基于ASGI的异步Web框架核心类 - 现在支持类视图"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.router = Router()
        self.middleware_stack = MiddlewareStack()
        self.background_tasks = BackgroundTaskManager()
        self.startup_handlers: List[Callable] = []
        self.shutdown_handlers: List[Callable] = []
        self.exception_handlers: Dict[int, Callable] = {}
        
    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        """ASGI应用入口点"""
        assert scope["type"] in ("http", "websocket", "lifespan")
        
        if scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
        elif scope["type"] == "http":
            await self._handle_http(scope, receive, send)
        elif scope["type"] == "websocket":
            await self._handle_websocket(scope, receive, send)
    
    async def _handle_lifespan(self, scope: Dict, receive: Callable, send: Callable):
        """处理应用生命周期事件"""
        message = await receive()
        assert message["type"] == "lifespan.startup"
        
        try:
            # 执行启动处理器
            for handler in self.startup_handlers:
                await handler()
            await send({"type": "lifespan.startup.complete"})
        except Exception as exc:
            await send({
                "type": "lifespan.startup.failed",
                "message": str(exc)
            })
            return
        
        message = await receive()
        assert message["type"] == "lifespan.shutdown"
        
        try:
            # 执行关闭处理器
            for handler in self.shutdown_handlers:
                await handler()
            await send({"type": "lifespan.shutdown.complete"})
        except Exception as exc:
            await send({
                "type": "lifespan.shutdown.failed", 
                "message": str(exc)
            })
    
    async def _handle_http(self, scope: Dict, receive: Callable, send: Callable):
        """处理HTTP请求"""
        try:
            # 创建请求对象
            request = Request(scope, receive)
            
            # 查找路由处理器
            handler, path_params = self.router.resolve(
                request.method, request.url.path
            )
            
            if handler is None:
                response = Response("Not Found", status_code=404)
            else:
                # 设置路径参数
                request.path_params = path_params
                
                # 通过中间件栈处理请求
                response = await self.middleware_stack.process_request(
                    request, handler
                )
            
            # 发送响应
            await response(scope, receive, send)
            
        except HTTPException as exc:
            response = await self._handle_exception(exc)
            await response(scope, receive, send)
        except Exception as exc:
            if self.debug:
                import traceback
                error_detail = traceback.format_exc()
            else:
                error_detail = "Internal Server Error"
            
            response = Response(error_detail, status_code=500)
            await response(scope, receive, send)
    
    async def _handle_websocket(self, scope: Dict, receive: Callable, send: Callable):
        """处理WebSocket连接"""
        from .websocket import WebSocket
        
        websocket = WebSocket(scope, receive, send)
        
        # 查找WebSocket处理器
        handler, path_params = self.router.resolve_websocket(scope["path"])
        
        if handler is None:
            await websocket.close(code=1000)
            return
        
        # 设置路径参数
        websocket.path_params = path_params
        
        try:
            await handler(websocket)
        except Exception as exc:
            if self.debug:
                print(f"WebSocket错误: {exc}")
            await websocket.close(code=1011)
    
    async def _handle_exception(self, exc: HTTPException) -> Response:
        """处理HTTP异常"""
        handler = self.exception_handlers.get(exc.status_code)
        if handler:
            return await handler(exc)
        
        return Response(exc.detail, status_code=exc.status_code)
    
    # 路由装饰器方法（函数视图）
    def route(self, path: str, methods: List[str] = None):
        """路由装饰器"""
        if methods is None:
            methods = ["GET"]
        return self.router.route(path, methods)
    
    def get(self, path: str):
        """GET路由装饰器"""
        return self.router.get(path)
    
    def post(self, path: str):
        """POST路由装饰器"""
        return self.router.post(path)
    
    def put(self, path: str):
        """PUT路由装饰器"""
        return self.router.put(path)
    
    def delete(self, path: str):
        """DELETE路由装饰器"""
        return self.router.delete(path)
    
    def websocket(self, path: str):
        """WebSocket路由装饰器"""
        return self.router.websocket(path)
    
    # 类视图相关方法
    def add_class_view(self, path: str, view_class, methods: List[str] = None):
        """添加类视图"""
        self.router.add_class_view(path, view_class, methods)
    
    def class_view(self, path: str, methods: List[str] = None):
        """类视图装饰器"""
        return self.router.class_view(path, methods)
    
    # 中间件方法
    def add_middleware(self, middleware_class, **kwargs):
        """添加中间件"""
        self.middleware_stack.add(middleware_class, **kwargs)
    
    # 事件处理器
    def on_startup(self, handler: Callable):
        """添加启动事件处理器"""
        self.startup_handlers.append(handler)
        return handler
    
    def on_shutdown(self, handler: Callable):
        """添加关闭事件处理器"""
        self.shutdown_handlers.append(handler)
        return handler
    
    def exception_handler(self, status_code: int):
        """异常处理器装饰器"""
        def decorator(handler):
            self.exception_handlers[status_code] = handler
            return handler
        return decorator
    
    def add_background_task(self, func: Callable, *args, **kwargs):
        """添加后台任务"""
        return self.background_tasks.add_task(func, *args, **kwargs)
    
    def run(self, host: str = "127.0.0.1", port: int = 8000, **kwargs):
        """运行ASGI应用（开发环境专用）"""
        try:
            import uvicorn
            print(f"🚀 启动 AsyncFrame 开发服务器")
            print(f"📍 地址: http://{host}:{port}")
            print(f"🔧 调试模式: {'开启' if self.debug else '关闭'}")
            print("⚡ 使用 Ctrl+C 停止服务器\n")
            
            uvicorn.run(self, host=host, port=port, **kwargs)
            
        except ImportError:
            print("❌ 需要安装 uvicorn: pip install uvicorn")
            print("💡 或者手动运行: uvicorn your_app:app --host {} --port {}".format(host, port))
            raise
        except KeyboardInterrupt:
            print("\n👋 服务器已停止")
        except Exception as e:
            print(f"❌ 启动失败: {e}")
            raise 