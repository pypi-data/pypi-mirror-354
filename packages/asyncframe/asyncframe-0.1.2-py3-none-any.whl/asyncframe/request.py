"""
请求处理类 - 异步请求解析和数据处理
"""

import json
import urllib.parse
from typing import Dict, Any, Optional, List
from .url import URL


class Request:
    """异步HTTP请求对象"""
    
    def __init__(self, scope: Dict[str, Any], receive):
        self.scope = scope
        self.receive = receive
        self._body: Optional[bytes] = None
        self._json: Optional[Any] = None
        self._form: Optional[Dict[str, Any]] = None
        self.path_params: Dict[str, Any] = {}
    
    @property
    def method(self) -> str:
        """HTTP方法"""
        return self.scope["method"]
    
    @property
    def url(self) -> URL:
        """请求URL"""
        return URL(scope=self.scope)
    
    @property
    def headers(self) -> Dict[str, str]:
        """请求头"""
        return {
            key.decode(): value.decode()
            for key, value in self.scope.get("headers", [])
        }
    
    @property
    def query_params(self) -> Dict[str, List[str]]:
        """查询参数"""
        query_string = self.scope.get("query_string", b"").decode()
        params = urllib.parse.parse_qs(query_string, keep_blank_values=True)
        return params
    
    @property
    def client(self) -> Optional[List[str]]:
        """客户端信息"""
        return self.scope.get("client")
    
    async def body(self) -> bytes:
        """获取请求体"""
        if self._body is None:
            body_parts = []
            while True:
                message = await self.receive()
                if message["type"] == "http.request":
                    body_parts.append(message.get("body", b""))
                    if not message.get("more_body", False):
                        break
                elif message["type"] == "http.disconnect":
                    break
            
            self._body = b"".join(body_parts)
        
        return self._body
    
    async def text(self) -> str:
        """获取文本形式的请求体"""
        body = await self.body()
        return body.decode("utf-8")
    
    async def json(self) -> Any:
        """解析JSON请求体"""
        if self._json is None:
            text = await self.text()
            try:
                self._json = json.loads(text) if text else None
            except json.JSONDecodeError:
                self._json = None
        
        return self._json
    
    async def form(self) -> Dict[str, Any]:
        """解析表单数据"""
        if self._form is None:
            content_type = self.headers.get("content-type", "")
            
            if content_type.startswith("application/x-www-form-urlencoded"):
                text = await self.text()
                self._form = dict(urllib.parse.parse_qsl(text))
            elif content_type.startswith("multipart/form-data"):
                # 简化的multipart解析，实际项目中应使用专门的库
                self._form = await self._parse_multipart()
            else:
                self._form = {}
        
        return self._form
    
    async def _parse_multipart(self) -> Dict[str, Any]:
        """简化的multipart解析"""
        # 这里只是一个基础实现，实际项目中建议使用
        # python-multipart 或类似的库
        return {}
    
    def get_header(self, name: str, default: str = None) -> Optional[str]:
        """获取单个请求头"""
        return self.headers.get(name.lower(), default)
    
    def get_query_param(self, name: str, default: Any = None) -> Any:
        """获取单个查询参数"""
        values = self.query_params.get(name, [])
        return values[0] if values else default
    
    def get_query_params(self, name: str) -> List[str]:
        """获取多个同名查询参数"""
        return self.query_params.get(name, [])
    
    @property
    def cookies(self) -> Dict[str, str]:
        """解析Cookies"""
        cookie_header = self.get_header("cookie", "")
        cookies = {}
        
        for item in cookie_header.split(";"):
            item = item.strip()
            if "=" in item:
                key, value = item.split("=", 1)
                cookies[key.strip()] = value.strip()
        
        return cookies
    
    def get_cookie(self, name: str, default: str = None) -> Optional[str]:
        """获取单个Cookie"""
        return self.cookies.get(name, default)
    
    @property
    def is_secure(self) -> bool:
        """是否为HTTPS请求"""
        return self.scope.get("scheme") == "https"
    
    @property
    def user_agent(self) -> Optional[str]:
        """获取User-Agent"""
        return self.get_header("user-agent")
    
    @property
    def content_type(self) -> Optional[str]:
        """获取Content-Type"""
        return self.get_header("content-type")
    
    @property
    def content_length(self) -> Optional[int]:
        """获取Content-Length"""
        length = self.get_header("content-length")
        return int(length) if length and length.isdigit() else None 