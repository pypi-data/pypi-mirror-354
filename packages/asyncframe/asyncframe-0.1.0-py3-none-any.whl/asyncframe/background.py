"""
后台任务管理 - 异步后台任务执行
"""

import asyncio
import uuid
from typing import Callable, Any, Dict, List, Optional


class BackgroundTask:
    """单个后台任务"""
    
    def __init__(self, func: Callable, *args, **kwargs):
        self.id = str(uuid.uuid4())
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.status = "pending"
    
    async def execute(self):
        """执行任务"""
        self.status = "running"
        
        try:
            if asyncio.iscoroutinefunction(self.func):
                await self.func(*self.args, **self.kwargs)
            else:
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(None, self.func, *self.args, **self.kwargs)
            
            self.status = "completed"
        except Exception as e:
            self.status = "failed"
            print(f"后台任务失败: {e}")


class BackgroundTaskManager:
    """后台任务管理器"""
    
    def __init__(self):
        self.tasks: Dict[str, BackgroundTask] = {}
    
    def add_task(self, func: Callable, *args, **kwargs) -> str:
        """添加后台任务"""
        task = BackgroundTask(func, *args, **kwargs)
        self.tasks[task.id] = task
        
        # 立即启动任务
        asyncio.create_task(task.execute())
        
        return task.id
    
    def get_task(self, task_id: str) -> Optional[BackgroundTask]:
        """获取任务信息"""
        return self.tasks.get(task_id)


class BackgroundTasks:
    """简化的后台任务接口"""
    
    def __init__(self):
        self.tasks: List[BackgroundTask] = []
    
    def add_task(self, func: Callable, *args, **kwargs):
        """添加任务"""
        task = BackgroundTask(func, *args, **kwargs)
        self.tasks.append(task)
    
    async def execute_all(self):
        """执行所有任务"""
        if not self.tasks:
            return
        
        await asyncio.gather(
            *[task.execute() for task in self.tasks],
            return_exceptions=True
        ) 