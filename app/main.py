from fastapi import FastAPI

from app.database.db import init_db
from app.routers.chat import router as chat_router

app = FastAPI(title="AI Chat API")


@app.on_event("startup")
def startup():
    init_db()


app.include_router(chat_router)

# 这份文件只有三个核心任务：
# 1. 创建 FastAPI 应用。
# 2. 启动时初始化数据库。
# 3. 注册聊天路由。

# main.py 是整个 FastAPI 项目的入口，它不负责具体业务，而是负责把应用创建起来，并把各个模块组织起来。