# Dify API 对话功能接入文档

## 📌 概述

本文档详细记录了如何在 `ciliAI` 项目中接入 Dify 工作流编排的对话型应用 API，实现流式对话功能。

---

## 🔧 一、API 基本配置

### 1.1 API 基础信息

```javascript
// 文件位置: src/views/ProjectDetail.vue
const difyApiKey = 'app-jd05GWziMofrIu8sX7FFfLd2'
const difyApiUrl = '/dify-api/chat-messages'
```

| 配置项 | 值 | 说明 |
|--------|-----|------|
| **API 基础 URL** | `https://whhongyi.com.cn/v1` | Dify 服务器地址 |
| **完整端点** | `/v1/chat-messages` | 发送对话消息的接口 |
| **API 密钥** | `app-jd05GWziMofrIu8sX7FFfLd2` | 应用访问凭证 |
| **认证方式** | Bearer Token | 在 Authorization Header 中传递 |

### 1.2 Vite 代理配置

```javascript
// 文件位置: vite.config.js
proxy: {
  '/dify-api': {
    target: 'https://whhongyi.com.cn',
    changeOrigin: true,
    rewrite: (path) => path.replace(/^\/dify-api/, '/v1'),
    secure: false,
    timeout: 180000  // 3分钟超时，支持长对话
  }
}
```

**作用说明**：
- 前端使用 `/dify-api/chat-messages` 发送请求
- Vite 代理自动转发到 `https://whhongyi.com.cn/v1/chat-messages`
- 避免跨域问题

---

## 📊 二、参数映射与配置

### 2.1 people 参数映射

Dify 工作流定义了 3 个角色，通过 `people` 变量选择：

```javascript
// 文件位置: src/views/ProjectDetail.vue

// 界面显示标签
const peopleLabels = {
  script: '剧本设计',
  character: '人设设计',
  scene: '场景设计'
}

// 传递给 Dify API 的值（字符串类型）
const peopleValues = {
  script: '1',    // 剧本设计
  character: '2',  // 人设设计
  scene: '3'      // 场景设计
}

// 当前选择的角色
const selectedPeople = ref('script')
```

### 2.2 Dify 工作流配置（参考）

```yaml
# 文件位置: 磁力AI对话.yml

# 用户输入节点定义
variables:
  - label: people
    type: select
    options:
      - '1'    # 剧本设计
      - '2'    # 人设设计
      - '3'    # 场景设计
    required: true

# 条件分支节点
cases:
  - conditions:
      - comparison_operator: contains
        value: '1'
        variable_selector: [1776059724557, people]
    # 连接到对应的 LLM 节点

  - conditions:
      - comparison_operator: contains
        value: '2'
        variable_selector: [1776059724557, people]
    # 连接到对应的 LLM 节点

  - conditions:
      - comparison_operator: contains
        value: '3'
        variable_selector: [1776059724557, people]
    # 连接到对应的 LLM 节点
```

---

## 🌊 三、流式响应实现

### 3.1 请求体构造

```javascript
const requestBody = {
  inputs: {
    people: peopleValues[people] || '1'  // 角色参数
  },
  query: query,                          // 用户输入
  response_mode: 'streaming',             // 流式响应模式
  user: userId,                          // 用户标识
  files: []                              // 文件列表（暂不使用）
}
```

### 3.2 流式响应处理

```javascript
// 文件位置: src/views/ProjectDetail.vue - callDifyAPI 函数

const reader = response.body.getReader()
const decoder = new TextDecoder()
let result = ''
let newConversationId = conversationId

// 逐块读取响应
while (!isCompleted) {
  const { done, value } = await reader.read()
  if (done) break

  // 解码数据块
  const chunk = decoder.decode(value, { stream: true })
  const lines = chunk.split('\n')

  for (const line of lines) {
    if (line.startsWith('data: ')) {
      const data = JSON.parse(line.slice(6))

      // 处理文本块事件
      if (data.event === 'message' || data.event === 'agent_message') {
        const answerText = data.answer || ''
        result += answerText

        // 实时更新 UI
        if (onChunk) {
          onChunk(answerText, data.conversation_id)
        }
      }

      // 处理消息结束事件
      if (data.event === 'message_end') {
        isCompleted = true
        return { answer: result, conversationId: newConversationId }
      }
    }
  }
}
```

### 3.3 响应事件类型

根据 Dify API 文档，主要事件类型：

| 事件 | 说明 | 关键字段 |
|------|------|---------|
| `message` | LLM 返回文本块 | `answer`, `conversation_id` |
| `agent_message` | Agent 消息块 | `answer`, `conversation_id` |
| `message_end` | 消息结束 | `conversation_id`, `usage`, `metadata` |
| `message_file` | 文件事件 | `id`, `type`, `url` |
| `error` | 错误事件 | `message`, `code` |

---

## 🔌 四、完整调用流程

### 4.1 前端调用入口

