import json

from fastapi import HTTPException
from openai import OpenAI

from app.core.config import settings

SYSTEM_PROMPT = """
你是一个专业的 Python 学习助手。

请根据用户的要求制定学习计划。
必须返回标准 JSON 格式，不能添加额外解释。

JSON 必须包含：
title：计划标题
days：学习天数
tasks：每天的学习任务，使用列表表示
"""


def chat_with_ai(messages):
    if not settings.api_key:
        raise HTTPException(status_code=500, detail="未配置 DEEPSEEK_API_KEY，请填写 .env 文件")

    client = OpenAI(api_key=settings.api_key, base_url=settings.base_url)
    # 你可以把 client 理解为一个专门负责与 AI 服务通信的工具。
    try:
        # 这是 OpenAI 兼容 SDK 的聊天补全接口。
        response = client.chat.completions.create(
            model=settings.model,#使用哪个模型
            messages=[{"role": "system", "content": SYSTEM_PROMPT}, *messages],#发送给模型的消息，
            #messages是发送给模型的消息，*messages是列表解包（会把原列表中的元素逐个展开到新列表中）。
            max_tokens=1500,#限制模型最多生成多少token
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 请求失败：{str(e)}")

    raw_reply = response.choices[0].message.content or ""#获取AI返回的内容
    try:
        ai_reply = json.loads(raw_reply) #json.loads：把 JSON 字符串变成 Python 字典
    except (json.JSONDecodeError, TypeError):
        ai_reply = {"error": "AI 返回的内容不是合法 JSON", "raw_reply": raw_reply}
    return ai_reply, raw_reply
    # ai_reply	解析后的 Python 对象	方便程序读取和处理
    # raw_reply	AI 原始回复字符串	    保留原始数据
    # response：整个 API 响应对象。
    # choices：模型返回的候选结果列表。
    # [0]：取第一个候选结果。
    # message：这个候选结果中的消息。
    # content：消息的具体文本内容。