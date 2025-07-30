"""
异步路由系统 - 支持路径参数和WebSocket，现在支持类视图（CBV）
"""

import re
import inspect
from typing import Dict, List, Callable, Optional, Tuple, Any
from collections import defaultdict


class Route:
    """单个路由对象"""
    
    def __init__(self, path: str, handler: Callable, methods: List[str] = None, is_class_view: bool = False):
        self.path = path
        self.handler = handler
        self.methods = methods or ["GET"]
        self.is_class_view = is_class_view
        self.regex, self.param_names = self._compile_path(path)
    
    def _compile_path(self, path: str) -> Tuple[re.Pattern, List[str]]:
        """将路径编译为正则表达式"""
        param_names = []
        pattern = ""
        
        # 处理路径参数 {param} 和 {param:type}
        parts = re.split(r'(\{[^}]+\})', path)
        
        for part in parts:
            if part.startswith('{') and part.endswith('}'):
                # 解析参数
                param_spec = part[1:-1]
                if ':' in param_spec:
                    param_name, param_type = param_spec.split(':', 1)
                    if param_type == 'int':
                        pattern += r'(\d+)'
                    elif param_type == 'float':
                        pattern += r'(\d+\.?\d*)'
                    elif param_type == 'path':
                        pattern += r'(.+)'
                    else:
                        pattern += r'([^/]+)'
                else:
                    param_name = param_spec
                    pattern += r'([^/]+)'
                
                param_names.append(param_name)
            else:
                # 转义特殊字符
                pattern += re.escape(part)
        
        return re.compile(f'^{pattern}$'), param_names
    
    def match(self, path: str) -> Optional[Dict[str, Any]]:
        """匹配路径并提取参数"""
        match = self.regex.match(path)
        if not match:
            return None
        
        params = {}
        for i, name in enumerate(self.param_names):
            value = match.group(i + 1)
            # 尝试类型转换
            if value.isdigit():
                params[name] = int(value)
            elif '.' in value and value.replace('.', '').isdigit():
                params[name] = float(value)
            else:
                params[name] = value
        
        return params


class Router:
    """异步路由器 - 现在支持类视图"""
    
    def __init__(self):
        self.routes: List[Route] = []
        self.websocket_routes: List[Route] = []
        self.route_groups: Dict[str, List[Route]] = defaultdict(list)
    
    def add_route(self, path: str, handler: Callable, methods: List[str] = None, is_class_view: bool = False):
        """添加路由"""
        route = Route(path, handler, methods, is_class_view)
        self.routes.append(route)
        
        # 按方法分组以提高查找效率
        for method in route.methods:
            self.route_groups[method].append(route)
    
    def add_websocket_route(self, path: str, handler: Callable):
        """添加WebSocket路由"""
        route = Route(path, handler, ["WEBSOCKET"])
        self.websocket_routes.append(route)
    
    def add_class_view(self, path: str, view_class, methods: List[str] = None):
        """添加类视图路由"""
        # 如果没有指定方法，自动检测类视图支持的方法
        if methods is None:
            methods = self._get_view_methods(view_class)
        
        # 将类视图转换为视图函数
        view_func = view_class.as_view()
        self.add_route(path, view_func, methods, is_class_view=True)
    
    def _get_view_methods(self, view_class) -> List[str]:
        """自动检测类视图支持的HTTP方法"""
        methods = []
        for method in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
            if hasattr(view_class, method):
                methods.append(method.upper())
        
        # 如果没有找到任何方法，默认支持GET
        return methods if methods else ['GET']
    
    def resolve(self, method: str, path: str) -> Tuple[Optional[Callable], Dict[str, Any]]:
        """解析HTTP路由"""
        # 首先在对应方法的路由组中查找
        for route in self.route_groups.get(method, []):
            params = route.match(path)
            if params is not None:
                return route.handler, params
        
        return None, {}
    
    def resolve_websocket(self, path: str) -> Tuple[Optional[Callable], Dict[str, Any]]:
        """解析WebSocket路由"""
        for route in self.websocket_routes:
            params = route.match(path)
            if params is not None:
                return route.handler, params
        
        return None, {}
    
    # 装饰器方法
    def route(self, path: str, methods: List[str] = None):
        """路由装饰器"""
        def decorator(handler):
            self.add_route(path, handler, methods)
            return handler
        return decorator
    
    def get(self, path: str):
        """GET路由装饰器"""
        return self.route(path, ["GET"])
    
    def post(self, path: str):
        """POST路由装饰器"""
        return self.route(path, ["POST"])
    
    def put(self, path: str):
        """PUT路由装饰器"""
        return self.route(path, ["PUT"])
    
    def delete(self, path: str):
        """DELETE路由装饰器"""
        return self.route(path, ["DELETE"])
    
    def patch(self, path: str):
        """PATCH路由装饰器"""
        return self.route(path, ["PATCH"])
    
    def websocket(self, path: str):
        """WebSocket装饰器"""
        def decorator(handler):
            self.add_websocket_route(path, handler)
            return handler
        return decorator
    
    def include_router(self, other_router: 'Router', prefix: str = ""):
        """包含其他路由器"""
        for route in other_router.routes:
            new_path = prefix + route.path if prefix else route.path
            self.add_route(new_path, route.handler, route.methods, route.is_class_view)
        
        for route in other_router.websocket_routes:
            new_path = prefix + route.path if prefix else route.path
            self.add_websocket_route(new_path, route.handler)
    
    # 类视图相关的便捷方法
    def class_view(self, path: str, methods: List[str] = None):
        """类视图装饰器"""
        def decorator(view_class):
            self.add_class_view(path, view_class, methods)
            return view_class
        return decorator 