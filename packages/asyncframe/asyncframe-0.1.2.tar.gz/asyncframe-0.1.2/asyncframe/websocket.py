"""
WebSocket支持 - 异步WebSocket连接处理
"""

import json
from typing import Dict, Any, Optional


class WebSocket:
    """WebSocket连接处理类"""
    
    def __init__(self, scope: Dict[str, Any], receive, send):
        self.scope = scope
        self.receive = receive
        self.send = send
        self.path_params: Dict[str, Any] = {}
        self._accepted = False
        self._closed = False
    
    @property
    def url(self):
        """WebSocket URL"""
        from .url import URL
        return URL(scope=self.scope)
    
    @property
    def headers(self) -> Dict[str, str]:
        """请求头"""
        return {
            key.decode(): value.decode()
            for key, value in self.scope.get("headers", [])
        }
    
    async def accept(self, subprotocol: Optional[str] = None):
        """接受WebSocket连接"""
        if self._accepted:
            raise RuntimeError("WebSocket连接已被接受")
        
        message = {"type": "websocket.accept"}
        if subprotocol:
            message["subprotocol"] = subprotocol
        
        await self.send(message)
        self._accepted = True
    
    async def close(self, code: int = 1000, reason: str = ""):
        """关闭WebSocket连接"""
        if not self._closed:
            await self.send({
                "type": "websocket.close",
                "code": code,
                "reason": reason
            })
            self._closed = True
    
    async def send_text(self, data: str):
        """发送文本消息"""
        if not self._accepted:
            raise RuntimeError("必须先接受WebSocket连接")
        
        await self.send({
            "type": "websocket.send",
            "text": data
        })
    
    async def send_bytes(self, data: bytes):
        """发送二进制消息"""
        if not self._accepted:
            raise RuntimeError("必须先接受WebSocket连接")
        
        await self.send({
            "type": "websocket.send", 
            "bytes": data
        })
    
    async def send_json(self, data: Any):
        """发送JSON消息"""
        text = json.dumps(data, ensure_ascii=False)
        await self.send_text(text)
    
    async def receive_text(self) -> str:
        """接收文本消息"""
        message = await self.receive()
        
        if message["type"] == "websocket.receive":
            return message.get("text", "")
        elif message["type"] == "websocket.disconnect":
            raise ConnectionClosed()
        else:
            raise RuntimeError(f"意外的消息类型: {message['type']}")
    
    async def receive_bytes(self) -> bytes:
        """接收二进制消息"""
        message = await self.receive()
        
        if message["type"] == "websocket.receive":
            return message.get("bytes", b"")
        elif message["type"] == "websocket.disconnect":
            raise ConnectionClosed()
        else:
            raise RuntimeError(f"意外的消息类型: {message['type']}")
    
    async def receive_json(self) -> Any:
        """接收JSON消息"""
        text = await self.receive_text()
        return json.loads(text) if text else None
    
    async def iter_text(self):
        """迭代接收文本消息"""
        try:
            while True:
                yield await self.receive_text()
        except ConnectionClosed:
            pass
    
    async def iter_bytes(self):
        """迭代接收二进制消息"""
        try:
            while True:
                yield await self.receive_bytes()
        except ConnectionClosed:
            pass
    
    async def iter_json(self):
        """迭代接收JSON消息"""
        try:
            while True:
                yield await self.receive_json()
        except ConnectionClosed:
            pass


class ConnectionClosed(Exception):
    """WebSocket连接已关闭异常"""
    pass 