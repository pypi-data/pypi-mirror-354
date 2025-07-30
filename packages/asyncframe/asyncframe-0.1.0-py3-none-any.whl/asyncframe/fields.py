"""
模型字段定义 - 用于定义模型属性
"""

import datetime
from typing import Any, Optional, Union, List, Dict, Callable
from decimal import Decimal


class ValidationError(Exception):
    """字段验证错误"""
    pass


class Field:
    """基础字段类"""
    
    def __init__(
        self,
        primary_key: bool = False,
        unique: bool = False,
        null: bool = True,
        blank: bool = True,
        default: Any = None,
        validators: List[Callable] = None,
        help_text: str = "",
        db_column: Optional[str] = None,
        db_index: bool = False,
        **kwargs
    ):
        self.primary_key = primary_key
        self.unique = unique
        self.null = null
        self.blank = blank
        self.default = default
        self.validators = validators or []
        self.help_text = help_text
        self.db_column = db_column
        self.db_index = db_index
        self.extra_kwargs = kwargs
        
        # 字段名称（由模型元类设置）
        self.name = None
        self.model_class = None
        
    def validate(self, value: Any) -> Any:
        """验证字段值"""
        # 检查空值
        if value is None:
            if not self.null:
                raise ValidationError(f"字段 '{self.name}' 不允许为空")
            return None
        
        # 检查空白值
        if value == "" and not self.blank:
            raise ValidationError(f"字段 '{self.name}' 不允许为空白")
        
        # 类型转换和验证
        value = self.to_python(value)
        
        # 运行自定义验证器
        for validator in self.validators:
            validator(value)
        
        return value
    
    def to_python(self, value: Any) -> Any:
        """将值转换为Python类型"""
        return value
    
    def to_db_value(self, value: Any) -> Any:
        """将值转换为数据库类型"""
        return value
    
    def get_db_column_name(self) -> str:
        """获取数据库列名"""
        return self.db_column or self.name
    
    def get_sql_type(self, db_type: str) -> str:
        """获取SQL类型定义"""
        raise NotImplementedError("子类必须实现 get_sql_type 方法")


class CharField(Field):
    """字符串字段"""
    
    def __init__(self, max_length: int = 255, min_length: int = 0, **kwargs):
        self.max_length = max_length
        self.min_length = min_length
        super().__init__(**kwargs)
    
    def to_python(self, value: Any) -> str:
        if value is None:
            return None
        
        value = str(value)
        
        # 长度验证
        if len(value) > self.max_length:
            raise ValidationError(f"字段 '{self.name}' 长度不能超过 {self.max_length} 个字符")
        
        if len(value) < self.min_length:
            raise ValidationError(f"字段 '{self.name}' 长度不能少于 {self.min_length} 个字符")
        
        return value
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return f"VARCHAR({self.max_length})"
        elif db_type == 'mysql':
            return f"VARCHAR({self.max_length})"
        elif db_type == 'sqlite':
            return "TEXT"
        else:
            return f"VARCHAR({self.max_length})"


class TextField(Field):
    """长文本字段"""
    
    def to_python(self, value: Any) -> str:
        if value is None:
            return None
        return str(value)
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "TEXT"
        elif db_type == 'mysql':
            return "LONGTEXT"
        elif db_type == 'sqlite':
            return "TEXT"
        else:
            return "TEXT"


class IntegerField(Field):
    """整数字段"""
    
    def __init__(self, min_value: Optional[int] = None, max_value: Optional[int] = None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(**kwargs)
    
    def to_python(self, value: Any) -> int:
        if value is None:
            return None
        
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValidationError(f"字段 '{self.name}' 必须是整数")
        
        # 范围验证
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"字段 '{self.name}' 不能小于 {self.min_value}")
        
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"字段 '{self.name}' 不能大于 {self.max_value}")
        
        return value
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "INTEGER"
        elif db_type == 'mysql':
            return "INT"
        elif db_type == 'sqlite':
            return "INTEGER"
        else:
            return "INTEGER"


class BigIntegerField(IntegerField):
    """大整数字段"""
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "BIGINT"
        elif db_type == 'mysql':
            return "BIGINT"
        elif db_type == 'sqlite':
            return "INTEGER"
        else:
            return "BIGINT"


class FloatField(Field):
    """浮点数字段"""
    
    def __init__(self, min_value: Optional[float] = None, max_value: Optional[float] = None, **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(**kwargs)
    
    def to_python(self, value: Any) -> float:
        if value is None:
            return None
        
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"字段 '{self.name}' 必须是浮点数")
        
        # 范围验证
        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"字段 '{self.name}' 不能小于 {self.min_value}")
        
        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"字段 '{self.name}' 不能大于 {self.max_value}")
        
        return value
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "REAL"
        elif db_type == 'mysql':
            return "FLOAT"
        elif db_type == 'sqlite':
            return "REAL"
        else:
            return "FLOAT"


class DecimalField(Field):
    """精确小数字段"""
    
    def __init__(self, max_digits: int = 10, decimal_places: int = 2, **kwargs):
        self.max_digits = max_digits
        self.decimal_places = decimal_places
        super().__init__(**kwargs)
    
    def to_python(self, value: Any) -> Decimal:
        if value is None:
            return None
        
        if isinstance(value, Decimal):
            return value
        
        try:
            return Decimal(str(value))
        except:
            raise ValidationError(f"字段 '{self.name}' 必须是有效的十进制数")
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return f"DECIMAL({self.max_digits}, {self.decimal_places})"
        elif db_type == 'mysql':
            return f"DECIMAL({self.max_digits}, {self.decimal_places})"
        elif db_type == 'sqlite':
            return "REAL"
        else:
            return f"DECIMAL({self.max_digits}, {self.decimal_places})"


