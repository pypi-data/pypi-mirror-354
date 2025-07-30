"""
AsyncFrame - 现代异步Python Web框架
现在支持函数视图（FBV）和类视图（CBV）两种编程风格，以及完整的异步ORM系统
"""

# 核心组件
from .application import AsyncFrame
from .request import Request
from .response import Response, JSONResponse, HTMLResponse, RedirectResponse
from .routing import Router
from .exceptions import HTTPException, NotFound, BadRequest, Unauthorized, Forbidden, InternalServerError

# 数据库和模型
from .database import DatabaseConfig, DatabasePool, DatabaseManager, db_manager
from .models import Model, QuerySet, Manager, create_tables, drop_tables
from .fields import (
    Field, CharField, TextField, IntegerField, DateTimeField, 
    BooleanField, JSONField, ForeignKeyField, ValidationError,
    email_validator, url_validator
)

# 迁移系统
from .migrations import Migration, MigrationManager, migration_manager

# 类视图支持（包含模型驱动视图）
from .views import (
    # 基础视图
    BaseView, APIView, GenericAPIView,
    
    # 非模型驱动视图
    ListAPIView, CreateAPIView, RetrieveAPIView, 
    UpdateAPIView, DestroyAPIView,
    ListCreateAPIView, RetrieveUpdateAPIView, 
    RetrieveUpdateDestroyAPIView, RetrieveDestroyAPIView,
    GenericModelViewSet,
    
    # 模型驱动视图
    ModelAPIView, ModelListAPIView, ModelCreateAPIView,
    ModelRetrieveAPIView, ModelUpdateAPIView, ModelDestroyAPIView,
    ModelListCreateAPIView, ModelRetrieveUpdateAPIView,
    ModelRetrieveUpdateDestroyAPIView, ModelRetrieveDestroyAPIView,
    ModelViewSet
)

# WebSocket支持
from .websocket import WebSocket

# 后台任务
from .background import BackgroundTaskManager

__version__ = "0.1.0"
__author__ = "0716gzs"

__all__ = [
    # 核心
    "AsyncFrame",
    "Request", 
    "Response",
    "JSONResponse",
    "HTMLResponse", 
    "RedirectResponse",
    "Router",
    
    # 异常
    "HTTPException",
    "NotFound",
    "BadRequest", 
    "Unauthorized",
    "Forbidden",
    "InternalServerError",
    
    # 数据库
    "DatabaseConfig",
    "DatabasePool", 
    "DatabaseManager",
    "db_manager",
    
    # 模型
    "Model",
    "QuerySet",
    "Manager",
    "DoesNotExist",
    "MultipleObjectsReturned",
    "create_tables",
    "drop_tables",
    
    # 字段
    "Field",
    "CharField",
    "TextField", 
    "IntegerField",
    "BigIntegerField",
    "FloatField",
    "DecimalField",
    "BooleanField",
    "DateTimeField",
    "DateField",
    "JSONField",
    "ForeignKeyField",
    "ValidationError",
    "email_validator",
    "url_validator",
    "min_length_validator",
    "max_length_validator",
    
    # 基础视图
    "BaseView",
    "APIView", 
    "GenericAPIView",
    
    # 非模型驱动视图
    "ListAPIView",
    "CreateAPIView",
    "RetrieveAPIView",
    "UpdateAPIView", 
    "DestroyAPIView",
    "ListCreateAPIView",
    "RetrieveUpdateAPIView",
    "RetrieveUpdateDestroyAPIView",
    "RetrieveDestroyAPIView", 
    "GenericModelViewSet",
    
    # 模型驱动视图
    "ModelAPIView",
    "ModelListAPIView",
    "ModelCreateAPIView",
    "ModelRetrieveAPIView",
    "ModelUpdateAPIView",
    "ModelDestroyAPIView",
    "ModelListCreateAPIView",
    "ModelRetrieveUpdateAPIView", 
    "ModelRetrieveUpdateDestroyAPIView",
    "ModelRetrieveDestroyAPIView",
    "ModelViewSet",
    
    # WebSocket
    "WebSocket",
    
    # 后台任务
    "BackgroundTaskManager",
] 
