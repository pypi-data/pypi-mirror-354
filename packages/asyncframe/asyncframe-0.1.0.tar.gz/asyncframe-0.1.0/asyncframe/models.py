"""
异步模型系统 - 提供ORM功能
"""

import datetime
import logging
from typing import Dict, Any, Optional, List, Type, Union, Tuple
from .fields import Field, IntegerField, DateTimeField, ValidationError
from .database import db_manager, DatabasePool


logger = logging.getLogger(__name__)


class DoesNotExist(Exception):
    """对象不存在异常"""
    pass


class MultipleObjectsReturned(Exception):
    """返回多个对象异常"""
    pass


class QuerySet:
    """异步查询集"""
    
    def __init__(self, model_class: Type['Model'], db_pool: DatabasePool = None):
        self.model_class = model_class
        self.db_pool = db_pool or db_manager.get_database()
        self._filters = []
        self._order_by = []
        self._limit = None
        self._offset = None
        self._select_related = []
        
    def filter(self, **kwargs) -> 'QuerySet':
        """添加过滤条件"""
        new_qs = self._clone()
        for key, value in kwargs.items():
            new_qs._filters.append((key, value))
        return new_qs
    
    def exclude(self, **kwargs) -> 'QuerySet':
        """排除条件"""
        new_qs = self._clone()
        for key, value in kwargs.items():
            new_qs._filters.append((f"NOT {key}", value))
        return new_qs
    
    def order_by(self, *fields) -> 'QuerySet':
        """排序"""
        new_qs = self._clone()
        new_qs._order_by.extend(fields)
        return new_qs
    
    def limit(self, count: int) -> 'QuerySet':
        """限制数量"""
        new_qs = self._clone()
        new_qs._limit = count
        return new_qs
    
    def offset(self, count: int) -> 'QuerySet':
        """偏移量"""
        new_qs = self._clone()
        new_qs._offset = count
        return new_qs
    
    def select_related(self, *fields) -> 'QuerySet':
        """预加载关联对象"""
        new_qs = self._clone()
        new_qs._select_related.extend(fields)
        return new_qs
    
    async def all(self) -> List['Model']:
        """获取所有对象"""
        query, params = self._build_select_query()
        rows = await self.db_pool.fetch_all(query, params)
        return [self.model_class(**row) for row in rows]
    
    async def first(self) -> Optional['Model']:
        """获取第一个对象"""
        query, params = self._build_select_query(limit=1)
        row = await self.db_pool.fetch_one(query, params)
        return self.model_class(**row) if row else None
    
    async def get(self, **kwargs) -> 'Model':
        """获取单个对象"""
        qs = self.filter(**kwargs)
        query, params = qs._build_select_query()
        rows = await self.db_pool.fetch_all(query, params)
        
        if not rows:
            raise DoesNotExist(f"{self.model_class.__name__} 对象不存在")
        
        if len(rows) > 1:
            raise MultipleObjectsReturned(f"查询返回了 {len(rows)} 个 {self.model_class.__name__} 对象")
        
        return self.model_class(**rows[0])
    
    async def count(self) -> int:
        """计数"""
        query, params = self._build_count_query()
        result = await self.db_pool.fetch_one(query, params)
        return result['count'] if result else 0
    
    async def exists(self) -> bool:
        """检查是否存在"""
        count = await self.count()
        return count > 0
    
    async def delete(self) -> int:
        """批量删除"""
        query, params = self._build_delete_query()
        result = await self.db_pool.execute(query, params)
        return result
    
    async def update(self, **kwargs) -> int:
        """批量更新"""
        query, params = self._build_update_query(kwargs)
        result = await self.db_pool.execute(query, params)
        return result
    
    def _clone(self) -> 'QuerySet':
        """克隆查询集"""
        new_qs = QuerySet(self.model_class, self.db_pool)
        new_qs._filters = self._filters.copy()
        new_qs._order_by = self._order_by.copy()
        new_qs._limit = self._limit
        new_qs._offset = self._offset
        new_qs._select_related = self._select_related.copy()
        return new_qs
    
    def _build_select_query(self, limit: Optional[int] = None) -> Tuple[str, Dict[str, Any]]:
        """构建SELECT查询"""
        table_name = self.model_class._meta.table_name
        
        # 构建SELECT子句
        columns = ', '.join([f.get_db_column_name() for f in self.model_class._meta.fields.values()])
        query_parts = [f"SELECT {columns} FROM {table_name}"]
        
        # 构建WHERE子句
        where_conditions = []
        params = {}
        param_counter = 0
        
        for condition, value in self._filters:
            param_counter += 1
            param_name = f"param_{param_counter}"
            
            if '__' in condition:
                # 处理查询操作符 (如 name__icontains, age__gt 等)
                field_name, operator = condition.split('__', 1)
                where_conditions.append(self._build_condition(field_name, operator, param_name))
            else:
                # 简单相等条件
                where_conditions.append(f"{condition} = :{param_name}")
            
            params[param_name] = value
        
        if where_conditions:
            query_parts.append(f"WHERE {' AND '.join(where_conditions)}")
        
        # ORDER BY
        if self._order_by:
            order_fields = []
            for field in self._order_by:
                if field.startswith('-'):
                    order_fields.append(f"{field[1:]} DESC")
                else:
                    order_fields.append(f"{field} ASC")
            query_parts.append(f"ORDER BY {', '.join(order_fields)}")
        
        # LIMIT 和 OFFSET
        if limit or self._limit:
            query_parts.append(f"LIMIT {limit or self._limit}")
        
        if self._offset:
            query_parts.append(f"OFFSET {self._offset}")
        
        return ' '.join(query_parts), params
    
    def _build_count_query(self) -> Tuple[str, Dict[str, Any]]:
        """构建COUNT查询"""
        table_name = self.model_class._meta.table_name
        
        query_parts = [f"SELECT COUNT(*) as count FROM {table_name}"]
        
        # WHERE子句
        where_conditions = []
        params = {}
        param_counter = 0
        
        for condition, value in self._filters:
            param_counter += 1
            param_name = f"param_{param_counter}"
            
            if '__' in condition:
                field_name, operator = condition.split('__', 1)
                where_conditions.append(self._build_condition(field_name, operator, param_name))
            else:
                where_conditions.append(f"{condition} = :{param_name}")
            
            params[param_name] = value
        
        if where_conditions:
            query_parts.append(f"WHERE {' AND '.join(where_conditions)}")
        
        return ' '.join(query_parts), params
    
    def _build_delete_query(self) -> Tuple[str, Dict[str, Any]]:
        """构建DELETE查询"""
        table_name = self.model_class._meta.table_name
        
        query_parts = [f"DELETE FROM {table_name}"]
        
        # WHERE子句
        where_conditions = []
        params = {}
        param_counter = 0
        
        for condition, value in self._filters:
            param_counter += 1
            param_name = f"param_{param_counter}"
            
            if '__' in condition:
                field_name, operator = condition.split('__', 1)
                where_conditions.append(self._build_condition(field_name, operator, param_name))
            else:
                where_conditions.append(f"{condition} = :{param_name}")
            
            params[param_name] = value
        
        if where_conditions:
            query_parts.append(f"WHERE {' AND '.join(where_conditions)}")
        
        return ' '.join(query_parts), params
    
    def _build_update_query(self, update_fields: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        """构建UPDATE查询"""
        table_name = self.model_class._meta.table_name
        
        # SET子句
        set_conditions = []
        params = {}
        param_counter = 0
        
        for field_name, value in update_fields.items():
            param_counter += 1
            param_name = f"set_param_{param_counter}"
            set_conditions.append(f"{field_name} = :{param_name}")
            params[param_name] = value
        
        query_parts = [f"UPDATE {table_name} SET {', '.join(set_conditions)}"]
        
        # WHERE子句
        where_conditions = []
        for condition, value in self._filters:
            param_counter += 1
            param_name = f"where_param_{param_counter}"
            
            if '__' in condition:
                field_name, operator = condition.split('__', 1)
                where_conditions.append(self._build_condition(field_name, operator, param_name))
            else:
                where_conditions.append(f"{condition} = :{param_name}")
            
            params[param_name] = value
        
        if where_conditions:
            query_parts.append(f"WHERE {' AND '.join(where_conditions)}")
        
        return ' '.join(query_parts), params
    
    def _build_condition(self, field_name: str, operator: str, param_name: str) -> str:
        """构建条件表达式"""
        operators_map = {
            'exact': f"{field_name} = :{param_name}",
            'iexact': f"LOWER({field_name}) = LOWER(:{param_name})",
            'contains': f"{field_name} LIKE '%' || :{param_name} || '%'",
            'icontains': f"LOWER({field_name}) LIKE '%' || LOWER(:{param_name}) || '%'",
            'startswith': f"{field_name} LIKE :{param_name} || '%'",
            'endswith': f"{field_name} LIKE '%' || :{param_name}",
            'gt': f"{field_name} > :{param_name}",
            'gte': f"{field_name} >= :{param_name}",
            'lt': f"{field_name} < :{param_name}",
            'lte': f"{field_name} <= :{param_name}",
            'in': f"{field_name} IN (:{param_name})",
            'isnull': f"{field_name} IS NULL" if param_name else f"{field_name} IS NOT NULL",
        }
        
        return operators_map.get(operator, f"{field_name} = :{param_name}")


class Manager:
    """模型管理器"""
    
    def __init__(self, model_class: Type['Model']):
        self.model_class = model_class
    
    def get_queryset(self) -> QuerySet:
        """获取查询集"""
        return QuerySet(self.model_class)
    
    def all(self) -> QuerySet:
        """获取所有对象的查询集"""
        return self.get_queryset()
    
    def filter(self, **kwargs) -> QuerySet:
        """过滤查询集"""
        return self.get_queryset().filter(**kwargs)
    
    def exclude(self, **kwargs) -> QuerySet:
        """排除查询集"""
        return self.get_queryset().exclude(**kwargs)
    
    def order_by(self, *fields) -> QuerySet:
        """排序查询集"""
        return self.get_queryset().order_by(*fields)
    
    async def get(self, **kwargs) -> 'Model':
        """根据条件获取单个对象"""
        return await self.get_queryset().get(**kwargs)
    
    async def first(self) -> Optional['Model']:
        """获取第一个对象"""
        return await self.get_queryset().first()
    
    async def last(self) -> Optional['Model']:
        """获取最后一个对象"""
        return await self.get_queryset().order_by('-id').first()
    
    async def count(self) -> int:
        """计数"""
        return await self.get_queryset().count()
    
    async def exists(self) -> bool:
        """检查是否存在"""
        return await self.get_queryset().exists()
    
    # ==================== 新增数据方法 ====================
    
    async def create(self, **kwargs) -> 'Model':
        """创建单个新对象"""
        instance = self.model_class(**kwargs)
        await instance.save()
        return instance
    
    async def bulk_create(self, objects: List[Dict[str, Any]], batch_size: int = 1000) -> List['Model']:
        """批量创建多个对象
        
        Args:
            objects: 包含字段数据的字典列表
            batch_size: 每批处理的数量
            
        Returns:
            创建的模型实例列表
        """
        if not objects:
            return []
        
        db_pool = db_manager.get_database()
        table_name = self.model_class._meta.table_name
        created_instances = []
        
        # 获取字段名（排除主键，因为它是自增的）
        fields = []
        for field_name, field in self.model_class._meta.fields.items():
            if not field.primary_key:
                fields.append(field_name)
        
        if not fields:
            return []
        
        # 分批处理
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            
            # 构建批量插入SQL
            placeholders = ', '.join([f":{field}" for field in fields])
            query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({placeholders})"
            
            # 逐个执行插入（因为没有execute_many方法）
            for obj_data in batch:
                params = {}
                for field_name in fields:
                    value = obj_data.get(field_name)
                    # 处理默认值
                    if value is None:
                        field_obj = self.model_class._meta.fields[field_name]
                        if field_obj.default is not None:
                            if callable(field_obj.default):
                                value = field_obj.default()
                            else:
                                value = field_obj.default
                    params[field_name] = value
                
                # 执行插入
                await db_pool.execute(query, params)
                
                # 创建模型实例
                instance = self.model_class(**obj_data)
                instance._is_new = False
                created_instances.append(instance)
        
        return created_instances
    
    async def get_or_create(self, defaults: Dict[str, Any] = None, **kwargs) -> Tuple['Model', bool]:
        """获取或创建对象
        
        Args:
            defaults: 创建时使用的默认值
            **kwargs: 查找条件
            
        Returns:
            (对象实例, 是否为新创建)
        """
        try:
            obj = await self.get(**kwargs)
            return obj, False
        except DoesNotExist:
            create_kwargs = kwargs.copy()
            if defaults:
                create_kwargs.update(defaults)
            obj = await self.create(**create_kwargs)
            return obj, True
    
    async def update_or_create(self, defaults: Dict[str, Any] = None, **kwargs) -> Tuple['Model', bool]:
        """更新或创建对象
        
        Args:
            defaults: 更新/创建时使用的值
            **kwargs: 查找条件
            
        Returns:
            (对象实例, 是否为新创建)
        """
        try:
            obj = await self.get(**kwargs)
            if defaults:
                for key, value in defaults.items():
                    setattr(obj, key, value)
                await obj.save()
            return obj, False
        except DoesNotExist:
            create_kwargs = kwargs.copy()
            if defaults:
                create_kwargs.update(defaults)
            obj = await self.create(**create_kwargs)
            return obj, True
    
    # ==================== 更新数据方法 ====================
    
    async def bulk_update(self, objects: List['Model'], fields: List[str], batch_size: int = 1000) -> int:
        """批量更新对象
        
        Args:
            objects: 要更新的模型实例列表
            fields: 要更新的字段名列表
            batch_size: 每批处理的数量
            
        Returns:
            更新的记录数
        """
        if not objects or not fields:
            return 0
        
        db_pool = db_manager.get_database()
        table_name = self.model_class._meta.table_name
        pk_field = self.model_class._meta.primary_key.name
        updated_count = 0
        
        # 分批处理
        for i in range(0, len(objects), batch_size):
            batch = objects[i:i + batch_size]
            
            for obj in batch:
                if obj.pk is None:
                    continue
                
                # 构建更新SQL
                set_clauses = [f"{field} = :{field}" for field in fields]
                query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE {pk_field} = :pk"
                
                # 准备参数
                params = {'pk': obj.pk}
                for field in fields:
                    params[field] = getattr(obj, field)
                
                # 执行更新
                result = await db_pool.execute(query, params)
                if result:
                    updated_count += 1
        
        return updated_count
    
    # ==================== 删除数据方法 ====================
    
    async def bulk_delete(self, objects: List['Model']) -> int:
        """批量删除对象
        
        Args:
            objects: 要删除的模型实例列表
            
        Returns:
            删除的记录数
        """
        if not objects:
            return 0
        
        pks = [obj.pk for obj in objects if obj.pk is not None]
        if not pks:
            return 0
        
        return await self.filter(pk__in=pks).delete()
    
    # ==================== 查询数据方法 ====================
    
    async def find_one(self, **kwargs) -> Optional['Model']:
        """根据条件查找单个对象（不存在时返回None）"""
        try:
            return await self.get(**kwargs)
        except DoesNotExist:
            return None
    
    async def find_many(self, limit: int = None, **kwargs) -> List['Model']:
        """根据条件查找多个对象
        
        Args:
            limit: 限制返回数量
            **kwargs: 查询条件
            
        Returns:
            模型实例列表
        """
        qs = self.filter(**kwargs)
        if limit:
            qs = qs.limit(limit)
        return await qs.all()
    
    async def search(self, query: str, fields: List[str]) -> List['Model']:
        """在指定字段中搜索文本
        
        Args:
            query: 搜索关键词
            fields: 要搜索的字段列表
            
        Returns:
            匹配的模型实例列表
        """
        if not query or not fields:
            return []
        
        db_pool = db_manager.get_database()
        table_name = self.model_class._meta.table_name
        
        # 构建OR条件的WHERE子句
        conditions = []
        params = {}
        
        for i, field in enumerate(fields):
            param_name = f"search_param_{i}"
            conditions.append(f"{field} LIKE :{param_name}")
            params[param_name] = f"%{query}%"
        
        # 构建完整的SQL查询 - 获取所有字段
        all_fields = list(self.model_class._meta.fields.keys())
        columns = ', '.join(all_fields)
        where_clause = ' OR '.join(conditions)
        sql_query = f"SELECT {columns} FROM {table_name} WHERE {where_clause}"
        
        # 执行查询
        rows = await db_pool.fetch_all(sql_query, params)
        return [self.model_class(**row) for row in rows]
    
    async def paginate(self, page: int = 1, per_page: int = 20, **kwargs) -> Dict[str, Any]:
        """分页查询
        
        Args:
            page: 页码（从1开始）
            per_page: 每页数量
            **kwargs: 查询条件
            
        Returns:
            包含分页信息的字典
        """
        if page < 1:
            page = 1
        
        offset = (page - 1) * per_page
        
        # 获取总数
        total_count = await self.filter(**kwargs).count()
        
        # 获取当前页数据
        items = await self.filter(**kwargs).offset(offset).limit(per_page).all()
        
        # 计算分页信息
        total_pages = (total_count + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
        
        return {
            'items': items,
            'page': page,
            'per_page': per_page,
            'total_count': total_count,
            'total_pages': total_pages,
            'has_prev': has_prev,
            'has_next': has_next,
            'prev_page': page - 1 if has_prev else None,
            'next_page': page + 1 if has_next else None
        }
    
    # ==================== 聚合查询方法 ====================
    
    async def aggregate(self, **expressions) -> Dict[str, Any]:
        """聚合查询
        
        Args:
            **expressions: 聚合表达式，如 avg_age='AVG(age)', max_id='MAX(id)'
            
        Returns:
            聚合结果字典
        """
        db_pool = db_manager.get_database()
        table_name = self.model_class._meta.table_name
        
        if not expressions:
            return {}
        
        # 构建聚合查询
        select_parts = []
        for alias, expression in expressions.items():
            select_parts.append(f"{expression} as {alias}")
        
        query = f"SELECT {', '.join(select_parts)} FROM {table_name}"
        result = await db_pool.fetch_one(query)
        
        return dict(result) if result else {}
    
    async def values(self, *fields) -> List[Dict[str, Any]]:
        """获取指定字段的值
        
        Args:
            *fields: 字段名列表
            
        Returns:
            包含字段值的字典列表
        """
        if not fields:
            fields = list(self.model_class._meta.fields.keys())
        
        db_pool = db_manager.get_database()
        table_name = self.model_class._meta.table_name
        
        query = f"SELECT {', '.join(fields)} FROM {table_name}"
        rows = await db_pool.fetch_all(query)
        
        return [dict(row) for row in rows]
    
    async def values_list(self, *fields, flat: bool = False) -> List[Any]:
        """获取指定字段的值列表
        
        Args:
            *fields: 字段名列表
            flat: 如果只有一个字段且为True，返回扁平列表
            
        Returns:
            值的列表或元组列表
        """
        if not fields:
            fields = list(self.model_class._meta.fields.keys())
        
        db_pool = db_manager.get_database()
        table_name = self.model_class._meta.table_name
        
        query = f"SELECT {', '.join(fields)} FROM {table_name}"
        rows = await db_pool.fetch_all(query)
        
        if flat and len(fields) == 1:
            return [row[fields[0]] for row in rows]
        else:
            return [tuple(row[field] for field in fields) for row in rows]


class ModelMeta:
    """模型元数据"""
    
    def __init__(self, model_class):
        self.model_class = model_class
        self.fields = {}
        self.table_name = getattr(model_class, '__tablename__', None) or model_class.__name__.lower()
        self.primary_key = None
        
        # 收集字段
        for name, attr in model_class.__dict__.items():
            if isinstance(attr, Field):
                attr.name = name
                attr.model_class = model_class
                self.fields[name] = attr
                
                if attr.primary_key:
                    self.primary_key = attr
        
        # 如果没有定义主键，自动添加id字段
        if self.primary_key is None:
            id_field = IntegerField(primary_key=True, null=False)
            id_field.name = 'id'
            id_field.model_class = model_class
            self.fields['id'] = id_field
            self.primary_key = id_field
            setattr(model_class, 'id', id_field)


class ModelMetaclass(type):
    """模型元类"""
    
    def __new__(mcs, name, bases, namespace, **kwargs):
        # 创建类
        cls = super().__new__(mcs, name, bases, namespace)
        
        # 只为非基类Model创建元数据
        if name != 'Model' and any(isinstance(base, ModelMetaclass) for base in bases):
            cls._meta = ModelMeta(cls)
            
            # 添加默认管理器
            if not hasattr(cls, 'objects'):
                cls.objects = Manager(cls)
            
            # 添加异常类
            cls.DoesNotExist = type(f'{name}DoesNotExist', (DoesNotExist,), {})
            cls.MultipleObjectsReturned = type(f'{name}MultipleObjectsReturned', (MultipleObjectsReturned,), {})
        
        return cls


class Model(metaclass=ModelMetaclass):
    """异步模型基类"""
    
    def __init__(self, **kwargs):
        # 设置字段值
        for field_name, field in self._meta.fields.items():
            value = kwargs.get(field_name, None)
            if value is None and field.default is not None:
                if callable(field.default):
                    value = field.default()
                else:
                    value = field.default
            setattr(self, field_name, value)
        
        # 标记是否为新对象
        self._is_new = True
        if self.pk is not None:
            self._is_new = False
    
    @property
    def pk(self):
        """主键值"""
        return getattr(self, self._meta.primary_key.name, None)
    
    @pk.setter
    def pk(self, value):
        """设置主键值"""
        setattr(self, self._meta.primary_key.name, value)
    
    async def save(self, force_insert: bool = False, force_update: bool = False):
        """保存对象"""
        db_pool = db_manager.get_database()
        
        # 验证字段
        self.full_clean()
        
        # 处理自动时间字段
        self._handle_auto_datetime_fields()
        
        if force_insert or (self._is_new and not force_update):
            await self._insert(db_pool)
        else:
            await self._update(db_pool)
    
    async def delete(self):
        """删除对象"""
        if self.pk is None:
            raise ValueError("无法删除没有主键的对象")
        
        db_pool = db_manager.get_database()
        table_name = self._meta.table_name
        pk_field = self._meta.primary_key.get_db_column_name()
        
        query = f"DELETE FROM {table_name} WHERE {pk_field} = :pk"
        params = {'pk': self.pk}
        
        await db_pool.execute(query, params)
    
    async def refresh_from_db(self):
        """从数据库刷新对象数据"""
        if self.pk is None:
            raise ValueError("无法刷新没有主键的对象")
        
        refreshed = await self.__class__.objects.get(pk=self.pk)
        for field_name in self._meta.fields:
            setattr(self, field_name, getattr(refreshed, field_name))
    
    def full_clean(self):
        """完整的字段验证"""
        errors = {}
        
        for field_name, field in self._meta.fields.items():
            try:
                value = getattr(self, field_name, None)
                validated_value = field.validate(value)
                setattr(self, field_name, validated_value)
            except ValidationError as e:
                errors[field_name] = str(e)
        
        if errors:
            raise ValidationError(f"验证失败: {errors}")
    
    def _handle_auto_datetime_fields(self):
        """处理自动时间字段"""
        now = datetime.datetime.now()
        
        for field_name, field in self._meta.fields.items():
            if isinstance(field, DateTimeField):
                if field.auto_now:
                    setattr(self, field_name, now)
                elif field.auto_now_add and self._is_new:
                    setattr(self, field_name, now)
    
    async def _insert(self, db_pool: DatabasePool):
        """插入新记录"""
        table_name = self._meta.table_name
        fields = []
        placeholders = []
        params = {}
        
        for field_name, field in self._meta.fields.items():
            # 跳过自增主键
            if field.primary_key and getattr(self, field_name, None) is None:
                continue
            
            value = getattr(self, field_name, None)
            if value is not None:
                db_column = field.get_db_column_name()
                fields.append(db_column)
                placeholders.append(f":{field_name}")
                params[field_name] = field.to_db_value(value)
        
        if fields:
            query = f"INSERT INTO {table_name} ({', '.join(fields)}) VALUES ({', '.join(placeholders)})"
            
            # 对于支持RETURNING的数据库，获取插入的ID
            if self._meta.primary_key.name not in params:
                if db_pool.config.db_type == 'postgresql':
                    query += f" RETURNING {self._meta.primary_key.get_db_column_name()}"
                    result = await db_pool.fetch_one(query, params)
                    if result:
                        setattr(self, self._meta.primary_key.name, result[self._meta.primary_key.get_db_column_name()])
                else:
                    await db_pool.execute(query, params)
                    # TODO: 为MySQL和SQLite获取last_insert_id
            else:
                await db_pool.execute(query, params)
        
        self._is_new = False
    
    async def _update(self, db_pool: DatabasePool):
        """更新记录"""
        if self.pk is None:
            raise ValueError("无法更新没有主键的对象")
        
        table_name = self._meta.table_name
        set_clauses = []
        params = {}
        
        for field_name, field in self._meta.fields.items():
            if field.primary_key:
                continue
            
            value = getattr(self, field_name, None)
            if value is not None:
                db_column = field.get_db_column_name()
                set_clauses.append(f"{db_column} = :{field_name}")
                params[field_name] = field.to_db_value(value)
        
        if set_clauses:
            pk_field = self._meta.primary_key.get_db_column_name()
            params['pk'] = self.pk
            
            query = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE {pk_field} = :pk"
            await db_pool.execute(query, params)
    
    def to_dict(self, exclude_fields: List[str] = None) -> Dict[str, Any]:
        """转换为字典"""
        exclude_fields = exclude_fields or []
        result = {}
        
        for field_name in self._meta.fields:
            if field_name not in exclude_fields:
                value = getattr(self, field_name, None)
                result[field_name] = value
        
        return result
    
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.pk}>"
    
    def __str__(self):
        return f"{self.__class__.__name__} object ({self.pk})"


# 用于创建数据库表的工具函数
async def create_tables(*model_classes, db_pool: DatabasePool = None):
    """创建数据库表"""
    if not db_pool:
        db_pool = db_manager.get_database()
    
    db_type = db_pool.config.db_type
    
    for model_class in model_classes:
        if not hasattr(model_class, '_meta'):
            continue
        
        table_name = model_class._meta.table_name
        columns = []
        
        for field_name, field in model_class._meta.fields.items():
            column_def = f"{field.get_db_column_name()} {field.get_sql_type(db_type)}"
            
            if field.primary_key:
                if db_type == 'postgresql':
                    column_def += " PRIMARY KEY"
                    if isinstance(field, IntegerField):
                        column_def = column_def.replace("INTEGER", "SERIAL")
                elif db_type == 'mysql':
                    column_def += " PRIMARY KEY AUTO_INCREMENT"
                elif db_type == 'sqlite':
                    column_def += " PRIMARY KEY AUTOINCREMENT"
            
            if not field.null and not field.primary_key:
                column_def += " NOT NULL"
            
            if field.unique and not field.primary_key:
                column_def += " UNIQUE"
            
            columns.append(column_def)
        
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        
        try:
            await db_pool.execute(create_sql)
            logger.info(f"创建表: {table_name}")
        except Exception as e:
            logger.error(f"创建表 {table_name} 失败: {e}")
            raise


async def drop_tables(*model_classes, db_pool: DatabasePool = None):
    """删除数据库表"""
    if not db_pool:
        db_pool = db_manager.get_database()
    
    for model_class in model_classes:
        if not hasattr(model_class, '_meta'):
            continue
        
        table_name = model_class._meta.table_name
        drop_sql = f"DROP TABLE IF EXISTS {table_name}"
        
        try:
            await db_pool.execute(drop_sql)
            logger.info(f"删除表: {table_name}")
        except Exception as e:
            logger.error(f"删除表 {table_name} 失败: {e}")
            raise 