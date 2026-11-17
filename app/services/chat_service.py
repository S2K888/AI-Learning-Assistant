
from fastapi import HTTPException
from openai import OpenAI

from app.core.config import settings


SYSTEM_PROMPT = """
你是一个专业、友好的 AI 智能学习助手。

你的主要任务是帮助用户学习编程、理解技术知识、解决开发问题和制定学习计划。

回答要求：

1. 根据用户的问题直接回答，不要强制生成学习计划。
2. 使用清晰、自然的 Markdown 格式组织回答。
3. 合理使用标题、加粗、列表和代码块。
4. 涉及代码时，使用 Markdown 代码块，并标注语言。
5. 回答尽量简洁、易懂，避免不必要的重复。
6. 只有用户明确要求制定学习计划时，才生成学习计划。
7. 除非用户明确要求 JSON，否则不要输出 JSON 格式。
"""


def chat_with_ai(messages):
    if not settings.api_key:
        raise HTTPException(
            status_code=500,
            detail="未配置 DEEPSEEK_API_KEY，请填写 .env 文件"
        )

    client = OpenAI(
        api_key=settings.api_key,
        base_url=settings.base_url
    )

    try:
        response = client.chat.completions.create(
            model=settings.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            max_tokens=1500,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI 请求失败：{str(e)}"
        )

    raw_reply = response.choices[0].message.content or ""

    return raw_reply, raw_reply


def chat_with_ai_stream(messages):
    if not settings.api_key:
        raise HTTPException(
            status_code=500,
            detail="未配置 DEEPSEEK_API_KEY，请填写 .env 文件"
        )

    client = OpenAI(
        api_key=settings.api_key,
        base_url=settings.base_url
    )

    try:
        stream = client.chat.completions.create(
            model=settings.model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *messages
            ],
            max_tokens=1500,
            stream=True,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"AI 请求失败：{str(e)}"
        )

    for chunk in stream:
        content = chunk.choices[0].delta.content

        if content:
            yield content
