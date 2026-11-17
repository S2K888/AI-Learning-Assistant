<script setup lang="ts">
import { ref } from "vue";
import { streamChat } from "@/api/chat";
import {marked} from 'marked'
import DOMPurify from 'dompurify'

//消息类型
interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
}

//聊天信息
const messages = ref<Message[]>([
  {
    id: 1,
    role: 'assistant',
    content: '你好，我是AI Learning Assistant，有什么学习问题可以问我。'
  }
]);

//输入框内容
const input = ref('');
const isLoading = ref(false)

//消息ID
let nextId = 2;


// 将 Markdown 转换成安全的 HTML
function renderMarkdown(content: string): string {
  const html = marked.parse(content, {
    async: false,
    gfm: true,
    breaks: true
  })

  return DOMPurify.sanitize(html)
}
//发送消息

async function sendMessage() {
  const content = input.value.trim()

  if (!content || isLoading.value) return

  // 1. 添加用户消息
  messages.value.push({
    id: nextId++,
    role: 'user',
    content
  })

  // 2. 创建一条空的 AI 消息
  const assistantId = nextId++

  messages.value.push({
    id: assistantId,
    role: 'assistant',
    content: ''
  })

  // 3. 清空输入框
  input.value = ''

  // 4. 开始加载
  isLoading.value = true

  try {
    // 5. 请求后端 SSE 接口
    await streamChat(
      {
        session_id: 'session001',
        message: content
      },
      (chunk) => {
        // 6. 找到刚才创建的 AI 消息
        const assistantMessage = messages.value.find(
          item => item.id === assistantId
        )

        // 7. 追加 AI 返回的内容
        if (assistantMessage) {
          assistantMessage.content += chunk
        }
      }
    )
  } catch (error) {
    console.error('AI 请求失败：', error)

    const assistantMessage = messages.value.find(
      item => item.id === assistantId
    )

    if (assistantMessage) {
      assistantMessage.content = '请求失败，请稍后重试。'
    }
  } finally {
    // 8. 无论成功还是失败，都结束加载状态
    isLoading.value = false
  }
}

</script>

<template>
   <div class="chat-container">

    <!-- 顶部导航 -->
    <header class="chat-header">
      <h2>AI Learning Assistant</h2>
      <span>智能学习助手</span>
    </header>

    <!-- 聊天消息区域 -->
    <main class="chat-messages">
      <div
        v-for="message in messages"
        :key="message.id"
        class="message-row"
        :class="message.role"
      >
        <div
  class="message-bubble"
  v-html="renderMarkdown(message.content)"
></div>
      </div>
    </main>

    <!-- 输入区域 -->
    <form class="chat-input-area" @submit.prevent="sendMessage">
      <textarea
        v-model="input"
        placeholder="输入你想学习的问题..."
        rows="2"
        @keydown.enter.exact.prevent="sendMessage"
      ></textarea>

      <button
  type="submit"
  :disabled="!input.trim() || isLoading"
>
  {{ isLoading ? 'AI 正在回复...' : '发送' }}
</button>
    </form>

  </div>
</template>


<style scoped>
.chat-container {
  width: min(900px, calc(100% - 32px));
  height: calc(100vh - 40px);
  margin: 20px auto;
  display: flex;
  flex-direction: column;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
}

.chat-header {
  padding: 20px 24px;
  background: white;
  border-bottom: 1px solid #e2e8f0;
}

.chat-header h2 {
  margin: 0;
  font-size: 20px;
}

.chat-header span {
  color: #64748b;
  font-size: 13px;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.message-row {
  display: flex;
}

.message-row.user {
  justify-content: flex-end;
}

.message-row.assistant {
  justify-content: flex-start;
}

.message-bubble {
  max-width: 75%;
  padding: 12px 16px;
  border-radius: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}


/* AI 和用户消息统一左对齐 */
.message-bubble {
  text-align: left;
  line-height: 1.75;
  overflow-wrap: anywhere;
}

/* 标题 */
.message-bubble :deep(h1),
.message-bubble :deep(h2),
.message-bubble :deep(h3) {
  margin: 16px 0 10px;
  font-weight: 700;
  line-height: 1.4;
}

/* 段落 */
.message-bubble :deep(p) {
  margin: 8px 0;
}

/* 列表 */
.message-bubble :deep(ul),
.message-bubble :deep(ol) {
  padding-left: 24px;
  margin: 10px 0;
}

/* 代码块 */
.message-bubble :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 14px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 12px 0;
}

/* 行内代码 */
.message-bubble :deep(code) {
  background: #f1f5f9;
  color: #db2777;
  padding: 2px 5px;
  border-radius: 4px;
}

/* 代码块内部不要使用行内代码样式 */
.message-bubble :deep(pre code) {
  background: transparent;
  color: inherit;
  padding: 0;
}

/* 引用 */
.message-bubble :deep(blockquote) {
  border-left: 3px solid #94a3b8;
  padding-left: 12px;
  margin: 12px 0;
  color: #64748b;
}

/* 表格 */
.message-bubble :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
}

.message-bubble :deep(th),
.message-bubble :deep(td) {
  border: 1px solid #e2e8f0;
  padding: 8px;
  text-align: left;
}


.user .message-bubble {
  background: #2563eb;
  color: white;
}

.assistant .message-bubble {
  background: white;
  border: 1px solid #e2e8f0;
  color: #1e293b;
}

.chat-input-area {
  display: flex;
  gap: 12px;
  padding: 18px 24px;
  background: white;
  border-top: 1px solid #e2e8f0;
}

.chat-input-area textarea {
  flex: 1;
  resize: none;
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  outline: none;
  font: inherit;
}

.chat-input-area textarea:focus {
  border-color: #2563eb;
}

.chat-input-area button {
  padding: 0 22px;
  border: none;
  border-radius: 10px;
  background: #2563eb;
  color: white;
  cursor: pointer;
}

.chat-input-area button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}
</style>
