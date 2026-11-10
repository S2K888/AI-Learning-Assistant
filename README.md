# AI Chat API

基于已学习的 FastAPI、OpenAI 兼容接口和 SQLite 聊天后端整理。项目使用同步函数和原生 sqlite3。

## 准备

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

在 `.env` 中填写自己的 `DEEPSEEK_API_KEY`。不要把真实密钥提交或分享。

## 启动

```powershell
uvicorn app.main:app --reload
```

打开 `http://127.0.0.1:8000/docs` 可以查看和调用接口。数据库 `chat.db` 会在项目根目录自动创建。

## 接口

- `POST /chat`：请求体 `{"session_id":"abc","message":"你好"}`；读取会话历史、调用模型、保存用户和 AI 回复，返回 `{"reply": ...}`。
- `GET /chat/{session_id}`：读取会话记录；没有记录时返回 404。
- `DELETE /chat/{session_id}`：删除该会话记录；没有记录时返回 404。

AI 回复按 JSON 解析；如果不是合法 JSON，会返回包含 `error` 和 `raw_reply` 的对象。AI 请求异常会转换成 HTTP 500。

## 文件说明

- `app/main.py`：创建 FastAPI 应用、启动时建表并注册路由。
- `app/routers/chat.py`：三个 HTTP 接口及请求流程。
- `app/services/chat_service.py`：system prompt、模型调用和 JSON 解析。
- `app/database/db.py`：SQLite 建表、保存、读取、删除函数；`get_messages` 只定义一次。
- `app/schemas/chat.py`：聊天请求的数据结构。
- `app/core/config.py`：读取 `.env` 和集中管理配置。
- `.env.example`：配置模板；真实 `.env` 由你本地创建。
- `requirements.txt`：项目依赖。

建议下一步从 `app/main.py` 开始，先看应用如何注册路由和在启动时初始化数据库，再沿着 `chat.py` 到 service、database 追踪一次请求。
