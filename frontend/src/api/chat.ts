// api：通常存放前端请求后端接口的代码。
// chat.ts：专门负责聊天相关的 API 请求。


export interface ChatRequest {
  session_id: string
  message: string
}

export async function streamChat(
  data: ChatRequest,
  onChunk: (content: string) => void
): Promise<void> {
  // 1. 发送请求
  const response = await fetch('/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })

  // 2. 检查请求是否成功
  if (!response.ok) {
    throw new Error(`请求失败：${response.status}`)
  }

  if (!response.body) {
    throw new Error('响应体不存在')
  }

  // 3. 获取读取器和解码器
  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')

  let buffer = ''

  try {
    // 4. 持续读取数据
    while (true) {
      const { value, done } = await reader.read()

      if (done) {
        buffer += decoder.decode()
        break
      }

      const text = decoder.decode(value, { stream: true })
      buffer += text

      // 5. 解析完整 SSE 消息
      while (buffer.includes('\n\n')) {
        const boundary = buffer.indexOf('\n\n')
        const message = buffer.slice(0, boundary)

        buffer = buffer.slice(boundary + 2)

        if (!message.startsWith('data:')) continue

        const content = message.slice(5).trimStart()

        if (content === '[DONE]') return

        const result: { content: string } = JSON.parse(content)

        // 6. 将 AI 内容交给调用者
        onChunk(result.content)
      }
    }
  } finally {
    reader.releaseLock()
  }
}
