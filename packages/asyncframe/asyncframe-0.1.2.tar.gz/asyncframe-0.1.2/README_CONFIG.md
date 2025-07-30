# AsyncFrame 数据库配置指南

AsyncFrame 框架支持从 `.env` 文件读取数据库配置，让你可以轻松地在不同的数据库之间切换而无需修改代码。

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install python-dotenv uvicorn asyncpg aiomysql aiosqlite databases
```

### 2. 配置数据库

选择你想使用的数据库类型，并复制相应的配置：

#### 方法一：使用配置模板

```bash
# 复制基础配置文件
cp config.env .env

# 然后编辑 .env 文件，修改相应的配置
```

#### 方法二：使用专用配置

```bash
# 使用 SQLite (默认)
cp config.env .env

# 使用 MySQL
cp mysql_config.env .env

# 使用 PostgreSQL  
cp postgresql_config.env .env
```

### 3. 启动应用

```bash
python example_model_app.py
```

## 📝 配置说明

### SQLite 配置 (默认)

```env
DB_TYPE=sqlite
SQLITE_PATH=./example.db
```

SQLite 不需要额外的服务器，适合开发和测试。

### MySQL 配置

```env
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=asyncframe_test
MYSQL_MIN_SIZE=2
MYSQL_MAX_SIZE=10
```

**MySQL 设置步骤：**

1. 安装 MySQL 服务器
2. 创建数据库：
   ```sql
   CREATE DATABASE asyncframe_test;
   ```
3. 修改 `.env` 文件中的密码
4. 启动应用

### PostgreSQL 配置

```env
DB_TYPE=postgresql
PG_HOST=localhost
PG_PORT=5432
PG_USER=postgres
PG_PASSWORD=your_password
PG_DATABASE=asyncframe_test
PG_MIN_SIZE=5
PG_MAX_SIZE=20
```

**PostgreSQL 设置步骤：**

1. 安装 PostgreSQL 服务器
2. 创建数据库：
   ```sql
   CREATE DATABASE asyncframe_test;
   ```
3. 修改 `.env` 文件中的密码
4. 启动应用

## ⚙️ 应用配置

除了数据库配置，你还可以配置应用的其他参数：

```env
# 应用配置
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
LOG_LEVEL=info

# 安全配置
CORS_ORIGINS=*
SECRET_KEY=your-secret-key-here
```

## 🔧 配置参数详解

### 数据库参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `DB_TYPE` | 数据库类型 (sqlite/mysql/postgresql) | sqlite |
| `SQLITE_PATH` | SQLite 数据库文件路径 | ./example.db |
| `MYSQL_HOST` | MySQL 服务器地址 | localhost |
| `MYSQL_PORT` | MySQL 端口 | 3306 |
| `MYSQL_USER` | MySQL 用户名 | root |
| `MYSQL_PASSWORD` | MySQL 密码 | password |
| `MYSQL_DATABASE` | MySQL 数据库名 | asyncframe_test |
| `MYSQL_MIN_SIZE` | MySQL 连接池最小连接数 | 2 |
| `MYSQL_MAX_SIZE` | MySQL 连接池最大连接数 | 10 |
| `PG_HOST` | PostgreSQL 服务器地址 | localhost |
| `PG_PORT` | PostgreSQL 端口 | 5432 |
| `PG_USER` | PostgreSQL 用户名 | postgres |
| `PG_PASSWORD` | PostgreSQL 密码 | password |
| `PG_DATABASE` | PostgreSQL 数据库名 | asyncframe_test |
| `PG_MIN_SIZE` | PostgreSQL 连接池最小连接数 | 5 |
| `PG_MAX_SIZE` | PostgreSQL 连接池最大连接数 | 20 |

### 应用参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `APP_HOST` | 应用监听地址 | 0.0.0.0 |
| `APP_PORT` | 应用监听端口 | 8000 |
| `DEBUG` | 调试模式 | true |
| `LOG_LEVEL` | 日志级别 | info |
| `CORS_ORIGINS` | 允许的CORS源 (逗号分隔) | * |
| `SECRET_KEY` | 应用密钥 | your-secret-key-here |

## 🎯 使用示例

### 切换到 MySQL

1. 编辑 `.env` 文件：
   ```env
   DB_TYPE=mysql
   MYSQL_HOST=localhost
   MYSQL_USER=myuser
   MYSQL_PASSWORD=mypassword
   MYSQL_DATABASE=mydatabase
   ```

2. 重启应用：
   ```bash
   python example_model_app.py
   ```

### 切换端口和调试模式

```env
APP_PORT=8080
DEBUG=false
LOG_LEVEL=warning
```

### 配置 CORS

```env
# 允许特定域名
CORS_ORIGINS=http://localhost:3000,https://myapp.com

# 允许所有域名 (开发环境)
CORS_ORIGINS=*
```

## 🔍 测试配置

应用提供了几个端点来测试配置：

- `GET /api/config` - 查看当前配置
- `GET /api/db-info` - 查看数据库连接信息
- `POST /api/test-db-compatibility` - 测试数据库兼容性

## 📁 文件结构

```
web_server/
├── .env                    # 你的配置文件 (不要提交到git)
├── config.env              # 配置模板
├── mysql_config.env        # MySQL 配置示例  
├── postgresql_config.env   # PostgreSQL 配置示例
├── example_model_app.py    # 主应用文件
└── README_CONFIG.md        # 本文档
```

## ⚠️ 安全建议

1. **不要提交 `.env` 文件到版本控制系统**
2. **生产环境使用强密钥**：
   ```env
   SECRET_KEY=your-very-strong-secret-key-here
   ```
3. **限制 CORS 源**：
   ```env
   CORS_ORIGINS=https://yourdomain.com
   ```
4. **使用专用数据库用户**，不要使用 root 用户

## 🐛 故障排除

### 常见问题

1. **找不到 `.env` 文件**
   - 确保 `.env` 文件在项目根目录
   - 检查文件名拼写是否正确

2. **数据库连接失败**
   - 检查数据库服务器是否运行
   - 验证用户名和密码是否正确
   - 确认数据库是否存在

3. **导入 dotenv 失败**
   ```bash
   pip install python-dotenv
   ```

4. **端口被占用**
   - 修改 `APP_PORT` 为其他端口
   - 或者停止占用端口的进程

### 调试技巧

1. **查看配置加载日志**
   应用启动时会显示配置加载信息

2. **使用配置接口**
   访问 `http://localhost:8000/api/config` 查看当前配置

3. **测试数据库连接**
   访问 `http://localhost:8000/api/db-info` 测试数据库连接 