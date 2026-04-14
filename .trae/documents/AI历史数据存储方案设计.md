# AI 历史数据存储方案设计

## 一、需求分析

### 1.1 当前状态
从代码分析，当前项目存在以下问题：
- **AI对话**：聊天会话数据仅存储在组件状态中，页面刷新后丢失
- **AI生图**：生图历史数据仅存储在组件状态中，页面刷新后丢失
- **会话ID**：虽然 Dify API 返回的 `conversation_id` 保存在 `localStorage`，但没有存储会话列表元数据

### 1.2 用户选中的元素
- `li` - "我的项目"菜单项
- `img` - 项目封面图片
- `div` - AI对话的聊天项（新对话）
- `div` - AI生图的历史记录列表

### 1.3 目标
实现以下功能的数据持久化：
1. **AI对话历史**：存储会话列表、会话ID、消息记录
2. **AI生图历史**：存储生图记录（提示词、图片URL、参数、时间等）
3. **跨会话持久化**：用户在下次登录时能够查看历史数据

---

## 二、数据库设计

### 2.1 现有表结构分析
当前数据库已有以下相关表：

| 表名 | 用途 | 状态 |
|------|------|------|
| `users` | 用户信息 | ✅ 已存在 |
| `projects` | 项目信息 | ✅ 已存在 |
| `chat_messages` | 聊天消息 | ✅ 已存在（含 chat_id） |
| `generation_records` | 图片生成记录 | ✅ 已存在 |

### 2.2 新增表：chat_sessions（聊天会话表）

**创建理由**：需要存储会话元数据（标题、创建时间、选中的AI角色等），而不仅仅是消息内容。

```sql
CREATE TABLE IF NOT EXISTS chat_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    user_id INTEGER NOT NULL,
    conversation_id TEXT,
    title TEXT NOT NULL DEFAULT '新对话',
    selected_people TEXT DEFAULT 'script',
    message_count INTEGER DEFAULT 0,
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

**字段说明**：
- `id`：本地会话ID
- `conversation_id`：Dify API 返回的会话ID（用于续接对话）
- `title`：会话标题（取自第一条消息的前20个字符）
- `selected_people`：当前选中的AI角色（script/character/scene）
- `message_count`：消息数量

---

## 三、API 接口设计

### 3.1 聊天会话 API

#### 3.1.1 获取会话列表
```
GET /api/chat/sessions?project_id=<id>

响应示例：
{
  "status": "success",
  "sessions": [
    {
      "id": 1,
      "conversation_id": "abc123",
      "title": "测试对话",
      "selected_people": "script",
      "message_count": 5,
      "create_time": "2026-04-14 10:00:00",
      "update_time": "2026-04-14 10:30:00"
    }
  ],
  "total": 1
}
```

#### 3.1.2 创建会话
```
POST /api/chat/sessions

请求体：
{
  "project_id": 1,
  "title": "新对话",
  "selected_people": "script"
}

响应示例：
{
  "status": "success",
  "session_id": 2
}
```

#### 3.1.3 更新会话
```
PUT /api/chat/sessions/<id>

请求体：
{
  "title": "更新后的标题",
  "selected_people": "character",
  "conversation_id": "new_conversation_id"
}

响应示例：
{
  "status": "success",
  "message": "会话更新成功"
}
```

#### 3.1.4 删除会话
```
DELETE /api/chat/sessions/<id>

响应示例：
{
  "status": "success",
  "message": "会话已删除"
}
```

#### 3.1.5 获取会话消息
```
GET /api/chat/sessions/<id>/messages

响应示例：
{
  "status": "success",
  "messages": [
    {
      "id": 1,
      "role": "user",
      "content": "你好",
      "time": "2026-04-14 10:00:00"
    },
    {
      "id": 2,
      "role": "assistant",
      "content": "你好，有什么可以帮你的？",
      "time": "2026-04-14 10:00:05"
    }
  ]
}
```

### 3.2 图片生成记录 API（扩展现有接口）

已有 `GET /api/records` 接口，但需要优化以支持前端的历史展示需求。

#### 3.2.1 获取生图历史
```
GET /api/records?project_id=<id>&type=generate&page=1&page_size=20

响应示例：
{
  "status": "success",
  "records": [
    {
      "id": 1,
      "prompt": "一个未来城市的夜景",
      "image_url": "https://...",
      "image_width": 1024,
      "image_height": 1024,
      "model_version": "v4.0",
      "params": {"size": "1024x1024"},
      "create_time": "2026-04-14 10:00:00"
    }
  ],
  "total": 50,
  "page": 1,
  "page_size": 20
}
```

---

## 四、前端实现方案

### 4.1 ProjectDetail.vue 修改

#### 4.1.1 数据加载流程
```javascript
// 初始化时加载历史数据
const loadHistoryData = async () => {
  // 1. 加载聊天会话列表
  await loadChatSessions()
  
  // 2. 加载图片生成历史
  await loadImageHistory()
}

// 加载聊天会话
const loadChatSessions = async () => {
  const response = await fetch(`/api/chat/sessions?project_id=${project.value.id}`)
  const result = await response.json()
  
  if (result.status === 'success') {
    chatList.value = result.sessions.map(session => ({
      id: session.id,
      title: session.title,
      conversationId: session.conversation_id,
      selectedPeople: session.selected_people,
      updateTime: session.update_time,
      messages: []
    }))
    
    // 如果有会话，选中第一个
    if (chatList.value.length > 0) {
      await selectChat(chatList.value[0].id)
    } else {
      // 没有会话时创建新对话
      createNewChat()
    }
  }
}

