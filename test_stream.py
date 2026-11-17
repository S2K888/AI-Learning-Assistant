
import requests
import json

url = "http://127.0.0.1:8000/chat/stream"

data = {
    "session_id": "stream001",
    "message": "请介绍一下 Python 的三个主要特点"
}

response = requests.post(
    url,
    json=data,
    stream=True
)

for line in response.iter_lines(decode_unicode=True):
    if line:
        if isinstance(line, bytes):
            line = line.decode("utf-8")

        if line.startswith("data: "):
            content = line[6:]

            if content == "[DONE]":
                print("\nAI 回复结束")
                break

            result = json.loads(content)
            print(result["content"], end="", flush=True)
