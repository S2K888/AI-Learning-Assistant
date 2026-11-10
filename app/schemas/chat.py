from pydantic import BaseModel

class ChatMessage(BaseModel):# 这里定义了一个 Python 类，名字叫 ChatMessage。它继承了 BaseModel。
    session_id: str
    message: str

# Pydantic 是 Python 中非常常用的数据校验库。
# 它主要帮助我们：
# - 定义数据应该包含哪些字段。
# - 定义每个字段的数据类型。
# - 自动检查用户传入的数据是否符合要求。
# BaseModel 是用来定义数据格式和规则的。