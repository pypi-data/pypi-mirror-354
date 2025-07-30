"""
类视图系统 - 支持RESTful CBV模式，现在支持模型驱动
"""

import inspect
import datetime
from typing import Dict, Any, Optional, List, Type, Union
from .response import JSONResponse, Response
from .exceptions import HTTPException


class BaseView:
    """基础视图类"""
    
    def __init__(self):
        self.request = None
    
    async def dispatch(self, request, **kwargs):
        """分发请求到对应的HTTP方法处理器"""
        self.request = request
        self.kwargs = kwargs
        
        # 获取HTTP方法对应的处理器
        method = request.method.lower()
        handler = getattr(self, method, None)
        
        if handler is None:
            # 如果没有对应的方法处理器，返回405错误
            allowed_methods = self.get_allowed_methods()
            raise HTTPException(
                405, 
                f"Method '{request.method}' not allowed. Allowed methods: {', '.join(allowed_methods)}"
            )
        
        # 调用处理器
        if inspect.iscoroutinefunction(handler):
            return await handler(request, **kwargs)
        else:
            return handler(request, **kwargs)
    
    def get_allowed_methods(self) -> List[str]:
        """获取允许的HTTP方法"""
        methods = []
        for method in ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']:
            if hasattr(self, method):
                methods.append(method.upper())
        return methods
    
    @classmethod
    def as_view(cls, **initkwargs):
        """将类视图转换为视图函数"""
        def view_func(request, **kwargs):
            view_instance = cls(**initkwargs)
            return view_instance.dispatch(request, **kwargs)
        
        # 保留类信息
        view_func.view_class = cls
        view_func.__name__ = cls.__name__
        view_func.__doc__ = cls.__doc__
        
        return view_func


class APIView(BaseView):
    """API视图基类"""
    
    def __init__(self):
        super().__init__()
        self.data = None
    
    async def dispatch(self, request, **kwargs):
        """重写分发方法，处理JSON数据"""
        # 预处理请求数据
        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                self.data = await request.json()
            except Exception:
                self.data = None
        
        return await super().dispatch(request, **kwargs)
    
    def get_serializer_data(self) -> Dict[str, Any]:
        """获取序列化数据 - 子类可重写"""
        return {}
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """获取上下文数据 - 子类可重写"""
        context = {
            'request': self.request,
            'view': self,
        }
        context.update(kwargs)
        return context


class GenericAPIView(APIView):
    """通用API视图 - 提供CRUD操作的基础实现"""
    
    # 子类可重写的属性
    serializer_class = None
    queryset = None
    lookup_field = 'id'
    
    def get_object(self, pk=None):
        """获取单个对象 - 子类需要实现具体逻辑"""
        obj_id = pk or self.kwargs.get(self.lookup_field)
        if not obj_id:
            raise HTTPException(400, f"Missing {self.lookup_field} parameter")
        
        # 这里应该从数据库或其他存储中获取对象
        # 子类需要重写此方法
        return {"id": obj_id, "message": "Override get_object method"}
    
    def get_queryset(self):
        """获取查询集 - 子类需要实现具体逻辑"""
        # 这里应该返回数据列表
        # 子类需要重写此方法
        return [{"id": i, "message": f"Item {i}"} for i in range(1, 6)]
    
    def perform_create(self, data):
        """执行创建操作 - 子类可重写"""
        # 这里应该实现实际的创建逻辑
        return {"id": 1, "created": True, **data}
    
    def perform_update(self, obj, data):
        """执行更新操作 - 子类可重写"""
        # 这里应该实现实际的更新逻辑
        obj.update(data)
        return obj
    
    def perform_destroy(self, obj):
        """执行删除操作 - 子类可重写"""
        # 这里应该实现实际的删除逻辑
        return {"deleted": True, "id": obj.get("id")}


# ================== 模型驱动的视图类 ==================