// 加载图片历史
const loadImageHistory = async () => {
  const response = await fetch(`/api/records?project_id=${project.value.id}&type=generate`)
  const result = await response.json()
  
  if (result.status === 'success') {
    imageHistory.value = result.records.map(record => ({
      id: record.id,
      prompt: record.prompt,
      imageUrl: record.image_url,
      createTime: record.create_time,
      params: JSON.parse(record.params || '{}')
    }))
  }
}
```

#### 4.1.2 创建新对话时保存会话
```javascript
const createNewChat = async () => {
  const newChat = {
    id: Date.now().toString(),
    title: '新对话',
    updateTime: new Date().toLocaleString('zh-CN'),
    messages: [],
    conversationId: ''
  }
  
  try {
    // 保存到后端
    const response = await fetch('/api/chat/sessions', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        project_id: project.value.id,
        title: '新对话',
        selected_people: selectedPeople.value
      })
    })
    
    const result = await response.json()
    if (result.status === 'success') {
      newChat.id = result.session_id.toString()
    }
  } catch (error) {
    console.error('保存会话失败:', error)
  }
  
  chatList.value.unshift(newChat)
  currentChatId.value = newChat.id
}
```

#### 4.1.3 发送消息时更新会话
```javascript
const sendMessage = async () => {
  // ... 发送消息逻辑 ...
  
  // 消息发送成功后，更新会话信息
  const chat = chatList.value.find(c => c.id === currentChatId.value)
  if (chat && chat.conversationId) {
    await fetch(`/api/chat/sessions/${chat.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: message.slice(0, 20) + (message.length > 20 ? '...' : ''),
        conversation_id: chat.conversationId
      })
    })
  }
}
```

#### 4.1.4 生成图片时保存记录
```javascript
const generateImage = async () => {
  // ... 生成图片逻辑 ...
  
  // 图片生成成功后，后端已经保存了记录
  // 前端刷新历史列表
  await loadImageHistory()
}
```

---

## 五、实施计划

### 5.1 第一阶段：后端 API 开发（预计工作量：2小时）

| 任务 | 说明 | 文件 |
|------|------|------|
| 1.1 创建 chat_sessions 表 | 添加数据库表结构 | app.py |
| 1.2 实现会话列表 API | GET /api/chat/sessions | app.py |
| 1.3 实现创建会话 API | POST /api/chat/sessions | app.py |
| 1.4 实现更新会话 API | PUT /api/chat/sessions/<id> | app.py |
| 1.5 实现删除会话 API | DELETE /api/chat/sessions/<id> | app.py |
| 1.6 实现获取会话消息 API | GET /api/chat/sessions/<id>/messages | app.py |

### 5.2 第二阶段：前端集成（预计工作量：3小时）

| 任务 | 说明 | 文件 |
|------|------|------|
| 2.1 修改数据加载逻辑 | 从 API 加载历史数据 | ProjectDetail.vue |
| 2.2 修改创建会话逻辑 | 保存会话到后端 | ProjectDetail.vue |
| 2.3 修改消息发送逻辑 | 更新会话信息 | ProjectDetail.vue |
| 2.4 修改图片生成逻辑 | 后端已保存，前端刷新 | ProjectDetail.vue |
| 2.5 添加加载状态 | 显示加载中效果 | ProjectDetail.vue |
| 2.6 优化错误处理 | 失败重试机制 | ProjectDetail.vue |

### 5.3 第三阶段：测试与优化（预计工作量：1小时）

| 任务 | 说明 |
|------|------|
| 3.1 功能测试 | 测试完整的创建、查看、删除流程 |
| 3.2 数据一致性 | 验证前后端数据同步 |
| 3.3 性能优化 | 大量数据时的分页加载 |

---

## 六、数据流程图

### 6.1 AI对话流程
```
用户进入项目
    ↓
加载聊天会话列表 (GET /api/chat/sessions)
    ↓
显示会话列表 + 加载选中会话消息
    ↓
用户发送消息
    ↓
保存消息到 chat_messages 表 (已有逻辑)
    ↓
更新会话元数据 (PUT /api/chat/sessions/<id>)
    ↓
刷新会话列表显示
```

### 6.2 AI生图流程
```
用户进入生图模块
    ↓
加载生图历史 (GET /api/records)
    ↓
显示历史列表
    ↓
用户生成新图片
    ↓
调用后端生成接口 (已有逻辑)
    ↓
后端保存记录到 generation_records 表 (已有逻辑)
    ↓
前端刷新历史列表
```

---

## 七、注意事项

### 7.1 Dify API 会话 ID
- `conversation_id` 由 Dify API 生成并返回
- 需要保存到本地会话表中，以便续接对话
- 如果 `conversation_id` 为空，说明是新会话

### 7.2 数据同步策略
- **乐观更新**：先更新前端显示，后端异步保存
- **失败回滚**：如果后端保存失败，回滚前端状态

### 7.3 性能考虑
- 会话列表：默认加载最近20个会话
- 历史记录：支持分页加载
- 图片缩略图：使用 URL 参数生成小图

---

## 八、预期效果

实现后，用户将能够：
1. ✅ 在"我的项目"中看到所有历史对话
2. ✅ 点击任意历史对话继续交流
3. ✅ 在"AI生图"中查看所有历史生成的图片
4. ✅ 关闭页面后重新打开，数据依然保留
5. ✅ 切换账号后，各自看到自己的历史数据
