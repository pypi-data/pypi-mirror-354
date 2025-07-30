#!/usr/bin/env python
"""
AsyncFrame 命令行管理工具
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any


class ProjectTemplate:
    """项目模版生成器"""
    
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_path = Path(project_name)
    
    def create_project(self):
        """创建项目结构"""
        if self.project_path.exists():
            print(f"错误: 目录 '{self.project_name}' 已存在!")
            return False
        
        print(f"正在创建 AsyncFrame 项目: {self.project_name}")
        
        # 创建项目目录结构
        self._create_directory_structure()
        
        # 创建配置文件
        self._create_config_files()
        
        # 创建应用文件
        self._create_app_files()
        
        # 创建模型文件
        self._create_model_files()
        
        # 创建视图文件
        self._create_view_files()
        
        # 创建路由文件
        self._create_route_files()
        
        # 创建模板文件
        self._create_template_files()
        
        print(f"\n✅ 项目 '{self.project_name}' 创建成功!")
        print(f"\n下一步操作:")
        print(f"  cd {self.project_name}")
        print(f"  pip install asyncframe")
        print(f"  python app.py")
        
        return True
    
    def _create_directory_structure(self):
        """创建目录结构"""
        directories = [
            self.project_path,
            self.project_path / "models",
            self.project_path / "views", 
            self.project_path / "routes",
            self.project_path / "templates",
            self.project_path / "static",
            self.project_path / "static" / "css",
            self.project_path / "static" / "js",
            self.project_path / "migrations",
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"创建目录: {directory}")
    
    def _create_config_files(self):
        """创建配置文件"""
        # requirements.txt
        requirements_content = """asyncframe>=0.1.0
uvicorn>=0.18.0
python-dotenv>=0.19.0
jinja2>=3.1.0
aiofiles>=0.8.0
"""
        self._write_file("requirements.txt", requirements_content)
        
        # .env
        env_content = """# 数据库配置
DATABASE_URL=sqlite:///./app.db

# 服务器配置
DEBUG=True
HOST=0.0.0.0
PORT=8000

# 安全配置
SECRET_KEY=your-secret-key-here
"""
        self._write_file(".env", env_content)
        
        # .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/

# AsyncFrame
*.db
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
        self._write_file(".gitignore", gitignore_content)
        
        # README.md
        readme_content = f"""# {self.project_name}

基于 AsyncFrame 框架构建的异步 Web 应用

## 快速开始

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 运行应用:
```bash
python app.py
```

3. 访问应用:
打开浏览器访问 http://localhost:8000

## 项目结构

```
{self.project_name}/
├── app.py              # 主应用文件
├── models/             # 数据模型
│   ├── __init__.py
│   └── user.py
├── views/              # 视图函数/类
│   ├── __init__.py
│   ├── index.py
│   └── user.py
├── routes/             # 路由配置
│   ├── __init__.py
│   └── main.py
├── templates/          # 模板文件
├── static/            # 静态文件
│   ├── css/
│   └── js/
├── migrations/        # 数据库迁移
├── requirements.txt   # 依赖文件
├── .env              # 环境变量
└── README.md         # 项目说明
```

## 功能特性

- ✅ 异步ORM支持
- ✅ RESTful API
- ✅ 类视图和函数视图
- ✅ 自动数据库迁移
- ✅ 静态文件服务
- ✅ 模板引擎集成

## API文档

### 用户相关接口

- GET /api/users - 获取用户列表
- POST /api/users - 创建用户
- GET /api/users/{{id}} - 获取单个用户
- PUT /api/users/{{id}} - 更新用户
- DELETE /api/users/{{id}} - 删除用户

## 开发指南