```javascript
// 文件位置: src/views/ProjectDetail.vue - sendMessage 函数

const sendMessage = async () => {
  const message = inputMessage.value.trim()
  if (!message) return

  // 1. 创建用户消息
  const userMessage = {
    id: Date.now().toString(),
    role: 'user',
    content: message,
    time: new Date().toLocaleTimeString()
  }

  // 2. 添加到聊天列表
  const chat = chatList.value.find(c => c.id === currentChatId.value)
  if (chat) {
    chat.messages.push(userMessage)
  }

  // 3. 创建 AI 消息占位
  const aiMessageId = (Date.now() + 1).toString()
  const aiMessage = {
    id: aiMessageId,
    role: 'assistant',
    content: '',
    status: 'sending'
  }
  chat.messages.push(aiMessage)

  // 4. 调用 Dify API
  try {
    const { answer, conversationId } = await callDifyAPI(
      message,
      chat.conversationId,
      selectedPeople.value,
      (chunk, receivedConversationId) => {
        // 流式更新 UI
        const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
        if (msgIndex > -1) {
          chat.messages[msgIndex].content += chunk
        }
      }
    )

    // 5. 保存会话 ID（用于多轮对话）
    if (conversationId) {
      chat.conversationId = conversationId
      localStorage.setItem('currentConversationId', conversationId)
    }
  } catch (error) {
    console.error('发送消息失败:', error)
  }
}
```

### 4.2 核心 API 调用函数

```javascript
// 文件位置: src/views/ProjectDetail.vue - callDifyAPI 函数

const callDifyAPI = async (query, conversationId, people, onChunk) => {
  const controller = new AbortController()
  const timeout = setTimeout(() => controller.abort(), 180000)

  const userId = localStorage.getItem('userId') || `user-${Date.now()}`

  // 构造请求体
  const requestBody = {
    inputs: {
      people: peopleValues[people] || '1'
    },
    query: query,
    response_mode: 'streaming',
    user: userId,
    files: []
  }

  // 添加会话 ID（支持多轮对话）
  if (conversationId) {
    requestBody.conversation_id = conversationId
  }

  // 发送请求
  const response = await fetch(difyApiUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${difyApiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody),
    signal: controller.signal
  })

  if (!response.ok) {
    throw new Error(`API请求失败 (${response.status})`)
  }

  // 处理流式响应
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let result = ''
  let newConversationId = conversationId

  // ... 流式处理逻辑（见 3.2 节）

  return { answer: result, conversationId: newConversationId }
}
```

---

## 🧪 五、测试方法

### 5.1 独立测试页面

创建了独立的测试工具页面：

```bash
文件路径: test-api.html
打开方式: 直接在浏览器中打开
功能:
  ✅ 直连 Dify API
  ✅ 可视化配置
  ✅ 实时日志输出
  ✅ 流式响应展示
  ✅ 一键选择角色
```

**使用方法**：
1. 打开 `test-api.html`
2. 点击"发送测试"按钮
3. 查看响应结果

### 5.2 浏览器控制台测试

在页面加载后，会自动注册测试方法：

```javascript
// 在浏览器控制台输入
window.testDifyAPI()
```

会输出详细的请求和响应日志。

### 5.3 查看日志

打开浏览器开发者工具 (F12) → Console 标签，应看到：

```
========== Dify API 请求开始 ==========
发送的消息详情: {
  query: "测试消息",
  people: "1",
  selectedPeople: "script",
  conversationId: "(新建会话)",
  user: "user-xxx"
}
=====================================

========== Dify API 响应 ==========
Dify API 响应状态: 200 OK
响应头 Content-Type: text/event-stream
===================================

收到事件: message {...}
收到事件: message_end {...}

========== 流式响应结束 ==========
最终回复: AI的回复内容
会话ID: conv-xxx
==================================
```

---

## 📝 六、关键代码位置

| 功能 | 文件 | 行数 |
|------|------|------|
| API 配置常量 | `src/views/ProjectDetail.vue` | 574-575 |
| people 映射 | `src/views/ProjectDetail.vue` | 583-592 |
| 发送消息入口 | `src/views/ProjectDetail.vue` | 790-839 |
| API 调用核心 | `src/views/ProjectDetail.vue` | 897-1070 |
| 流式响应处理 | `src/views/ProjectDetail.vue` | 1001-1065 |
| 测试方法注册 | `src/views/ProjectDetail.vue` | 1493-1575 |
| Vite 代理配置 | `vite.config.js` | 14-19 |

---

## ✅ 七、注意事项

### 7.1 重要配置点

1. **people 参数类型**：必须是字符串 `'1'`, `'2'`, `'3'`，不能是数字
2. **response_mode**：必须使用 `'streaming'` 启用流式响应
3. **超时时间**：设置 180 秒（3分钟），支持长对话
4. **会话 ID**：首次请求不传 `conversation_id`，后续请求需要传递以保持上下文

### 7.2 错误处理

- 网络连接失败
- API 返回错误状态码
- 流式响应中断
- 会话过期（conversation_id 无效）

### 7.3 性能优化

- 使用 `AbortController` 支持请求取消
- 流式响应实时更新 UI
- 本地存储会话 ID 支持页面刷新后继续对话

---

## 🎯 八、快速参考

### API 调用示例

```bash
POST https://whhongyi.com.cn/v1/chat-messages

Headers:
  Authorization: Bearer app-jd05GWziMofrIu8sX7FFfLd2
  Content-Type: application/json

Body:
{
  "inputs": {
    "people": "1"  # 剧本设计
  },
  "query": "帮我写一个开场白",
  "response_mode": "streaming",
  "user": "user-123",
  "files": []
}
```

### 参数速查表

| 角色 | people 值 | 说明 |
|------|----------|------|
| 剧本设计 | `'1'` | 触发剧本设计 LLM |
| 人设设计 | `'2'` | 触发人设设计 LLM |
| 场景设计 | `'3'` | 触发场景设计 LLM |

---

## 📚 九、相关资源

- **Dify 官方文档**: https://docs.dify.ai/
- **接口文档**: 工作流编排对话型应用 API
- **测试页面**: `test-api.html`

---

**文档版本**: v1.0  
**最后更新**: 2026-04-13  
**维护人**: AI Assistant
