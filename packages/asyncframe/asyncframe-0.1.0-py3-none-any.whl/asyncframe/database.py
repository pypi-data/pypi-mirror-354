"""
异步数据库连接池 - 支持PostgreSQL、MySQL、SQLite
"""

import asyncio
import logging
from typing import Dict, Any, Optional, Union, List
from contextlib import asynccontextmanager
from urllib.parse import urlparse

try:
    import asyncpg
    HAS_ASYNCPG = True
except ImportError:
    HAS_ASYNCPG = False

try:
    import aiomysql
    HAS_AIOMYSQL = True
except ImportError:
    HAS_AIOMYSQL = False

try:
    import aiosqlite
    HAS_AIOSQLITE = True
except ImportError:
    HAS_AIOSQLITE = False

try:
    from databases import Database
    HAS_DATABASES = True
except ImportError:
    HAS_DATABASES = False


logger = logging.getLogger(__name__)


class DatabaseConfig:
    """数据库配置类"""
    
    def __init__(
        self,
        url: str,
        min_size: int = 1,
        max_size: int = 10,
        pool_timeout: float = 30.0,
        query_timeout: float = 30.0,
        **kwargs
    ):
        self.url = url
        self.min_size = min_size
        self.max_size = max_size
        self.pool_timeout = pool_timeout
        self.query_timeout = query_timeout
        self.extra_config = kwargs
        
        # 解析数据库URL
        parsed = urlparse(url)
        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.port = parsed.port
        self.database = parsed.path.lstrip('/')
        self.username = parsed.username
        self.password = parsed.password
        
    @property
    def db_type(self) -> str:
        """获取数据库类型"""
        if self.scheme.startswith('postgresql'):
            return 'postgresql'
        elif self.scheme.startswith('mysql'):
            return 'mysql'
        elif self.scheme.startswith('sqlite'):
            return 'sqlite'
        else:
            raise ValueError(f"不支持的数据库类型: {self.scheme}")


