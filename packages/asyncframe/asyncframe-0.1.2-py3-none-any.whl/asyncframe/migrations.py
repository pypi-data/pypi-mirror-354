"""
AsyncFrame 数据库迁移系统
支持数据库结构版本管理、迁移执行和回滚
"""

import os
import json
import time
import asyncio
import importlib.util
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any
from .database import db_manager


class Migration:
    """迁移文件基类"""
    
    def __init__(self, name: str, timestamp: str):
        self.name = name
        self.timestamp = timestamp
        self.version = f"{timestamp}_{name}"
    
    async def up(self):
        """向上迁移（应用更改）"""
        raise NotImplementedError("必须实现 up 方法")
    
    async def down(self):
        """向下迁移（回滚更改）"""
        raise NotImplementedError("必须实现 down 方法")


class MigrationManager:
    """迁移管理器"""
    
    def __init__(self, migrations_dir: str = "script/migrations"):
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(parents=True, exist_ok=True)
        self.migration_table = "asyncframe_migrations"
    
    async def init_migration_table(self):
        """初始化迁移表"""
        pool = db_manager.get_database()
        db_type = pool.config.db_type
        
        if db_type == 'sqlite':
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.migration_table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        elif db_type == 'mysql':
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.migration_table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                version VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        elif db_type == 'postgresql':
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS {self.migration_table} (
                id SERIAL PRIMARY KEY,
                version VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255) NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
        
        await pool.execute(create_sql)
        print(f"✅ 迁移表 {self.migration_table} 已初始化")
    
    def create_migration(self, name: str, content: str = None) -> str:
        """创建新的迁移文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version = f"{timestamp}_{name}"
        filename = f"{version}.py"
        filepath = self.migrations_dir / filename
        
        if content is None:
            content = self._get_migration_template(name, timestamp)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 创建迁移文件: {filename}")
        return str(filepath)
    
    def _get_migration_template(self, name: str, timestamp: str) -> str:
        """获取迁移文件模板"""
        return f'''"""
迁移: {name}
创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
版本: {timestamp}_{name}
"""

from asyncframe.migrations import Migration
from asyncframe.database import db_manager


class {self._to_class_name(name)}Migration(Migration):
    """
    {name} 迁移
    
    描述你的迁移内容...
    """
    
    def __init__(self):
        super().__init__("{name}", "{timestamp}")
    
    async def up(self):
        """向上迁移 - 应用更改"""
        pool = db_manager.get_database()
        
        # 示例: 创建表
        # await pool.execute("""
        #     CREATE TABLE example_table (
        #         id INTEGER PRIMARY KEY,
        #         name VARCHAR(100) NOT NULL,
        #         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        #     )
        # """)
        
        # 示例: 添加列
        # await pool.execute("ALTER TABLE users ADD COLUMN phone VARCHAR(20)")
        
        # 示例: 创建索引
        # await pool.execute("CREATE INDEX idx_users_email ON users(email)")
        
        print(f"✅ 应用迁移: {{self.version}}")
    
    async def down(self):
        """向下迁移 - 回滚更改"""
        pool = db_manager.get_database()
        
        # 示例: 删除表
        # await pool.execute("DROP TABLE IF EXISTS example_table")
        
        # 示例: 删除列
        # await pool.execute("ALTER TABLE users DROP COLUMN phone")
        
        # 示例: 删除索引
        # await pool.execute("DROP INDEX IF EXISTS idx_users_email")
        
        print(f"✅ 回滚迁移: {{self.version}}")