class BooleanField(Field):
    """布尔字段"""
    
    def to_python(self, value: Any) -> bool:
        if value is None:
            return None
        
        if isinstance(value, bool):
            return value
        
        if isinstance(value, str):
            if value.lower() in ('true', '1', 'yes', 'on'):
                return True
            elif value.lower() in ('false', '0', 'no', 'off'):
                return False
            else:
                raise ValidationError(f"字段 '{self.name}' 无法转换为布尔值")
        
        return bool(value)
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "BOOLEAN"
        elif db_type == 'mysql':
            return "TINYINT(1)"
        elif db_type == 'sqlite':
            return "INTEGER"
        else:
            return "BOOLEAN"


class DateTimeField(Field):
    """日期时间字段"""
    
    def __init__(self, auto_now: bool = False, auto_now_add: bool = False, **kwargs):
        self.auto_now = auto_now
        self.auto_now_add = auto_now_add
        super().__init__(**kwargs)
    
    def to_python(self, value: Any) -> datetime.datetime:
        if value is None:
            return None
        
        if isinstance(value, datetime.datetime):
            return value
        
        if isinstance(value, str):
            try:
                # 尝试多种日期格式
                formats = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d %H:%M:%S.%f",
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%dT%H:%M:%S.%f",
                    "%Y-%m-%d",
                ]
                
                for fmt in formats:
                    try:
                        return datetime.datetime.strptime(value, fmt)
                    except ValueError:
                        continue
                
                raise ValueError("无法解析日期格式")
                
            except ValueError:
                raise ValidationError(f"字段 '{self.name}' 必须是有效的日期时间格式")
        
        raise ValidationError(f"字段 '{self.name}' 必须是日期时间类型")
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "TIMESTAMP"
        elif db_type == 'mysql':
            return "DATETIME"
        elif db_type == 'sqlite':
            return "DATETIME"
        else:
            return "TIMESTAMP"


class DateField(Field):
    """日期字段"""
    
    def to_python(self, value: Any) -> datetime.date:
        if value is None:
            return None
        
        if isinstance(value, datetime.date):
            return value
        
        if isinstance(value, datetime.datetime):
            return value.date()
        
        if isinstance(value, str):
            try:
                return datetime.datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError(f"字段 '{self.name}' 必须是有效的日期格式 (YYYY-MM-DD)")
        
        raise ValidationError(f"字段 '{self.name}' 必须是日期类型")
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "DATE"
        elif db_type == 'mysql':
            return "DATE"
        elif db_type == 'sqlite':
            return "DATE"
        else:
            return "DATE"


class JSONField(Field):
    """JSON字段"""
    
    def to_python(self, value: Any) -> Union[Dict, List]:
        if value is None:
            return None
        
        if isinstance(value, (dict, list)):
            return value
        
        if isinstance(value, str):
            try:
                import json
                return json.loads(value)
            except json.JSONDecodeError:
                raise ValidationError(f"字段 '{self.name}' 必须是有效的JSON格式")
        
        raise ValidationError(f"字段 '{self.name}' 必须是JSON类型")
    
    def to_db_value(self, value: Any) -> str:
        if value is None:
            return None
        
        import json
        return json.dumps(value, ensure_ascii=False)
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "JSONB"
        elif db_type == 'mysql':
            return "JSON"
        elif db_type == 'sqlite':
            return "TEXT"
        else:
            return "TEXT"


class ForeignKeyField(Field):
    """外键字段"""
    
    def __init__(self, to_model: str, on_delete: str = "CASCADE", related_name: Optional[str] = None, **kwargs):
        self.to_model = to_model
        self.on_delete = on_delete  # CASCADE, SET_NULL, RESTRICT等
        self.related_name = related_name
        super().__init__(**kwargs)
    
    def to_python(self, value: Any) -> int:
        if value is None:
            return None
        
        try:
            return int(value)
        except (TypeError, ValueError):
            raise ValidationError(f"外键字段 '{self.name}' 必须是整数")
    
    def get_sql_type(self, db_type: str) -> str:
        if db_type == 'postgresql':
            return "INTEGER REFERENCES {table_name}(id) ON DELETE {on_delete}".format(
                table_name=self.to_model.lower(),
                on_delete=self.on_delete
            )
        elif db_type == 'mysql':
            return "INTEGER"
        elif db_type == 'sqlite':
            return "INTEGER"
        else:
            return "INTEGER"


# 字段验证器
def min_length_validator(min_length: int):
    """最小长度验证器"""
    def validator(value):
        if len(str(value)) < min_length:
            raise ValidationError(f"值的长度不能少于 {min_length} 个字符")
    return validator


def max_length_validator(max_length: int):
    """最大长度验证器"""
    def validator(value):
        if len(str(value)) > max_length:
            raise ValidationError(f"值的长度不能超过 {max_length} 个字符")
    return validator


def email_validator(value):
    """邮箱验证器"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, str(value)):
        raise ValidationError("请输入有效的邮箱地址")


def url_validator(value):
    """URL验证器"""
    import re
    pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$'
    if not re.match(pattern, str(value)):
        raise ValidationError("请输入有效的URL地址") 