class ModelAPIView(APIView):
    """模型驱动的API视图基类"""
    
    # 子类需要设置的属性
    model = None
    lookup_field = 'id'
    fields = None  # 允许的字段列表，None表示所有字段
    exclude_fields = None  # 排除的字段列表
    
    def __init__(self):
        super().__init__()
        if self.model is None:
            raise ValueError("必须设置 model 属性")
    
    def get_queryset(self):
        """获取查询集"""
        return self.model.objects.all()
    
    async def get_object(self, pk=None):
        """获取单个对象"""
        obj_id = pk or self.kwargs.get(self.lookup_field)
        if not obj_id:
            raise HTTPException(400, f"Missing {self.lookup_field} parameter")
        
        try:
            filter_kwargs = {self.lookup_field: obj_id}
            return await self.model.objects.get(**filter_kwargs)
        except self.model.DoesNotExist:
            raise HTTPException(404, f"{self.model.__name__} 对象不存在")
    
    def serialize_object(self, obj) -> Dict[str, Any]:
        """序列化对象"""
        if hasattr(obj, 'to_dict'):
            data = obj.to_dict(exclude_fields=self.exclude_fields)
        else:
            # 如果不是模型对象，直接返回
            return obj if isinstance(obj, dict) else {"data": obj}
        
        # 过滤字段
        if self.fields is not None:
            data = {k: v for k, v in data.items() if k in self.fields}
        
        # 处理日期时间字段的序列化
        for key, value in data.items():
            if isinstance(value, datetime.datetime):
                data[key] = value.isoformat()
            elif isinstance(value, datetime.date):
                data[key] = value.isoformat()
        
        return data
    
    def get_create_data(self) -> Dict[str, Any]:
        """获取创建数据"""
        if not self.data:
            raise HTTPException(400, "Request body is required")
        
        # 过滤允许的字段
        if self.fields is not None:
            return {k: v for k, v in self.data.items() if k in self.fields}
        
        # 排除不允许的字段
        if self.exclude_fields is not None:
            return {k: v for k, v in self.data.items() if k not in self.exclude_fields}
        
        return self.data
    
    def get_update_data(self) -> Dict[str, Any]:
        """获取更新数据"""
        return self.get_create_data()


class ModelListAPIView(ModelAPIView):
    """模型列表API视图"""
    
    # 分页设置
    page_size = 20
    max_page_size = 100
    
    async def get(self, request, **kwargs):
        """处理GET请求 - 返回对象列表"""
        queryset = self.get_queryset()
        
        # 处理过滤
        filter_params = {}
        for key, value in request.query_params.items():
            if key not in ['page', 'page_size', 'ordering']:
                filter_params[key] = value
        
        if filter_params:
            queryset = queryset.filter(**filter_params)
        
        # 处理排序
        ordering = request.get_query_param('ordering')
        if ordering:
            order_fields = [field.strip() for field in ordering.split(',')]
            queryset = queryset.order_by(*order_fields)
        
        # 处理分页
        page = int(request.get_query_param('page', 1))
        page_size = min(
            int(request.get_query_param('page_size', self.page_size)),
            self.max_page_size
        )
        
        # 计算偏移量
        offset = (page - 1) * page_size
        queryset = queryset.offset(offset).limit(page_size)
        
        # 获取数据
        objects = await queryset.all()
        total_count = await self.get_queryset().count()
        
        # 序列化数据
        data = [self.serialize_object(obj) for obj in objects]
        
        return JSONResponse({
            "success": True,
            "data": data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total_count,
                "pages": (total_count + page_size - 1) // page_size
            }
        })


class ModelCreateAPIView(ModelAPIView):
    """模型创建API视图"""
    
    async def post(self, request, **kwargs):
        """处理POST请求 - 创建新对象"""
        create_data = self.get_create_data()
        
        try:
            # 使用模型管理器创建对象
            obj = await self.model.objects.create(**create_data)
            
            return JSONResponse({
                "success": True,
                "data": self.serialize_object(obj),
                "message": f"{self.model.__name__} 创建成功"
            }, status_code=201)
            
        except Exception as e:
            raise HTTPException(400, f"创建失败: {str(e)}")


class ModelRetrieveAPIView(ModelAPIView):
    """模型检索API视图"""
    
    async def get(self, request, **kwargs):
        """处理GET请求 - 返回单个对象"""
        obj = await self.get_object()
        
        return JSONResponse({
            "success": True,
            "data": self.serialize_object(obj)
        })


class ModelUpdateAPIView(ModelAPIView):
    """模型更新API视图"""
    
    async def put(self, request, **kwargs):
        """处理PUT请求 - 完整更新对象"""
        obj = await self.get_object()
        update_data = self.get_update_data()
        
        try:
            # 更新对象属性
            for key, value in update_data.items():
                setattr(obj, key, value)
            
            # 保存对象
            await obj.save()
            
            return JSONResponse({
                "success": True,
                "data": self.serialize_object(obj),
                "message": f"{self.model.__name__} 更新成功"
            })
            
        except Exception as e:
            raise HTTPException(400, f"更新失败: {str(e)}")
    
    async def patch(self, request, **kwargs):
        """处理PATCH请求 - 部分更新对象"""
        return await self.put(request, **kwargs)


