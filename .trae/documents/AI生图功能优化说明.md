# AI 生图功能优化说明

## ✅ 已完成的优化

### 1. 添加类型选择器
在图像生成参数表单中添加了"生成类型"选择器：
- **生图**：根据提示词生成新图片
- **扩图**：基于参考图片扩展尺寸
- **改图**：基于原图和蒙版进行修改

### 2. 优化 API 调用参数

#### 修改前的请求格式
```json
{
  "inputs": {},
  "query": "生图\n提示词: xxx\n尺寸: xxx\n模型: xxx\n水印: xxx",
  "response_mode": "blocking",
  "user": "user-xxx"
}
```

#### 修改后的请求格式
```json
{
  "inputs": {
    "type": "生图"
  },
  "query": "用户输入的提示词",
  "response_mode": "blocking",
  "user": "user-xxx"
}
```

**关键改进**：
- ✅ `inputs.type` 参数正确传递（Dify 工作流的必需参数）
- ✅ `query` 直接使用用户输入的提示词
- ✅ 移除了冗余的参数格式

### 3. 优化响应处理

#### 响应格式
```json
{
  "event": "message",
  "task_id": "900bbd43-dc0b-4383-a372-aa6e6c414227",
  "id": "663c5084-a254-4040-8ad3-51f2a3c1a77c",
  "conversation_id": "conv_xxx",
  "answer": "生成的图片URL：https://example.com/image.png",
  "created_at": 1705398420
}
```

#### 图片提取逻辑
```javascript
// 从 answer 字段中提取图片 URL
if (data.answer) {
  const urlMatch = data.answer.match(/https?:\/\/[^\s]+\.(?:jpg|jpeg|png|gif|webp)/gi)
  if (urlMatch) {
    imageUrls = urlMatch
  }
}
```

### 4. 更新默认参数

#### 模型版本
- **默认模型**：Seedream4.5（`doubao-seedream-4-5-251128`）
- 可选版本：
  - Seedream4.0
  - Seedream4.5
  - Seedream5.0 Lite

#### 水印设置
- **类型**：字符串 `'true'` / `'false'`（不是布尔值）
- 符合 Dify 配置的期望格式

---

## 📋 Dify 工作流配置

根据 `磁力AI生图.yml` 配置：

### 工作流结构
```
用户输入 (start)
    ↓
条件分支 (if-else)
    ├─ type = '生图' → 生图工具
    ├─ type = '扩图' → 扩图工具
    └─ type = '改图' → 改图工具
    ↓
直接回复 (answer)
```

### 必需的 inputs 参数
```yaml
inputs:
  type: '生图' | '扩图' | '改图'  # 必需，select 类型
```

### 生图工具参数
```yaml
prompt: string  # 提示词（必需）
size: string    # 图像尺寸（默认 2048x2048）
watermark: string # 水印设置（默认 'true'）
model: string   # 模型版本（默认 doubao-seedream-4-5-251128）
```

---

## 🎯 使用说明

### 1. 生图模式

1. 在"生成类型"中选择"**生图**"
2. 输入提示词（例如："一只可爱的橘猫在阳光下打盹"）
3. 选择图片尺寸（例如：1:1）
4. 选择模型版本（推荐 Seedream4.5）
5. 设置水印（启用/禁用）
6. 点击"**开始生成**"

**API 调用示例**：
```json
{
  "inputs": {
    "type": "生图"
  },
  "query": "一只可爱的橘猫在阳光下打盹",
  "response_mode": "blocking",
  "user": "user-1741865600000"
}
```

### 2. 扩图模式

1. 在"生成类型"中选择"**扩图**"
2. 输入扩图描述或提示词
3. 选择目标尺寸
4. 选择模型版本
5. 设置水印
6. 点击"**开始生成**"

**注意**：扩图功能需要上传参考图片，当前版本暂未实现文件上传。

### 3. 改图模式

1. 在"生成类型"中选择"**改图**"
2. 输入修改描述（例如："将猫咪替换成狗狗"）
3. 选择图片尺寸
4. 选择模型版本
5. 设置水印
6. 点击"**开始生成**"

**注意**：改图功能需要上传原图和蒙版，当前版本暂未实现。