# 导出迁移实例
migration = {self._to_class_name(name)}Migration()
'''
    
    def _to_class_name(self, name: str) -> str:
        """将迁移名称转换为类名"""
        return ''.join(word.capitalize() for word in name.split('_'))
    
    async def get_applied_migrations(self) -> List[str]:
        """获取已应用的迁移列表"""
        try:
            pool = db_manager.get_database()
            query = f"SELECT version FROM {self.migration_table} ORDER BY applied_at"
            results = await pool.fetch_all(query)
            return [row['version'] for row in results]
        except Exception:
            # 如果表不存在，返回空列表
            return []
    
    async def get_pending_migrations(self) -> List[str]:
        """获取待应用的迁移列表"""
        applied = await self.get_applied_migrations()
        all_migrations = self.get_migration_files()
        return [m for m in all_migrations if m not in applied]
    
    def get_migration_files(self) -> List[str]:
        """获取所有迁移文件列表"""
        if not self.migrations_dir.exists():
            return []
        
        migrations = []
        for file in self.migrations_dir.glob("*.py"):
            if file.name != "__init__.py":
                migrations.append(file.stem)
        
        return sorted(migrations)
    
    async def load_migration(self, version: str) -> Migration:
        """加载迁移文件"""
        filepath = self.migrations_dir / f"{version}.py"
        if not filepath.exists():
            raise FileNotFoundError(f"迁移文件不存在: {filepath}")
        
        spec = importlib.util.spec_from_file_location(version, filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        return module.migration
    
    async def apply_migration(self, version: str):
        """应用单个迁移"""
        migration = await self.load_migration(version)
        
        try:
            await migration.up()
            
            # 记录迁移
            pool = db_manager.get_database()
            await pool.execute(
                f"INSERT INTO {self.migration_table} (version, name) VALUES (:version, :name)",
                {"version": version, "name": migration.name}
            )
            
            print(f"✅ 迁移已应用: {version}")
        except Exception as e:
            print(f"❌ 迁移应用失败: {version}, 错误: {e}")
            raise
    
    async def rollback_migration(self, version: str):
        """回滚单个迁移"""
        migration = await self.load_migration(version)
        
        try:
            await migration.down()
            
            # 删除迁移记录
            pool = db_manager.get_database()
            await pool.execute(
                f"DELETE FROM {self.migration_table} WHERE version = :version",
                {"version": version}
            )
            
            print(f"✅ 迁移已回滚: {version}")
        except Exception as e:
            print(f"❌ 迁移回滚失败: {version}, 错误: {e}")
            raise
    
    async def migrate(self, target: Optional[str] = None):
        """执行迁移到指定版本（默认为最新）"""
        await self.init_migration_table()
        
        pending = await self.get_pending_migrations()
        if not pending:
            print("✅ 所有迁移都已应用")
            return
        
        if target:
            # 迁移到指定版本
            if target not in pending:
                print(f"⚠️  迁移 {target} 已应用或不存在")
                return
            
            to_apply = [m for m in pending if m <= target]
        else:
            # 迁移到最新版本
            to_apply = pending
        
        print(f"📋 准备应用 {len(to_apply)} 个迁移:")
        for migration in to_apply:
            print(f"   - {migration}")
        
        for migration in to_apply:
            await self.apply_migration(migration)
        
        print(f"✅ 迁移完成! 共应用 {len(to_apply)} 个迁移")
    
    async def rollback(self, target: Optional[str] = None, steps: int = 1):
        """回滚迁移"""
        await self.init_migration_table()
        
        applied = await self.get_applied_migrations()
        if not applied:
            print("⚠️  没有可回滚的迁移")
            return
        
        if target:
            # 回滚到指定版本
            to_rollback = [m for m in reversed(applied) if m > target]
        else:
            # 回滚指定步数
            to_rollback = list(reversed(applied))[:steps]
        
        if not to_rollback:
            print("⚠️  没有需要回滚的迁移")
            return
        
        print(f"📋 准备回滚 {len(to_rollback)} 个迁移:")
        for migration in to_rollback:
            print(f"   - {migration}")
        
        for migration in to_rollback:
            await self.rollback_migration(migration)
        
        print(f"✅ 回滚完成! 共回滚 {len(to_rollback)} 个迁移")
    
    async def status(self):
        """显示迁移状态"""
        await self.init_migration_table()
        
        all_migrations = self.get_migration_files()
        applied = await self.get_applied_migrations()
        pending = await self.get_pending_migrations()
        
        print("📊 迁移状态:")
        print(f"   总计: {len(all_migrations)} 个迁移")
        print(f"   已应用: {len(applied)} 个")
        print(f"   待应用: {len(pending)} 个")
        
        if pending:
            print("\n⏳ 待应用的迁移:")
            for migration in pending:
                print(f"   - {migration}")
        
        if applied:
            print("\n✅ 已应用的迁移:")
            for migration in applied[-5:]:  # 显示最近5个
                print(f"   - {migration}")
            
            if len(applied) > 5:
                print(f"   ... 以及其他 {len(applied) - 5} 个")
    
    def create_model_migration(self, models: List[Any]) -> str:
        """根据模型创建迁移文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name = "create_initial_tables"
        
        content = self._generate_model_migration_content(models, name, timestamp)
        return self.create_migration(name, content)
    
    def _generate_model_migration_content(self, models: List[Any], name: str, timestamp: str) -> str:
        """生成模型迁移文件内容"""
        imports = "from asyncframe.migrations import Migration\nfrom asyncframe.database import db_manager\n"
        
        # 添加模型导入
        model_names = [model.__name__ for model in models]
        imports += f"from asyncframe.models import {', '.join(model_names)}\n"
        
        content = f'''"""
迁移: {name}
创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
版本: {timestamp}_{name}
"""

{imports}


class {self._to_class_name(name)}Migration(Migration):
    """
    创建初始数据表
    
    根据模型定义创建数据库表
    """
    
    def __init__(self):
        super().__init__("{name}", "{timestamp}")
    
    async def up(self):
        """向上迁移 - 创建表"""
        from asyncframe.database import create_tables
        
        # 创建所有模型表
        await create_tables({', '.join(model_names)})
        print(f"✅ 应用迁移: {{self.version}} - 创建了 {len(models)} 个表")
    
    async def down(self):
        """向下迁移 - 删除表"""
        from asyncframe.database import drop_tables
        
        # 删除所有模型表
        await drop_tables({', '.join(model_names)})
        print(f"✅ 回滚迁移: {{self.version}} - 删除了 {len(models)} 个表")


# 导出迁移实例
migration = {self._to_class_name(name)}Migration()
'''
        return content


# 默认迁移管理器实例
migration_manager = MigrationManager() 