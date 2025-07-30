"""
AsyncFrame 自动迁移系统
在应用启动时自动检查模型变化并同步到数据库
支持增量更新，避免数据丢失
"""

import hashlib
import json
import logging
import inspect
import importlib
import importlib.util
import pkgutil
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Type
from datetime import datetime

from .models import Model
from .database import db_manager
from .migrations import migration_manager


logger = logging.getLogger(__name__)


class TableSchema:
    """数据库表结构信息"""
    
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.columns = {}  # {column_name: column_info}
        self.indexes = {}
        self.constraints = {}


class FieldComparator:
    """字段对比器"""
    
    @staticmethod
    def get_column_definition(field, db_type: str) -> str:
        """根据字段类型生成数据库列定义"""
        field_type = field.__class__.__name__
        
        # 类型映射
        if db_type == 'mysql':
            type_mapping = {
                'CharField': f"VARCHAR({getattr(field, 'max_length', 255)})",
                'TextField': "TEXT",
                'IntegerField': "INT",
                'BigIntegerField': "BIGINT", 
                'FloatField': "FLOAT",
                'BooleanField': "BOOLEAN",
                'DateTimeField': "DATETIME",
                'DateField': "DATE",
                'JSONField': "JSON"
            }
        elif db_type == 'postgresql':
            type_mapping = {
                'CharField': f"VARCHAR({getattr(field, 'max_length', 255)})",
                'TextField': "TEXT",
                'IntegerField': "INTEGER",
                'BigIntegerField': "BIGINT",
                'FloatField': "REAL", 
                'BooleanField': "BOOLEAN",
                'DateTimeField': "TIMESTAMP",
                'DateField': "DATE",
                'JSONField': "JSONB"
            }
        elif db_type == 'sqlite':
            type_mapping = {
                'CharField': "TEXT",
                'TextField': "TEXT", 
                'IntegerField': "INTEGER",
                'BigIntegerField': "INTEGER",
                'FloatField': "REAL",
                'BooleanField': "INTEGER",
                'DateTimeField': "TEXT",
                'DateField': "TEXT",
                'JSONField': "TEXT"
            }
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        
        column_type = type_mapping.get(field_type, "TEXT")
        
        # 构建完整列定义
        definition = column_type
        
        # NULL/NOT NULL
        if not getattr(field, 'null', True):
            definition += " NOT NULL"
        
        # PRIMARY KEY
        if getattr(field, 'primary_key', False):
            if db_type == 'mysql':
                definition += " AUTO_INCREMENT PRIMARY KEY"
            elif db_type == 'postgresql':
                definition = "SERIAL PRIMARY KEY"
            elif db_type == 'sqlite':
                definition += " PRIMARY KEY AUTOINCREMENT"
        
        # UNIQUE
        elif getattr(field, 'unique', False):
            definition += " UNIQUE"
        
        # DEFAULT
        default = getattr(field, 'default', None)
        if default is not None and not callable(default):
            if isinstance(default, str):
                definition += f" DEFAULT '{default}'"
            elif isinstance(default, bool):
                definition += f" DEFAULT {1 if default else 0}"
            else:
                definition += f" DEFAULT {default}"
        
        return definition
    
    @staticmethod
    def compare_columns(field_name: str, model_field, db_column_info: Dict, db_type: str) -> List[str]:
        """对比模型字段和数据库列，返回需要执行的SQL语句"""
        changes = []
        
        # 获取期望的列定义
        expected_def = FieldComparator.get_column_definition(model_field, db_type)
        
        # 比较类型
        expected_type = expected_def.split()[0]
        actual_type = db_column_info.get('Type', '').upper()
        
        # 简化类型对比（这里可以进一步优化）
        if not FieldComparator._types_compatible(expected_type, actual_type, db_type):
            # 类型不兼容，需要修改
            changes.append(f"MODIFY COLUMN {field_name} {expected_def}")
        
        # 比较NULL约束
        expected_null = getattr(model_field, 'null', True)
        actual_null = db_column_info.get('Null', 'YES') == 'YES'
        
        if expected_null != actual_null:
            null_constraint = "NULL" if expected_null else "NOT NULL"
            changes.append(f"MODIFY COLUMN {field_name} {expected_def}")
        
        return changes
    
    @staticmethod
    def _types_compatible(expected: str, actual: str, db_type: str) -> bool:
        """检查类型是否兼容"""
        # 简化的类型兼容性检查
        if db_type == 'mysql':
            type_groups = {
                'VARCHAR': ['VARCHAR', 'CHAR'],
                'TEXT': ['TEXT', 'LONGTEXT', 'MEDIUMTEXT'],
                'INT': ['INT', 'INTEGER'],
                'BIGINT': ['BIGINT'],
                'FLOAT': ['FLOAT', 'DOUBLE'],
                'BOOLEAN': ['TINYINT', 'BOOLEAN'],
                'DATETIME': ['DATETIME', 'TIMESTAMP'],
                'DATE': ['DATE'],
                'JSON': ['JSON']
            }
            
            for group_type, variants in type_groups.items():
                if expected.startswith(group_type) and any(actual.startswith(v) for v in variants):
                    return True
        
        return expected.upper() == actual.upper()