class DatabasePool:
    """异步数据库连接池"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.pool = None
        self._database = None
        self._is_connected = False
        
    async def connect(self):
        """连接数据库"""
        if self._is_connected:
            return
            
        try:
            if HAS_DATABASES:
                # 使用databases库（推荐）
                self._database = Database(self.config.url)
                await self._database.connect()
                logger.info(f"数据库连接成功: {self.config.db_type}")
            else:
                # 直接使用原生驱动
                await self._connect_native()
                
            self._is_connected = True
            
        except Exception as e:
            logger.error(f"数据库连接失败: {e}")
            raise
    
    async def _connect_native(self):
        """使用原生驱动连接"""
        db_type = self.config.db_type
        
        if db_type == 'postgresql':
            if not HAS_ASYNCPG:
                raise ImportError("需要安装 asyncpg: pip install asyncpg")
            
            self.pool = await asyncpg.create_pool(
                host=self.config.host,
                port=self.config.port or 5432,
                user=self.config.username,
                password=self.config.password,
                database=self.config.database,
                min_size=self.config.min_size,
                max_size=self.config.max_size,
                command_timeout=self.config.query_timeout
            )
            
        elif db_type == 'mysql':
            if not HAS_AIOMYSQL:
                raise ImportError("需要安装 aiomysql: pip install aiomysql")
                
            self.pool = await aiomysql.create_pool(
                host=self.config.host,
                port=self.config.port or 3306,
                user=self.config.username,
                password=self.config.password,
                db=self.config.database,
                minsize=self.config.min_size,
                maxsize=self.config.max_size,
                autocommit=True
            )
            
        elif db_type == 'sqlite':
            if not HAS_AIOSQLITE:
                raise ImportError("需要安装 aiosqlite: pip install aiosqlite")
            # SQLite不需要连接池，但我们仍然记录配置
            pass
            
        else:
            raise ValueError(f"不支持的数据库类型: {db_type}")
    
    async def disconnect(self):
        """断开数据库连接"""
        if not self._is_connected:
            return
            
        try:
            if self._database:
                await self._database.disconnect()
            elif self.pool:
                if self.config.db_type == 'postgresql':
                    await self.pool.close()
                elif self.config.db_type == 'mysql':
                    self.pool.close()
                    await self.pool.wait_closed()
                    
            self._is_connected = False
            logger.info("数据库连接已断开")
            
        except Exception as e:
            logger.error(f"断开数据库连接时出错: {e}")
    
    @asynccontextmanager
    async def get_connection(self):
        """获取数据库连接"""
        if not self._is_connected:
            await self.connect()
            
        if self._database:
            # 使用databases库
            yield self._database
        elif self.pool:
            # 使用原生驱动
            if self.config.db_type == 'postgresql':
                async with self.pool.acquire() as conn:
                    yield conn
            elif self.config.db_type == 'mysql':
                async with self.pool.acquire() as conn:
                    yield conn
        elif self.config.db_type == 'sqlite':
            # SQLite连接
            async with aiosqlite.connect(self.config.database) as conn:
                yield conn
        else:
            raise RuntimeError("无效的数据库连接状态")
    
    async def execute(self, query: str, values: Dict[str, Any] = None) -> Any:
        """执行SQL查询"""
        async with self.get_connection() as conn:
            if self._database:
                return await conn.execute(query, values or {})
            else:
                return await self._execute_native(conn, query, values)
    
    async def fetch_all(self, query: str, values: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """查询多条记录"""
        async with self.get_connection() as conn:
            if self._database:
                rows = await conn.fetch_all(query, values or {})
                return [dict(row) for row in rows]
            else:
                return await self._fetch_all_native(conn, query, values)
    
    async def fetch_one(self, query: str, values: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """查询单条记录"""
        async with self.get_connection() as conn:
            if self._database:
                row = await conn.fetch_one(query, values or {})
                return dict(row) if row else None
            else:
                return await self._fetch_one_native(conn, query, values)
    
    async def _execute_native(self, conn, query: str, values: Dict[str, Any] = None):
        """使用原生驱动执行查询"""
        if self.config.db_type == 'postgresql':
            if values:
                # 转换命名参数为位置参数
                query, args = self._convert_named_params_pg(query, values)
                return await conn.execute(query, *args)
            else:
                return await conn.execute(query)
                
        elif self.config.db_type == 'mysql':
            async with conn.cursor() as cursor:
                await cursor.execute(query, values or {})
                return cursor.rowcount
                
        elif self.config.db_type == 'sqlite':
            if values:
                return await conn.execute(query, values)
            else:
                return await conn.execute(query)
    
    async def _fetch_all_native(self, conn, query: str, values: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """使用原生驱动查询多条记录"""
        if self.config.db_type == 'postgresql':
            if values:
                query, args = self._convert_named_params_pg(query, values)
                rows = await conn.fetch(query, *args)
            else:
                rows = await conn.fetch(query)
            return [dict(row) for row in rows]
            
        elif self.config.db_type == 'mysql':
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values or {})
                rows = await cursor.fetchall()
                return list(rows)
                
        elif self.config.db_type == 'sqlite':
            conn.row_factory = aiosqlite.Row
            if values:
                cursor = await conn.execute(query, values)
            else:
                cursor = await conn.execute(query)
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]
    
    async def _fetch_one_native(self, conn, query: str, values: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """使用原生驱动查询单条记录"""
        if self.config.db_type == 'postgresql':
            if values:
                query, args = self._convert_named_params_pg(query, values)
                row = await conn.fetchrow(query, *args)
            else:
                row = await conn.fetchrow(query)
            return dict(row) if row else None
            
        elif self.config.db_type == 'mysql':
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(query, values or {})
                row = await cursor.fetchone()
                return row
                
        elif self.config.db_type == 'sqlite':
            conn.row_factory = aiosqlite.Row
            if values:
                cursor = await conn.execute(query, values)
            else:
                cursor = await conn.execute(query)
            row = await cursor.fetchone()
            return dict(row) if row else None
    
    def _convert_named_params_pg(self, query: str, values: Dict[str, Any]):
        """将命名参数转换为PostgreSQL的位置参数"""
        import re
        
        # 找到所有命名参数
        param_pattern = r':(\w+)'
        params = re.findall(param_pattern, query)
        
        # 转换为位置参数
        new_query = query
        args = []
        for i, param in enumerate(params, 1):
            new_query = new_query.replace(f':{param}', f'${i}')
            args.append(values.get(param))
            
        return new_query, args


class DatabaseManager:
    """数据库管理器 - 管理多个数据库连接"""
    
    def __init__(self):
        self.pools: Dict[str, DatabasePool] = {}
        self.default_pool: Optional[DatabasePool] = None
    
    def add_database(self, name: str, config: DatabaseConfig, is_default: bool = False):
        """添加数据库连接"""
        pool = DatabasePool(config)
        self.pools[name] = pool
        
        if is_default or self.default_pool is None:
            self.default_pool = pool
    
    def get_database(self, name: str = None) -> DatabasePool:
        """获取数据库连接池"""
        if name is None:
            if self.default_pool is None:
                raise ValueError("没有配置默认数据库")
            return self.default_pool
        
        if name not in self.pools:
            raise ValueError(f"数据库 '{name}' 不存在")
        
        return self.pools[name]
    
    async def connect_all(self):
        """连接所有数据库"""
        for pool in self.pools.values():
            await pool.connect()
    
    async def disconnect_all(self):
        """断开所有数据库连接"""
        for pool in self.pools.values():
            await pool.disconnect()


# 全局数据库管理器实例
db_manager = DatabaseManager() 