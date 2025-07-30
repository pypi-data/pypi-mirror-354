'''
Author: jiaochanghao jch_2154195820@163.com
Date: 2025-06-05 17:40:54
LastEditors: jiaochanghao jch_2154195820@163.com
LastEditTime: 2025-06-05 17:43:24
FilePath: /web_server/asyncframe/url.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
"""
URL处理类 - URL解析和操作
"""

import urllib.parse
from typing import Dict, Any


class URL:
    """URL处理类"""
    
    def __init__(self, scope: Dict[str, Any]):
        self.scope = scope
        
    @property
    def scheme(self) -> str:
        """URL协议"""
        return self.scope.get("scheme", "http")
    
    @property
    def netloc(self) -> str:
        """网络位置"""
        host = self.scope.get("server", ["localhost", None])[0]
        port = self.scope.get("server", [None, 80])[1]
        
        if (self.scheme == "http" and port == 80) or (self.scheme == "https" and port == 443):
            return host
        return f"{host}:{port}"
    
    @property
    def path(self) -> str:
        """URL路径"""
        return self.scope.get("path", "/")
    
    @property
    def query(self) -> str:
        """查询字符串"""
        return self.scope.get("query_string", b"").decode()
    
    @property
    def fragment(self) -> str:
        """URL片段"""
        return ""
    
    def __str__(self) -> str:
        """完整URL字符串"""
        url = f"{self.scheme}://{self.netloc}{self.path}"
        if self.query:
            url += f"?{self.query}"
        return url
    
    @property
    def hostname(self) -> str:
        """主机名"""
        return self.scope.get("server", ["localhost", None])[0]
    
    @property
    def port(self) -> int:
        """端口号"""
        return self.scope.get("server", [None, 80])[1] 