class ModelScanner:
    """模型扫描器 - 自动发现项目中的模型类"""
    
    def __init__(self, scan_paths: List[str] = None):
        self.scan_paths = scan_paths or ['models', 'app.models', 'apps']
        self._discovered_models = {}
        self._model_registry = {}
    
    def discover_models(self) -> Dict[str, Type[Model]]:
        """自动发现所有模型类"""
        models = {}
        
        # 扫描指定路径
        for path in self.scan_paths:
            try:
                models.update(self._scan_module(path))
            except ImportError:
                # 如果模块不存在就跳过
                continue
        
        # 扫描当前工作目录中的Python文件
        models.update(self._scan_directory('.'))
        
        # 更新缓存
        self._discovered_models = models
        logger.info(f"🔍 发现 {len(models)} 个模型类: {list(models.keys())}")
        
        return models
    
    def _scan_module(self, module_path: str) -> Dict[str, Type[Model]]:
        """扫描指定模块"""
        models = {}
        
        try:
            module = importlib.import_module(module_path)
            models.update(self._extract_models_from_module(module))
        except ImportError as e:
            logger.debug(f"无法导入模块 {module_path}: {e}")
        
        return models
    
    def _scan_directory(self, directory: str) -> Dict[str, Type[Model]]:
        """扫描目录中的Python文件"""
        models = {}
        
        try:
            for file_path in Path(directory).glob("**/*.py"):
                if file_path.name.startswith('.') or file_path.name.startswith('__'):
                    continue
                
                # 转换文件路径为模块路径
                module_path = str(file_path.with_suffix('')).replace('/', '.')
                
                try:
                    spec = importlib.util.spec_from_file_location(module_path, file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        models.update(self._extract_models_from_module(module))
                except Exception as e:
                    logger.debug(f"扫描文件 {file_path} 时出错: {e}")
                    continue
        
        except Exception as e:
            logger.debug(f"扫描目录 {directory} 时出错: {e}")
        
        return models
    
    def _extract_models_from_module(self, module) -> Dict[str, Type[Model]]:
        """从模块中提取模型类"""
        models = {}
        
        for name, obj in inspect.getmembers(module):
            if (inspect.isclass(obj) and 
                issubclass(obj, Model) and 
                obj is not Model and
                hasattr(obj, '_meta')):
                
                models[f"{obj.__module__}.{obj.__name__}"] = obj
        
        return models
    
    def get_models(self) -> Dict[str, Type[Model]]:
        """获取已发现的模型"""
        if not self._discovered_models:
            self.discover_models()
        return self._discovered_models


class ModelFingerprinter:
    """模型指纹生成器 - 为模型结构生成唯一标识"""
    
    @staticmethod
    def generate_model_fingerprint(model_class: Type[Model]) -> str:
        """为模型生成指纹"""
        model_info = {
            'name': model_class.__name__,
            'table_name': model_class._meta.table_name,
            'fields': {}
        }
        
        # 收集字段信息
        for field_name, field in model_class._meta.fields.items():
            field_info = {
                'type': field.__class__.__name__,
                'null': getattr(field, 'null', True),
                'unique': getattr(field, 'unique', False),
                'primary_key': getattr(field, 'primary_key', False),
                'max_length': getattr(field, 'max_length', None),
                'default': str(getattr(field, 'default', None)),
                'auto_now': getattr(field, 'auto_now', False),
                'auto_now_add': getattr(field, 'auto_now_add', False)
            }
            model_info['fields'][field_name] = field_info
        
        # 生成JSON字符串并计算MD5
        json_str = json.dumps(model_info, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()
    
    @staticmethod
    def generate_models_fingerprint(models: Dict[str, Type[Model]]) -> str:
        """为所有模型生成总体指纹"""
        all_fingerprints = {}
        
        for model_name, model_class in models.items():
            all_fingerprints[model_name] = ModelFingerprinter.generate_model_fingerprint(model_class)
        
        # 生成总体指纹
        json_str = json.dumps(all_fingerprints, sort_keys=True)
        return hashlib.md5(json_str.encode()).hexdigest()


class AutoMigrationManager:
    """自动迁移管理器 - 支持增量更新"""
    
    def __init__(self, enable_column_deletion: bool = False, enable_table_deletion: bool = False):
        self.scanner = ModelScanner()
        self.fingerprinter = ModelFingerprinter()
        self.field_comparator = FieldComparator()
        self.schema_table = "asyncframe_schema_versions"
        self._current_models = {}
        # 新增配置选项
        self.enable_column_deletion = enable_column_deletion
        self.enable_table_deletion = enable_table_deletion
    
    async def initialize(self):
        """初始化自动迁移系统"""
        await self._ensure_schema_table()
        logger.info("✅ 自动迁移系统已初始化")
    
    async def _ensure_schema_table(self):
        """确保模式版本表存在"""
        pool = db_manager.get_database()
        db_type = pool.config.db_type
        
        if db_type == 'mysql':
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.schema_table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fingerprint VARCHAR(32) NOT NULL UNIQUE,
                model_count INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
        elif db_type == 'postgresql':
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.schema_table} (
                id SERIAL PRIMARY KEY,
                fingerprint VARCHAR(32) NOT NULL UNIQUE,
                model_count INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        elif db_type == 'sqlite':
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.schema_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fingerprint VARCHAR(32) NOT NULL UNIQUE,
                model_count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        
        await pool.execute(create_sql)
    
    async def check_and_sync(self) -> bool:
        """检查模型变化并自动同步"""
        logger.info("🔍 检查模型变化...")
        
        # 发现当前模型
        current_models = self.scanner.discover_models()
        self._current_models = current_models
        
        if not current_models:
            logger.info("⚠️  未发现任何模型，跳过同步")
            return False
        
        # 生成当前模型指纹
        current_fingerprint = self.fingerprinter.generate_models_fingerprint(current_models)
        
        # 检查数据库中的最新指纹
        last_fingerprint = await self._get_last_fingerprint()
        
        if last_fingerprint == current_fingerprint:
            logger.info("✅ 模型无变化，跳过同步")
            return False
        
        # 模型有变化，需要同步
        if last_fingerprint is None:
            logger.info("🆕 首次运行，创建所有数据库表...")
            await self._create_all_tables(current_models)
        else:
            logger.info("🔄 检测到模型变化，增量同步数据库结构...")
            await self._incremental_sync(current_models)
        
        # 记录新的指纹
        await self._record_fingerprint(current_fingerprint, len(current_models))
        
        logger.info("✅ 数据库同步完成")
        return True
    
    async def _get_last_fingerprint(self) -> Optional[str]:
        """获取最后一次记录的指纹"""
        try:
            pool = db_manager.get_database()
            query = f"SELECT fingerprint FROM {self.schema_table} ORDER BY applied_at DESC LIMIT 1"
            result = await pool.fetch_one(query)
            return result['fingerprint'] if result else None
        except Exception:
            # 如果表不存在或查询失败，返回None
            return None
    
    async def _record_fingerprint(self, fingerprint: str, model_count: int):
        """记录新的指纹（如果已存在则更新）"""
        pool = db_manager.get_database()
        db_type = pool.config.db_type
        
        try:
            if db_type == 'mysql':
                # MySQL使用INSERT ... ON DUPLICATE KEY UPDATE
                query = f"""
                INSERT INTO {self.schema_table} (fingerprint, model_count, created_at, applied_at) 
                VALUES (:fingerprint, :model_count, NOW(), NOW())
                ON DUPLICATE KEY UPDATE 
                    model_count = VALUES(model_count),
                    applied_at = NOW()
                """
            elif db_type == 'postgresql':
                # PostgreSQL使用INSERT ... ON CONFLICT
                query = f"""
                INSERT INTO {self.schema_table} (fingerprint, model_count, created_at, applied_at) 
                VALUES (:fingerprint, :model_count, NOW(), NOW())
                ON CONFLICT (fingerprint) DO UPDATE SET
                    model_count = EXCLUDED.model_count,
                    applied_at = NOW()
                """
            elif db_type == 'sqlite':
                # SQLite使用INSERT OR REPLACE
                query = f"""
                INSERT OR REPLACE INTO {self.schema_table} (fingerprint, model_count, created_at, applied_at) 
                VALUES (:fingerprint, :model_count, datetime('now'), datetime('now'))
                """
            else:
                raise ValueError(f"不支持的数据库类型: {db_type}")
            
            await pool.execute(query, {
                'fingerprint': fingerprint,
                'model_count': model_count
            })
            logger.debug(f"✅ 记录指纹: {fingerprint}")
            
        except Exception as e:
            logger.error(f"❌ 记录指纹失败: {e}")
            # 如果UPSERT失败，尝试简单的UPDATE
            try:
                update_query = f"""
                UPDATE {self.schema_table} 
                SET model_count = :model_count, applied_at = CURRENT_TIMESTAMP 
                WHERE fingerprint = :fingerprint
                """
                result = await pool.execute(update_query, {
                    'fingerprint': fingerprint,
                    'model_count': model_count
                })
                logger.debug(f"✅ 更新指纹记录: {fingerprint}")
            except Exception as update_error:
                logger.error(f"❌ 更新指纹记录也失败: {update_error}")
                raise
    
    async def _create_all_tables(self, models: Dict[str, Type[Model]]):
        """创建所有数据库表"""
        from .models import create_tables
        
        model_classes = list(models.values())
        await create_tables(*model_classes)
        
        logger.info(f"🎉 成功创建 {len(model_classes)} 个数据库表")
    
    async def _incremental_sync(self, models: Dict[str, Type[Model]]):
        """增量同步数据库结构"""
        pool = db_manager.get_database()
        db_type = pool.config.db_type
        
        # 获取现有表列表
        existing_tables = await self._get_existing_tables()
        
        # 处理模型对应的表
        for model_name, model_class in models.items():
            table_name = model_class._meta.table_name
            
            if table_name not in existing_tables:
                # 新表，直接创建
                logger.info(f"📝 创建新表: {table_name}")
                await self._create_single_table(model_class)
            else:
                # 现有表，检查字段变化
                logger.info(f"🔧 检查表字段变化: {table_name}")
                await self._sync_table_columns(model_class)
        
        # 新增：检查需要删除的表（如果启用了表删除功能）
        if self.enable_table_deletion:
            await self._remove_obsolete_tables(models, existing_tables)
    
    async def _get_existing_tables(self) -> Set[str]:
        """获取数据库中现有的表"""
        pool = db_manager.get_database()
        db_type = pool.config.db_type
        
        if db_type == 'mysql':
            query = "SHOW TABLES"
        elif db_type == 'postgresql':
            query = "SELECT tablename FROM pg_tables WHERE schemaname='public'"
        elif db_type == 'sqlite':
            query = "SELECT name FROM sqlite_master WHERE type='table'"
        
        tables = await pool.fetch_all(query)
        return {list(table.values())[0] for table in tables}
    
    async def _create_single_table(self, model_class: Type[Model]):
        """创建单个表"""
        from .models import create_tables
        await create_tables(model_class)
    
    async def _sync_table_columns(self, model_class: Type[Model]):
        """同步表的列结构"""
        pool = db_manager.get_database()
        db_type = pool.config.db_type
        table_name = model_class._meta.table_name
        
        logger.info(f"🔧 开始同步表 {table_name} 的列结构")
        
        # 获取现有列信息
        existing_columns = await self._get_table_columns(table_name)
        logger.debug(f"📋 {table_name} 现有列: {list(existing_columns.keys())}")
        
        # 检查需要添加的新列
        model_fields = model_class._meta.fields
        logger.debug(f"📋 {table_name} 模型字段: {list(model_fields.keys())}")
        
        added_count = 0
        modified_count = 0
        
        for field_name, field in model_fields.items():
            if field_name not in existing_columns:
                # 添加新列
                logger.info(f"➕ 发现新字段需要添加: {table_name}.{field_name}")
                await self._add_column(table_name, field_name, field, db_type)
                added_count += 1
            else:
                # 检查列是否需要修改
                logger.debug(f"🔧 检查字段是否需要修改: {table_name}.{field_name}")
                await self._modify_column_if_needed(table_name, field_name, field, existing_columns[field_name], db_type)
        
        # 新增：检查需要删除的列（如果启用了列删除功能）
        if self.enable_column_deletion:
            await self._remove_obsolete_columns(table_name, model_fields, existing_columns, db_type)
        
        logger.info(f"✅ {table_name} 列结构同步完成 (添加: {added_count}, 修改: {modified_count})")
    
    async def _get_table_columns(self, table_name: str) -> Dict[str, Dict]:
        """获取表的列信息"""
        pool = db_manager.get_database()
        db_type = pool.config.db_type
        
        logger.debug(f"🔍 获取表 {table_name} 的列信息")
        
        if db_type == 'mysql':
            query = f"DESCRIBE {table_name}"
        elif db_type == 'postgresql':
            query = f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            """
        elif db_type == 'sqlite':
            query = f"PRAGMA table_info({table_name})"
        
        columns = await pool.fetch_all(query)
        logger.debug(f"📊 查询到 {len(columns)} 列信息")
        
        # 转换为统一格式
        column_info = {}
        for col in columns:
            if db_type == 'mysql':
                column_info[col['Field']] = {
                    'Type': col['Type'],
                    'Null': col['Null'],
                    'Key': col['Key'],
                    'Default': col['Default']
                }
            elif db_type == 'postgresql':
                column_info[col['column_name']] = {
                    'Type': col['data_type'],
                    'Null': 'YES' if col['is_nullable'] == 'YES' else 'NO',
                    'Default': col['column_default']
                }
            elif db_type == 'sqlite':
                column_info[col['name']] = {
                    'Type': col['type'],
                    'Null': 'YES' if col['notnull'] == 0 else 'NO',
                    'Default': col['dflt_value']
                }
        
        logger.debug(f"📋 解析后的列信息: {list(column_info.keys())}")
        return column_info
    
    async def _add_column(self, table_name: str, field_name: str, field, db_type: str):
        """添加新列"""
        pool = db_manager.get_database()
        
        logger.info(f"➕ 开始添加列: {table_name}.{field_name}")
        logger.debug(f"   字段类型: {field.__class__.__name__}")
        logger.debug(f"   字段属性: null={getattr(field, 'null', True)}, max_length={getattr(field, 'max_length', None)}")
        
        try:
            column_def = self.field_comparator.get_column_definition(field, db_type)
            logger.debug(f"   生成的列定义: {column_def}")
            
            sql = f"ALTER TABLE {table_name} ADD COLUMN {field_name} {column_def}"
            logger.debug(f"   执行SQL: {sql}")
            
            await pool.execute(sql)
            logger.info(f"✅ 成功添加列: {table_name}.{field_name}")
            
        except Exception as e:
            logger.error(f"❌ 添加列失败: {table_name}.{field_name}, 错误: {e}")
            logger.error(f"   SQL: ALTER TABLE {table_name} ADD COLUMN {field_name} {column_def if 'column_def' in locals() else 'N/A'}")
            raise
    
    async def _modify_column_if_needed(self, table_name: str, field_name: str, field, existing_column: Dict, db_type: str):
        """如果需要则修改列"""
        changes = self.field_comparator.compare_columns(field_name, field, existing_column, db_type)
        
        if changes:
            pool = db_manager.get_database()
            
            for change in changes:
                if db_type == 'mysql':
                    sql = f"ALTER TABLE {table_name} {change}"
                elif db_type == 'postgresql':
                    # PostgreSQL需要特殊处理
                    sql = self._generate_postgresql_alter(table_name, field_name, field)
                elif db_type == 'sqlite':
                    # SQLite不支持修改列，需要重建表
                    logger.warning(f"⚠️  SQLite不支持修改列: {table_name}.{field_name}")
                    continue
                
                try:
                    await pool.execute(sql)
                    logger.info(f"✅ 修改列: {table_name}.{field_name}")
                except Exception as e:
                    logger.error(f"❌ 修改列失败: {table_name}.{field_name}, 错误: {e}")
    
    def _generate_postgresql_alter(self, table_name: str, field_name: str, field) -> str:
        """生成PostgreSQL的ALTER语句"""
        # PostgreSQL的ALTER语法比较复杂，这里简化处理
        column_def = self.field_comparator.get_column_definition(field, 'postgresql')
        type_part = column_def.split()[0]
        return f"ALTER TABLE {table_name} ALTER COLUMN {field_name} TYPE {type_part}"
    
    async def force_sync(self):
        """强制同步所有模型到数据库"""
        logger.info("🔧 强制同步所有模型...")
        
        current_models = self.scanner.discover_models()
        if not current_models:
            logger.warning("⚠️  未发现任何模型")
            return
        
        await self._create_all_tables(current_models)
        
        # 更新指纹
        current_fingerprint = self.fingerprinter.generate_models_fingerprint(current_models)
        await self._record_fingerprint(current_fingerprint, len(current_models))
        
        logger.info("✅ 强制同步完成")
    
    async def _remove_obsolete_columns(self, table_name: str, model_fields: Dict, existing_columns: Dict, db_type: str):
        """删除模型中不存在的列"""
        pool = db_manager.get_database()
        
        # 找出数据库中存在但模型中不存在的列
        obsolete_columns = []
        for column_name in existing_columns.keys():
            if column_name not in model_fields and column_name != 'id':  # 保留主键列
                obsolete_columns.append(column_name)
        
        for column_name in obsolete_columns:
            if db_type == 'mysql':
                sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            elif db_type == 'postgresql':
                sql = f"ALTER TABLE {table_name} DROP COLUMN {column_name}"
            elif db_type == 'sqlite':
                # SQLite不支持直接删除列，需要重建表
                logger.warning(f"⚠️  SQLite不支持删除列: {table_name}.{column_name}")
                logger.warning("💡 建议手动处理SQLite列删除")
                continue
            
            try:
                logger.info(f"🗑️  删除列: {table_name}.{column_name}")
                await pool.execute(sql)
                logger.info(f"✅ 成功删除列: {table_name}.{column_name}")
            except Exception as e:
                logger.error(f"❌ 删除列失败: {table_name}.{column_name}, 错误: {e}")

    async def _remove_obsolete_tables(self, models: Dict[str, Type[Model]], existing_tables: Set[str]):
        """删除模型中不存在的表"""
        pool = db_manager.get_database()
        
        # 获取所有模型对应的表名
        model_tables = {model_class._meta.table_name for model_class in models.values()}
        
        # 系统表，不应删除
        system_tables = {self.schema_table, 'information_schema', 'performance_schema', 'mysql', 'sys'}
        
        # 找出数据库中存在但模型中不存在的表
        obsolete_tables = []
        for table_name in existing_tables:
            if (table_name not in model_tables and 
                table_name not in system_tables and 
                not table_name.startswith('__')):
                obsolete_tables.append(table_name)
        
        for table_name in obsolete_tables:
            try:
                logger.info(f"🗑️  删除表: {table_name}")
                await pool.execute(f"DROP TABLE {table_name}")
                logger.info(f"✅ 成功删除表: {table_name}")
            except Exception as e:
                logger.error(f"❌ 删除表失败: {table_name}, 错误: {e}")

    async def get_status(self) -> Dict[str, Any]:
        """获取自动迁移状态"""
        current_models = self.scanner.discover_models()
        current_fingerprint = self.fingerprinter.generate_models_fingerprint(current_models)
        last_fingerprint = await self._get_last_fingerprint()
        
        # 获取现有表信息
        existing_tables = await self._get_existing_tables()
        model_tables = {model_class._meta.table_name for model_class in current_models.values()}
        
        return {
            'current_models_count': len(current_models),
            'current_fingerprint': current_fingerprint,
            'last_fingerprint': last_fingerprint,
            'needs_sync': last_fingerprint != current_fingerprint,
            'is_first_run': last_fingerprint is None,
            'discovered_models': list(current_models.keys()),
            'existing_tables': list(existing_tables),
            'model_tables': list(model_tables),
            'enable_column_deletion': self.enable_column_deletion,
            'enable_table_deletion': self.enable_table_deletion
        }


# 全局自动迁移管理器
auto_migration_manager = AutoMigrationManager()


async def auto_migrate_on_startup():
    """应用启动时自动检查和迁移"""
    try:
        await auto_migration_manager.initialize()
        await auto_migration_manager.check_and_sync()
    except Exception as e:
        logger.error(f"❌ 自动迁移失败: {e}")
        raise


def enable_auto_migration(app, enable_column_deletion: bool = False, enable_table_deletion: bool = False):
    """为应用启用自动迁移
    
    Args:
        app: AsyncFrame应用实例
        enable_column_deletion: 是否启用列删除功能（默认False，避免数据丢失）
        enable_table_deletion: 是否启用表删除功能（默认False，避免数据丢失）
    """
    global auto_migration_manager
    
    # 重新创建管理器实例以应用新配置
    auto_migration_manager = AutoMigrationManager(
        enable_column_deletion=enable_column_deletion,
        enable_table_deletion=enable_table_deletion
    )
    
    # 创建带配置的启动函数
    async def startup_auto_migrate_with_config():
        """带配置的自动迁移启动函数"""
        try:
            # 使用当前配置的管理器实例
            logger.info(f"🔧 开始自动迁移 (列删除: {enable_column_deletion}, 表删除: {enable_table_deletion})")
            await auto_migration_manager.initialize()
            await auto_migration_manager.check_and_sync()
        except Exception as e:
            logger.error(f"❌ 自动迁移失败: {e}")
            raise
    
    # 注册启动回调
    app.on_startup(startup_auto_migrate_with_config)
    
    deletion_status = []
    if enable_column_deletion:
        deletion_status.append("列删除")
    if enable_table_deletion:
        deletion_status.append("表删除")
    
    if deletion_status:
        logger.info(f"🔧 已启用自动迁移功能 (包含: {', '.join(deletion_status)})")
        logger.warning("⚠️  启用删除功能可能导致数据丢失，请谨慎使用")
    else:
        logger.info("🔧 已启用自动迁移功能 (安全模式: 不删除表/列)") 