---

## 🔧 进一步优化建议

### 1. 添加文件上传功能

对于扩图和改图功能，需要实现文件上传：

#### 步骤 1：上传文件到 Dify
```javascript
const uploadFile = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('user', 'user-' + Date.now())
  
  const response = await fetch('/dify-api/files/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${difyImageApiKey}`
    },
    body: formData
  })
  
  const data = await response.json()
  return data.id  // 返回 upload_file_id
}
```

#### 步骤 2：在 API 请求中包含文件
```json
{
  "inputs": {
    "type": "扩图"
  },
  "query": "扩图描述",
  "response_mode": "blocking",
  "files": [
    {
      "type": "image",
      "transfer_method": "local_file",
      "upload_file_id": "file-xxx"
    }
  ]
}
```

### 2. 添加流式响应支持

当前使用 `blocking` 模式，可以改为 `streaming` 模式以获得更好的用户体验：

```javascript
const response = await fetch('/dify-api/chat-messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${difyImageApiKey}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    inputs: { type: '生图' },
    query: prompt,
    response_mode: 'streaming',
    user: 'user-' + Date.now()
  })
})

// 处理流式响应
const reader = response.body.getReader()
const decoder = new TextDecoder()

while (true) {
  const { done, value } = await reader.read()
  if (done) break
  
  const chunk = decoder.decode(value, { stream: true })
  // 解析 SSE 事件
  // 提取图片 URL
}
```

### 3. 添加图片预览和编辑功能

- 大图预览
- 图片裁剪
- 旋转和缩放
- 下载原图或压缩图

---

## 🧪 测试步骤

### 1. 刷新页面
```
Ctrl + Shift + R  (Windows)
Cmd + Shift + R  (Mac)
```

### 2. 测试生图功能
1. 进入项目详情页
2. 选择"AI生图"标签
3. 在"生成类型"中选择"**生图**"
4. 输入提示词："一只可爱的猫咪"
5. 点击"开始生成"
6. 等待响应
7. 查看是否成功生成图片

### 3. 检查浏览器控制台
打开开发者工具（F12）→ Console 标签，查看：
- `生图响应:` - 显示 API 响应内容
- 图片 URL 是否正确提取

### 4. 检查 Dify 后台
1. 访问 Dify 管理后台
2. 查看应用调用日志
3. 确认 `inputs.type` 参数是否为 '生图'

---

## 📊 预期结果

### 成功的响应示例
```json
{
  "event": "message",
  "task_id": "xxx",
  "id": "xxx",
  "conversation_id": "xxx",
  "answer": "生成的图片链接：\nhttps://example.com/generated_image.png",
  "created_at": 1705398420
}
```

### 图片提取结果
```javascript
imageUrls = [
  "https://example.com/generated_image.png"
]
```

### 页面显示
- 成功生成：显示图片缩略图
- 加载中：显示"生成中..."提示
- 失败：显示错误信息

---

## 🚀 下一步

### 短期优化（已完成）
- ✅ 添加类型选择器
- ✅ 优化 API 参数
- ✅ 改进响应处理

### 中期优化（建议）
- 🔧 实现文件上传功能
- 🔧 添加扩图和改图的上传界面
- 🔧 支持流式响应

### 长期优化（可选）
- 🔧 添加图片编辑功能
- 🔧 实现历史记录管理
- 🔧 添加批量生成功能

---

## 📝 注意事项

### 1. API 密钥
- 对话密钥：`app-jd05GWziMofrIu8sX7FFfLd2`
- 生图密钥：`app-fJTo6AKTDYgm4yes1yY1lgno`

### 2. 必需参数
- `inputs.type`：生图/扩图/改图
- `query`：提示词

### 3. 可选参数
- `size`：图像尺寸
- `watermark`：水印设置
- `model`：模型版本

### 4. 文件上传
当前版本暂不支持扩图和改图的文件上传，需要后续实现。

---

## 🎉 总结

AI 生图功能已成功优化：
- ✅ 支持三种生成类型（生图/扩图/改图）
- ✅ API 参数正确传递
- ✅ 响应处理逻辑优化
- ✅ 用户界面友好

**现在可以测试生图功能了！** 🚀