1. 创建新模型: 在 `models/` 目录下创建新的模型文件
2. 创建新视图: 在 `views/` 目录下创建新的视图文件
3. 配置路由: 在 `routes/main.py` 中添加新的路由规则
"""
        self._write_file("README.md", readme_content)
    
    def _create_app_files(self):
        """创建主应用文件"""
        app_content = f'''"""
{self.project_name} - AsyncFrame 应用主入口
"""

import os
from asyncframe import AsyncFrame
from asyncframe.database import db_manager, DatabaseConfig
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建应用实例
app = AsyncFrame()

# 配置数据库
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
db_config = DatabaseConfig(DATABASE_URL)
db_manager.add_database("default", db_config, is_default=True)

# 导入模型 (确保数据库表创建)
from models import *

# 导入路由
from routes.main import router
app.include_router(router)

# 静态文件服务
app.mount("/static", app.static_files("static"))

# 主页路由
@app.route("/")
async def index(request):
    return app.render_template("index.html", {{
        "title": "{self.project_name}",
        "message": "欢迎使用 AsyncFrame!"
    }})

# 健康检查
@app.route("/health")
async def health_check(request):
    return {{"status": "ok", "message": "服务运行正常"}}

if __name__ == "__main__":
    import uvicorn
    
    # 获取配置
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "False").lower() == "true"
    
    print(f"🚀 启动 {{'{self.project_name}'}} 应用...")
    print(f"📡 服务地址: http://{{host}}:{{port}}")
    print(f"🔧 调试模式: {{debug}}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=debug
    )
'''
        self._write_file("app.py", app_content)
    
    def _create_model_files(self):
        """创建模型文件"""
        # models/__init__.py
        models_init_content = '''"""
数据模型包
"""

from .user import User

__all__ = ["User"]
'''
        self._write_file("models/__init__.py", models_init_content)
        
        # models/user.py
        user_model_content = '''"""
用户模型
"""

from asyncframe.models import Model
from asyncframe.fields import IntegerField, CharField, EmailField, BooleanField, DateTimeField


class User(Model):
    """用户模型"""
    
    class Meta:
        table_name = "users"
    
    # 主键
    id = IntegerField(primary_key=True, auto_increment=True)
    
    # 基本信息
    username = CharField(max_length=50, unique=True, null=False, help_text="用户名")
    email = EmailField(unique=True, null=False, help_text="邮箱地址")
    password = CharField(max_length=255, null=False, help_text="密码")
    
    # 个人信息
    first_name = CharField(max_length=30, null=True, blank=True, help_text="名字")
    last_name = CharField(max_length=30, null=True, blank=True, help_text="姓氏")
    
    # 状态字段
    is_active = BooleanField(default=True, help_text="是否激活")
    is_staff = BooleanField(default=False, help_text="是否为员工")
    is_superuser = BooleanField(default=False, help_text="是否为超级用户")
    
    # 时间字段
    created_at = DateTimeField(auto_now_add=True, help_text="创建时间")
    updated_at = DateTimeField(auto_now=True, help_text="更新时间")
    last_login = DateTimeField(null=True, blank=True, help_text="最后登录时间")
    
    def __str__(self):
        return f"User(id={self.id}, username={self.username})"
    
    def __repr__(self):
        return f"<User: {self.username}>"
    
    @property
    def full_name(self):
        """获取全名"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def to_dict(self, exclude_fields=None):
        """转换为字典，默认排除敏感字段"""
        if exclude_fields is None:
            exclude_fields = ['password']
        return super().to_dict(exclude_fields=exclude_fields)
'''
        self._write_file("models/user.py", user_model_content)
    
    def _create_view_files(self):
        """创建视图文件"""
        # views/__init__.py
        views_init_content = '''"""
视图包
"""

from .index import IndexView
from .user import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

__all__ = [
    "IndexView",
    "UserListView", 
    "UserDetailView", 
    "UserCreateView", 
    "UserUpdateView", 
    "UserDeleteView"
]
'''
        self._write_file("views/__init__.py", views_init_content)
        
        # views/index.py
        index_view_content = '''"""
首页视图
"""

from asyncframe.views import BaseView
from asyncframe.response import JSONResponse


class IndexView(BaseView):
    """首页视图"""
    
    async def get(self, request):
        """处理GET请求"""
        return JSONResponse({
            "message": "欢迎使用 AsyncFrame!",
            "status": "success",
            "version": "1.0.0"
        })


