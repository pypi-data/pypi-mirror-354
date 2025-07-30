"""
响应处理类 - 支持多种响应类型
"""

import json
import mimetypes
from typing import Dict, Any, Optional, Union, Iterator
from pathlib import Path


class Response:
    """基础HTTP响应类"""
    
    def __init__(
        self,
        content: Union[str, bytes] = "",
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None
    ):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
        self.media_type = media_type
        
        if media_type is not None:
            self.headers["content-type"] = media_type
    
    def set_cookie(
        self,
        key: str,
        value: str,
        max_age: Optional[int] = None,
        expires: Optional[str] = None,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: str = "lax"
    ):
        """设置Cookie"""
        cookie = f"{key}={value}"
        
        if max_age is not None:
            cookie += f"; Max-Age={max_age}"
        if expires is not None:
            cookie += f"; Expires={expires}"
        if path:
            cookie += f"; Path={path}"
        if domain:
            cookie += f"; Domain={domain}"
        if secure:
            cookie += "; Secure"
        if httponly:
            cookie += "; HttpOnly"
        if samesite:
            cookie += f"; SameSite={samesite}"
        
        # 处理多个Cookie
        if "set-cookie" in self.headers:
            if isinstance(self.headers["set-cookie"], list):
                self.headers["set-cookie"].append(cookie)
            else:
                self.headers["set-cookie"] = [self.headers["set-cookie"], cookie]
        else:
            self.headers["set-cookie"] = cookie
    
    def delete_cookie(self, key: str, path: str = "/", domain: Optional[str] = None):
        """删除Cookie"""
        self.set_cookie(
            key=key,
            value="",
            max_age=0,
            path=path,
            domain=domain
        )
    
    async def __call__(self, scope: Dict[str, Any], receive, send):
        """ASGI调用接口"""
        await self._send_response(send)
    
    async def _send_response(self, send):
        """发送响应"""
        # 准备响应体
        if isinstance(self.content, str):
            body = self.content.encode("utf-8")
        else:
            body = self.content or b""
        
        # 设置Content-Length
        if "content-length" not in self.headers:
            self.headers["content-length"] = str(len(body))
        
        # 发送响应头
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": [
                [key.encode(), value.encode()]
                for key, value in self.headers.items()
            ]
        })
        
        # 发送响应体
        await send({
            "type": "http.response.body",
            "body": body
        })


class JSONResponse(Response):
    """JSON响应"""
    
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        **json_kwargs
    ):
        json_content = json.dumps(content, ensure_ascii=False, **json_kwargs)
        super().__init__(
            content=json_content,
            status_code=status_code,
            headers=headers,
            media_type="application/json; charset=utf-8"
        )


class HTMLResponse(Response):
    """HTML响应"""
    
    def __init__(
        self,
        content: str,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="text/html; charset=utf-8"
        )


class PlainTextResponse(Response):
    """纯文本响应"""
    
    def __init__(
        self,
        content: str,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type="text/plain; charset=utf-8"
        )


class RedirectResponse(Response):
    """重定向响应"""
    
    def __init__(
        self,
        url: str,
        status_code: int = 307,
        headers: Optional[Dict[str, str]] = None
    ):
        headers = headers or {}
        headers["location"] = url
        super().__init__(
            content="",
            status_code=status_code,
            headers=headers
        )


class FileResponse(Response):
    """文件响应"""
    
    def __init__(
        self,
        path: Union[str, Path],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        filename: Optional[str] = None
    ):
        self.path = Path(path)
        
        if not self.path.exists():
            raise FileNotFoundError(f"文件不存在: {path}")
        
        if media_type is None:
            media_type, _ = mimetypes.guess_type(str(self.path))
            media_type = media_type or "application/octet-stream"
        
        headers = headers or {}
        
        if filename:
            headers["content-disposition"] = f'attachment; filename="{filename}"'
        
        headers["content-length"] = str(self.path.stat().st_size)
        
        super().__init__(
            content="",
            status_code=status_code,
            headers=headers,
            media_type=media_type
        )
    
    async def _send_response(self, send):
        """异步发送文件"""
        # 发送响应头
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": [
                [key.encode(), value.encode()]
                for key, value in self.headers.items()
            ]
        })
        
        # 分块读取并发送文件
        chunk_size = 8192
        with open(self.path, "rb") as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                
                await send({
                    "type": "http.response.body",
                    "body": chunk,
                    "more_body": True
                })
        
        # 发送结束标志
        await send({
            "type": "http.response.body",
            "body": b"",
            "more_body": False
        })


class StreamingResponse(Response):
    """流式响应"""
    
    def __init__(
        self,
        content: Iterator[bytes],
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None
    ):
        self.content_iterator = content
        super().__init__(
            content="",
            status_code=status_code,
            headers=headers,
            media_type=media_type
        )
    
    async def _send_response(self, send):
        """发送流式响应"""
        # 移除Content-Length，因为是流式响应
        self.headers.pop("content-length", None)
        
        # 发送响应头
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": [
                [key.encode(), value.encode()]
                for key, value in self.headers.items()
            ]
        })
        
        # 流式发送内容
        try:
            for chunk in self.content_iterator:
                await send({
                    "type": "http.response.body",
                    "body": chunk,
                    "more_body": True
                })
        finally:
            # 发送结束标志
            await send({
                "type": "http.response.body",
                "body": b"",
                "more_body": False
            }) 