class ModelDestroyAPIView(ModelAPIView):
    """模型删除API视图"""
    
    async def delete(self, request, **kwargs):
        """处理DELETE请求 - 删除对象"""
        obj = await self.get_object()
        
        try:
            obj_id = obj.pk
            await obj.delete()
            
            return JSONResponse({
                "success": True,
                "data": {"id": obj_id},
                "message": f"{self.model.__name__} 删除成功"
            })
            
        except Exception as e:
            raise HTTPException(400, f"删除失败: {str(e)}")


# ================== 非模型驱动的原有视图类 ==================

class ListAPIView(GenericAPIView):
    """列表API视图"""
    
    async def get(self, request, **kwargs):
        """处理GET请求 - 返回对象列表"""
        queryset = self.get_queryset()
        return JSONResponse({
            "success": True,
            "data": queryset,
            "count": len(queryset)
        })


class CreateAPIView(GenericAPIView):
    """创建API视图"""
    
    async def post(self, request, **kwargs):
        """处理POST请求 - 创建新对象"""
        if not self.data:
            raise HTTPException(400, "Request body is required")
        
        obj = self.perform_create(self.data)
        return JSONResponse({
            "success": True,
            "data": obj,
            "message": "Object created successfully"
        }, status_code=201)


class RetrieveAPIView(GenericAPIView):
    """检索API视图"""
    
    async def get(self, request, **kwargs):
        """处理GET请求 - 返回单个对象"""
        obj = self.get_object()
        return JSONResponse({
            "success": True,
            "data": obj
        })


class UpdateAPIView(GenericAPIView):
    """更新API视图"""
    
    async def put(self, request, **kwargs):
        """处理PUT请求 - 完整更新对象"""
        if not self.data:
            raise HTTPException(400, "Request body is required")
        
        obj = self.get_object()
        updated_obj = self.perform_update(obj, self.data)
        
        return JSONResponse({
            "success": True,
            "data": updated_obj,
            "message": "Object updated successfully"
        })
    
    async def patch(self, request, **kwargs):
        """处理PATCH请求 - 部分更新对象"""
        if not self.data:
            raise HTTPException(400, "Request body is required")
        
        obj = self.get_object()
        updated_obj = self.perform_update(obj, self.data)
        
        return JSONResponse({
            "success": True,
            "data": updated_obj,
            "message": "Object partially updated successfully"
        })


class DestroyAPIView(GenericAPIView):
    """删除API视图"""
    
    async def delete(self, request, **kwargs):
        """处理DELETE请求 - 删除对象"""
        obj = self.get_object()
        result = self.perform_destroy(obj)
        
        return JSONResponse({
            "success": True,
            "data": result,
            "message": "Object deleted successfully"
        }, status_code=204)


# ================== 组合视图类 ==================

class ListCreateAPIView(ListAPIView, CreateAPIView):
    """列表和创建API视图 - 组合视图"""
    pass


class RetrieveUpdateAPIView(RetrieveAPIView, UpdateAPIView):
    """检索和更新API视图 - 组合视图"""
    pass


class RetrieveUpdateDestroyAPIView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    """检索、更新和删除API视图 - 组合视图"""
    pass


class RetrieveDestroyAPIView(RetrieveAPIView, DestroyAPIView):
    """检索和删除API视图 - 组合视图"""
    pass


# ================== 模型驱动的组合视图类 ==================

class ModelListCreateAPIView(ModelListAPIView, ModelCreateAPIView):
    """模型列表和创建API视图 - 组合视图"""
    pass


class ModelRetrieveUpdateAPIView(ModelRetrieveAPIView, ModelUpdateAPIView):
    """模型检索和更新API视图 - 组合视图"""
    pass


class ModelRetrieveUpdateDestroyAPIView(ModelRetrieveAPIView, ModelUpdateAPIView, ModelDestroyAPIView):
    """模型检索、更新和删除API视图 - 组合视图"""
    pass


class ModelRetrieveDestroyAPIView(ModelRetrieveAPIView, ModelDestroyAPIView):
    """模型检索和删除API视图 - 组合视图"""
    pass