# 函数视图示例
async def welcome(request):
    """欢迎页面"""
    return JSONResponse({
        "message": "这是一个函数视图示例",
        "method": request.method,
        "path": request.url.path
    })
'''
        self._write_file("views/index.py", index_view_content)
        
        # views/user.py
        user_view_content = '''"""
用户相关视图
"""

from asyncframe.views import (
    ModelListAPIView, 
    ModelRetrieveAPIView, 
    ModelCreateAPIView,
    ModelUpdateAPIView,
    ModelDestroyAPIView
)
from asyncframe.response import JSONResponse
from asyncframe.exceptions import HTTPException
from models.user import User


class UserListView(ModelListAPIView):
    """用户列表视图"""
    model = User
    fields = ["id", "username", "email", "first_name", "last_name", "is_active", "created_at"]
    page_size = 20


class UserDetailView(ModelRetrieveAPIView):
    """用户详情视图"""
    model = User
    exclude_fields = ["password"]


class UserCreateView(ModelCreateAPIView):
    """用户创建视图"""
    model = User
    fields = ["username", "email", "password", "first_name", "last_name"]
    
    async def post(self, request, **kwargs):
        """重写post方法，添加密码加密等逻辑"""
        # 这里可以添加密码加密、数据验证等逻辑
        data = self.get_create_data()
        
        # 简单的数据验证
        if not data.get("username"):
            raise HTTPException(400, "用户名不能为空")
        if not data.get("email"):
            raise HTTPException(400, "邮箱不能为空")
        if not data.get("password"):
            raise HTTPException(400, "密码不能为空")
        
        # 检查用户名是否已存在
        existing_user = await User.objects.filter(username=data["username"]).first()
        if existing_user:
            raise HTTPException(400, "用户名已存在")
        
        # 检查邮箱是否已存在
        existing_email = await User.objects.filter(email=data["email"]).first()
        if existing_email:
            raise HTTPException(400, "邮箱已被使用")
        
        return await super().post(request, **kwargs)


class UserUpdateView(ModelUpdateAPIView):
    """用户更新视图"""
    model = User
    fields = ["username", "email", "first_name", "last_name", "is_active"]
    
    async def put(self, request, **kwargs):
        """重写put方法，添加更新逻辑"""
        data = self.get_update_data()
        
        # 如果更新用户名，检查是否已存在
        if "username" in data:
            user_id = kwargs.get("id")
            existing_user = await User.objects.filter(username=data["username"]).exclude(id=user_id).first()
            if existing_user:
                raise HTTPException(400, "用户名已存在")
        
        # 如果更新邮箱，检查是否已存在
        if "email" in data:
            user_id = kwargs.get("id")
            existing_email = await User.objects.filter(email=data["email"]).exclude(id=user_id).first()
            if existing_email:
                raise HTTPException(400, "邮箱已被使用")
        
        return await super().put(request, **kwargs)


class UserDeleteView(ModelDestroyAPIView):
    """用户删除视图"""
    model = User
    
    async def delete(self, request, **kwargs):
        """重写delete方法，添加删除前检查"""
        user = await self.get_object()
        
        # 防止删除超级用户
        if user.is_superuser:
            raise HTTPException(400, "不能删除超级用户")
        
        return await super().delete(request, **kwargs)


# 函数视图示例
async def user_stats(request):
    """用户统计接口"""
    total_users = await User.objects.count()
    active_users = await User.objects.filter(is_active=True).count()
    staff_users = await User.objects.filter(is_staff=True).count()
    
    return JSONResponse({
        "total_users": total_users,
        "active_users": active_users,
        "staff_users": staff_users,
        "inactive_users": total_users - active_users
    })
'''
        self._write_file("views/user.py", user_view_content)
    
    def _create_route_files(self):
        """创建路由文件"""
        # routes/__init__.py
        routes_init_content = '''"""
路由包
"""

