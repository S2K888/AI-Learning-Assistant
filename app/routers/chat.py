import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatMessage
from app.services.chat_service import chat_with_ai, chat_with_ai_stream
from app.database.db import delete_messages, get_messages, save_message

router = APIRouter()


# 普通聊天接口：一次性返回
@router.post("/chat")
def chat(data: ChatMessage):
    messages = get_messages(data.session_id)
    messages.append({"role": "user", "content": data.message})

    ai_reply, raw_reply = chat_with_ai(messages)

    save_message(data.session_id, "user", data.message)
    save_message(data.session_id, "assistant", raw_reply)

    return {"reply": ai_reply}


# 流式聊天接口：逐步返回
@router.post("/chat/stream")
def chat_stream(data: ChatMessage):
    messages = get_messages(data.session_id)
    messages.append({"role": "user", "content": data.message})

    def generate():
        full_reply = ""

        for chunk in chat_with_ai_stream(messages):
            full_reply += chunk

            yield f"data: {json.dumps({'content': chunk}, ensure_ascii=False)}\n\n"
            # yield 的作用是：向外产出一个值，然后暂停函数执行。

        save_message(data.session_id, "user", data.message)
        save_message(data.session_id, "assistant", full_reply)

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )


# 查询历史聊天记录
@router.get("/chat/{session_id}")
def get_chat(session_id: str):
    messages = get_messages(session_id)

    if not messages:
        raise HTTPException(status_code=404, detail="聊天记录不存在")

    return {"session_id": session_id, "messages": messages}


# 删除历史聊天记录
@router.delete("/chat/{session_id}")
def clear_chat(session_id: str):
    deleted_count = delete_messages(session_id)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="聊天记录不存在")

    return {"message": "聊天记录已清空"}


# APIRouter()	             创建路由集合
# @router.post()	         注册 POST 接口
# @router.get()	             注册 GET 接口
# @router.delete()	         注册 DELETE 接口
# HTTPException	             返回 HTTP 错误
# data: ChatMessage	         使用 Pydantic 模型接收和校验请求
# data.xxx	                 读取对象属性
# list.append()	             向列表末尾添加元素
# return a, b	             函数可以返回多个值
# {session_id}	             动态路径参数
# if not messages	         判断数据是否为空