# ================== 视图集合 ==================

class ModelViewSet(ModelAPIView):
    """完整的模型视图集 - 包含所有CRUD操作"""
    
    async def get(self, request, **kwargs):
        """GET请求 - 根据是否有ID参数决定是列表还是详情"""
        if self.kwargs.get(self.lookup_field):
            # 有ID参数，返回单个对象
            obj = await self.get_object()
            return JSONResponse({
                "success": True,
                "data": self.serialize_object(obj)
            })
        else:
            # 没有ID参数，返回列表
            # 使用ModelListAPIView的逻辑
            list_view = ModelListAPIView()
            list_view.model = self.model
            list_view.fields = self.fields
            list_view.exclude_fields = self.exclude_fields
            return await list_view.get(request, **kwargs)
    
    async def post(self, request, **kwargs):
        """POST请求 - 创建新对象"""
        create_data = self.get_create_data()
        
        try:
            obj = await self.model.objects.create(**create_data)
            
            return JSONResponse({
                "success": True,
                "data": self.serialize_object(obj),
                "message": f"{self.model.__name__} 创建成功"
            }, status_code=201)
            
        except Exception as e:
            raise HTTPException(400, f"创建失败: {str(e)}")
    
    async def put(self, request, **kwargs):
        """PUT请求 - 完整更新对象"""
        obj = await self.get_object()
        update_data = self.get_update_data()
        
        try:
            for key, value in update_data.items():
                setattr(obj, key, value)
            
            await obj.save()
            
            return JSONResponse({
                "success": True,
                "data": self.serialize_object(obj),
                "message": f"{self.model.__name__} 更新成功"
            })
            
        except Exception as e:
            raise HTTPException(400, f"更新失败: {str(e)}")
    
    async def patch(self, request, **kwargs):
        """PATCH请求 - 部分更新对象"""
        return await self.put(request, **kwargs)
    
    async def delete(self, request, **kwargs):
        """DELETE请求 - 删除对象"""
        obj = await self.get_object()
        
        try:
            obj_id = obj.pk
            await obj.delete()
            
            return JSONResponse({
                "success": True,
                "data": {"id": obj_id},
                "message": f"{self.model.__name__} 删除成功"
            })
            
        except Exception as e:
            raise HTTPException(400, f"删除失败: {str(e)}")


# 保持向后兼容的非模型ViewSet
class GenericModelViewSet(GenericAPIView):
    """完整的模型视图集 - 包含所有CRUD操作（非模型驱动版本）"""
    
    async def get(self, request, **kwargs):
        """GET请求 - 根据是否有ID参数决定是列表还是详情"""
        if self.kwargs.get(self.lookup_field):
            # 有ID参数，返回单个对象
            obj = self.get_object()
            return JSONResponse({
                "success": True,
                "data": obj
            })
        else:
            # 没有ID参数，返回列表
            queryset = self.get_queryset()
            return JSONResponse({
                "success": True,
                "data": queryset,
                "count": len(queryset)
            })
    
    async def post(self, request, **kwargs):
        """POST请求 - 创建新对象"""
        if not self.data:
            raise HTTPException(400, "Request body is required")
        
        obj = self.perform_create(self.data)
        return JSONResponse({
            "success": True,
            "data": obj,
            "message": "Object created successfully"
        }, status_code=201)
    
    async def put(self, request, **kwargs):
        """PUT请求 - 完整更新对象"""
        if not self.data:
            raise HTTPException(400, "Request body is required")
        
        obj = self.get_object()
        updated_obj = self.perform_update(obj, self.data)
        
        return JSONResponse({
            "success": True,
            "data": updated_obj,
            "message": "Object updated successfully"
        })
    
    async def patch(self, request, **kwargs):
        """PATCH请求 - 部分更新对象"""
        if not self.data:
            raise HTTPException(400, "Request body is required")
        
        obj = self.get_object()
        updated_obj = self.perform_update(obj, self.data)
        
        return JSONResponse({
            "success": True,
            "data": updated_obj,
            "message": "Object partially updated successfully"
        })
    
    async def delete(self, request, **kwargs):
        """DELETE请求 - 删除对象"""
        obj = self.get_object()
        result = self.perform_destroy(obj)
        
        return JSONResponse({
            "success": True,
            "data": result,
            "message": "Object deleted successfully"
        }, status_code=204) 