from .main import router

__all__ = ["router"]
'''
        self._write_file("routes/__init__.py", routes_init_content)
        
        # routes/main.py
        main_route_content = '''"""
主路由配置
"""

from asyncframe.routing import Router
from views.index import IndexView, welcome
from views.user import (
    UserListView, UserDetailView, UserCreateView, 
    UserUpdateView, UserDeleteView, user_stats
)

# 创建路由器
router = Router()

# ==================== 首页路由 ====================
router.add_class_view("/api", IndexView)
router.add_route("/api/welcome", welcome, ["GET"])

# ==================== 用户相关路由 ====================

# 用户列表和创建
router.add_class_view("/api/users", UserListView, ["GET"])
router.add_class_view("/api/users", UserCreateView, ["POST"])

# 用户详情、更新和删除
router.add_class_view("/api/users/{id:int}", UserDetailView, ["GET"])
router.add_class_view("/api/users/{id:int}", UserUpdateView, ["PUT", "PATCH"])
router.add_class_view("/api/users/{id:int}", UserDeleteView, ["DELETE"])

# 用户统计
router.add_route("/api/users/stats", user_stats, ["GET"])

# ==================== 其他路由示例 ====================

# RESTful 路由示例
@router.route("/api/test", ["GET", "POST"])
async def test_endpoint(request):
    """测试端点"""
    return {
        "method": request.method,
        "message": "这是一个测试端点",
        "data": await request.json() if request.method == "POST" else None
    }

# 路径参数示例
@router.route("/api/hello/{name}", ["GET"])
async def hello_name(request, name):
    """带参数的问候接口"""
    return {"message": f"Hello, {name}!"}

# 查询参数示例
@router.route("/api/search", ["GET"])
async def search(request):
    """搜索接口"""
    query = request.get_query_param("q", "")
    page = int(request.get_query_param("page", 1))
    
    return {
        "query": query,
        "page": page,
        "results": f"搜索 '{query}' 的结果 (第 {page} 页)"
    }
