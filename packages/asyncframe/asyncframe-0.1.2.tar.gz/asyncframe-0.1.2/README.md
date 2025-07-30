# AsyncFrame

一个现代化的基于协程的异步Python Web框架，基于ASGI标准构建，提供高性能的异步编程体验。

## 🌟 主要特性

### 核心架构
- **基于ASGI标准**：完全兼容ASGI规范，支持HTTP/1.1和HTTP/2
- **原生async/await**：全面支持Python原生协程
- **高性能异步处理**：基于事件循环的异步I/O
- **模块化设计**：清晰的组件分离和扩展点

### 核心功能
- **异步路由系统**：支持路径参数、类型转换、多HTTP方法
- **请求/响应管道**：完整的HTTP请求响应处理
- **中间件支持**：可扩展的中间件系统
- **WebSocket支持**：原生WebSocket连接处理
- **后台任务管理**：异步后台任务执行

### 内置中间件
- **CORS中间件**：跨源资源共享支持
- **日志中间件**：请求日志记录
- **安全中间件**：HTTP安全头设置
- **速率限制**：简单的API速率限制
- **响应压缩**：Gzip压缩支持

## 📦 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 创建基本应用

```python
from asyncframe import AsyncFrame, JSONResponse

app = AsyncFrame(debug=True)

@app.get("/")
async def hello(request):
    return JSONResponse({"message": "Hello, AsyncFrame!"})

@app.get("/users/{user_id:int}")
async def get_user(request):
    user_id = request.path_params["user_id"]
    return JSONResponse({"user_id": user_id, "name": f"用户{user_id}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 运行示例应用

```bash
python example_app.py
```

访问 http://localhost:8000 查看完整示例。

## 🚀 核心概念

### 路由系统

```python
# 基本路由
@app.get("/api/hello")
async def hello_api(request):
    return JSONResponse({"message": "Hello"})

# 路径参数
@app.get("/users/{user_id:int}")
async def get_user(request):
    user_id = request.path_params["user_id"]
    return JSONResponse({"user_id": user_id})

# 多种HTTP方法
@app.route("/api/data", methods=["GET", "POST", "PUT"])
async def handle_data(request):
    if request.method == "GET":
        return JSONResponse({"data": "get_data"})
    elif request.method == "POST":
        data = await request.json()
        return JSONResponse({"received": data})
```

### 请求处理

```python
@app.post("/api/submit")
async def submit_data(request):
    # JSON数据
    json_data = await request.json()
    
    # 表单数据
    form_data = await request.form()
    
    # 原始文本
    text_data = await request.text()
    
    # 查询参数
    param = request.get_query_param("param", "default")
    
    # 请求头
    user_agent = request.get_header("user-agent")
    
    return JSONResponse({"status": "success"})
```

### 响应类型

```python
from asyncframe import JSONResponse, HTMLResponse, RedirectResponse, FileResponse

@app.get("/json")
async def json_response(request):
    return JSONResponse({"data": "value"})

@app.get("/html")
async def html_response(request):
    return HTMLResponse("<h1>Hello HTML</h1>")

@app.get("/redirect")
async def redirect_response(request):
    return RedirectResponse("/")

@app.get("/file")
async def file_response(request):
    return FileResponse("static/file.pdf")
```

### 中间件使用

```python
from asyncframe.middleware import LoggingMiddleware, CORSMiddleware

# 添加中间件
app.add_middleware(LoggingMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# 自定义中间件
class CustomMiddleware:
    async def before_request(self, request):
        print(f"请求开始: {request.url}")
        return request
    
    async def after_request(self, request, response):
        print(f"请求结束: {response.status_code}")
        return response

app.add_middleware(CustomMiddleware)
```

### WebSocket支持

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()
    
    try:
        async for message in websocket.iter_json():
            # 处理消息
            await websocket.send_json({"echo": message})
    except Exception as e:
        print(f"WebSocket错误: {e}")
```

### 后台任务

```python
async def send_email(email, subject):
    # 模拟发送邮件
    print(f"发送邮件到 {email}")

@app.post("/send-email")
async def create_email_task(request):
    data = await request.json()
    
    # 添加后台任务
    task_id = app.add_background_task(
        send_email, 
        data["email"], 
        data["subject"]
    )
    
    return JSONResponse({"task_id": task_id})
```

### 异常处理

```python
from asyncframe.exceptions import HTTPException

@app.get("/error")
async def trigger_error(request):
    raise HTTPException(400, "这是一个错误")

@app.exception_handler(404)
async def not_found_handler(exc):
    return JSONResponse({"error": "未找到"}, status_code=404)
```

### 生命周期事件

```python
@app.on_startup
async def startup_event():
    print("应用启动")
    # 初始化数据库连接、缓存等

@app.on_shutdown  
async def shutdown_event():
    print("应用关闭")
    # 清理资源
```

## 🏗️ 项目结构

```
asyncframe/
├── __init__.py          # 框架入口
├── application.py       # 核心应用类
├── routing.py          # 路由系统
├── request.py          # 请求处理
├── response.py         # 响应处理
├── middleware.py       # 中间件系统
├── websocket.py        # WebSocket支持
├── background.py       # 后台任务
├── exceptions.py       # 异常定义
└── url.py             # URL处理

example_app.py          # 使用示例
requirements.txt        # 依赖文件
README.md              # 说明文档
```

## 🔧 配置和扩展

### 自定义配置

```python
app = AsyncFrame(
    debug=True,           # 调试模式
)

# 添加自定义配置
app.config = {
    "DATABASE_URL": "sqlite:///app.db",
    "SECRET_KEY": "your-secret-key"
}
```

### 路由分组

```python
from asyncframe.routing import Router

# 创建子路由器
api_router = Router()

@api_router.get("/users")
async def list_users(request):
    return JSONResponse({"users": []})

@api_router.get("/users/{user_id}")
async def get_user(request):
    return JSONResponse({"user": "data"})

# 包含到主应用
app.router.include_router(api_router, prefix="/api/v1")
```

## 🚀 性能特性

- **异步I/O**：基于asyncio的高并发处理
- **零拷贝响应**：流式响应和文件传输
- **连接池支持**：可配合aiohttp、asyncpg等使用
- **内存优化**：最小化内存占用和垃圾回收

## 📋 TODO

- [ ] 模板引擎集成 (Jinja2)
- [ ] 数据库ORM支持
- [ ] 身份验证和授权
- [ ] 静态文件服务
- [ ] API文档自动生成
- [ ] 测试客户端
- [ ] 性能监控

## 🤝 贡献

欢迎贡献代码！请确保：

1. 遵循现有代码风格
2. 添加适当的测试
3. 更新相关文档
4. 提交前运行所有测试

## 📄 许可证

MIT License - 详见 LICENSE 文件。

---

**AsyncFrame** - 为现代Python异步应用而生的Web框架 🚀 