'''
        self._write_file("routes/main.py", main_route_content)
    
    def _create_template_files(self):
        """创建模板文件"""
        # templates/index.html
        index_template_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{{{ title }}}}</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>{{{{ title }}</h1>
            <p>基于 AsyncFrame 构建的现代异步 Web 应用</p>
        </header>
        
        <main>
            <div class="welcome-card">
                <h2>{{{{ message }}</h2>
                <p>您的 AsyncFrame 应用已成功运行!</p>
                
                <div class="features">
                    <div class="feature">
                        <h3>🚀 异步优先</h3>
                        <p>基于 asyncio 的高性能异步框架</p>
                    </div>
                    <div class="feature">
                        <h3>🗄️ ORM 支持</h3>
                        <p>内置异步 ORM，支持多种数据库</p>
                    </div>
                    <div class="feature">
                        <h3>🛠️ 开发友好</h3>
                        <p>类视图、函数视图，RESTful API</p>
                    </div>
                </div>
                
                <div class="api-links">
                    <h3>快速测试 API:</h3>
                    <ul>
                        <li><a href="/api" target="_blank">GET /api</a> - API信息</li>
                        <li><a href="/api/users" target="_blank">GET /api/users</a> - 用户列表</li>
                        <li><a href="/api/users/stats" target="_blank">GET /api/users/stats</a> - 用户统计</li>
                        <li><a href="/health" target="_blank">GET /health</a> - 健康检查</li>
                    </ul>
                </div>
            </div>
        </main>
        
        <footer>
            <p>&copy; 2024 {self.project_name} - Powered by AsyncFrame</p>
        </footer>
    </div>
    
    <script src="/static/js/app.js"></script>
</body>
</html>
'''
        self._write_file("templates/index.html", index_template_content)
        
        # static/css/style.css
        style_content = '''/* AsyncFrame 项目样式 */

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    line-height: 1.6;
    color: #333;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

header {
    text-align: center;
    color: white;
    margin-bottom: 2rem;
}

header h1 {
    font-size: 3rem;
    margin-bottom: 0.5rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

header p {
    font-size: 1.2rem;
    opacity: 0.9;
}

main {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.welcome-card {
    background: white;
    border-radius: 16px;
    padding: 3rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    max-width: 800px;
    width: 100%;
}

.welcome-card h2 {
    font-size: 2rem;
    color: #4a5568;
    margin-bottom: 1rem;
    text-align: center;
}

.welcome-card > p {
    text-align: center;
    font-size: 1.1rem;
    color: #718096;
    margin-bottom: 2rem;
}

.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin: 2rem 0;
}

.feature {
    text-align: center;
    padding: 1.5rem;
    border-radius: 12px;
    background: #f7fafc;
    border: 1px solid #e2e8f0;
}

.feature h3 {
    font-size: 1.3rem;
    color: #2d3748;
    margin-bottom: 0.5rem;
}

.feature p {
    color: #718096;
}

.api-links {
    margin-top: 2rem;
    padding: 1.5rem;
    background: #edf2f7;
    border-radius: 12px;
}

.api-links h3 {
    color: #2d3748;
    margin-bottom: 1rem;
}

.api-links ul {
    list-style: none;
}

.api-links li {
    margin-bottom: 0.5rem;
}

.api-links a {
    color: #667eea;
    text-decoration: none;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.9rem;
    padding: 0.3rem 0.6rem;
    background: white;
    border-radius: 6px;
    border: 1px solid #e2e8f0;
    display: inline-block;
    transition: all 0.2s;
}

.api-links a:hover {
    background: #667eea;
    color: white;
    transform: translateY(-1px);
}

footer {
    text-align: center;
    color: white;
    margin-top: 2rem;
    opacity: 0.8;
}

@media (max-width: 768px) {
    .container {
        padding: 1rem;
    }
    
    header h1 {
        font-size: 2rem;
    }
    
    .welcome-card {
        padding: 2rem;
    }
    
    .features {
        grid-template-columns: 1fr;
    }
}
'''
        self._write_file("static/css/style.css", style_content)
        
        # static/js/app.js
        js_content = '''// AsyncFrame 项目 JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('AsyncFrame 应用已加载');
    
    // 添加一些交互效果
    const features = document.querySelectorAll('.feature');
    features.forEach(feature => {
        feature.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        feature.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // API链接点击统计
    const apiLinks = document.querySelectorAll('.api-links a');
    apiLinks.forEach(link => {
        link.addEventListener('click', function() {
            console.log(`访问API: ${this.href}`);
        });
    });
});

// 简单的API测试函数
async function testAPI(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log('API响应:', data);
        return data;
    } catch (error) {
        console.error('API请求失败:', error);
    }
}

// 全局可用的工具函数
window.AsyncFrameUtils = {
    testAPI: testAPI,
    log: (message) => console.log(`[AsyncFrame] ${message}`)
};
'''
        self._write_file("static/js/app.js", js_content)
    
    def _write_file(self, file_path: str, content: str):
        """写入文件内容"""
        full_path = self.project_path / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"创建文件: {full_path}")


def create_project(project_name: str):
    """创建新项目"""
    if not project_name:
        print("错误: 请提供项目名称")
        return False
    
    # 验证项目名称
    if not project_name.isidentifier():
        print("错误: 项目名称必须是有效的Python标识符")
        return False
    
    template = ProjectTemplate(project_name)
    return template.create_project()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="AsyncFrame 命令行管理工具",
        prog="asyncframe"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建新项目')
    create_parser.add_argument('project_name', help='项目名称')
    
    # version 命令
    version_parser = subparsers.add_parser('version', help='显示版本信息')
    
    # 如果没有参数，显示帮助
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    args = parser.parse_args()
    
    if args.command == 'create':
        success = create_project(args.project_name)
        sys.exit(0 if success else 1)
    
    elif args.command == 'version':
        print("AsyncFrame 0.1.0")
        print("现代异步Python Web框架")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 