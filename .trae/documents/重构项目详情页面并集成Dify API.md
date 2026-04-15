# 重构项目详情页面并集成Dify API

## 问题分析

### 1. 语法错误问题
**症状**：`SyntaxError: Unexpected token ')'` 错误
**原因**：ProjectDetail.vue 文件中中文字符显示为乱码，导致 JavaScript 解析错误
**示例**：
- "鍒涘缓浜?" → 应该是 "创建于"
- "瀵硅瘽鍒楄〃" → 应该是 "对话列表"
- "AI瀵硅瘽" → 应该是 "AI对话"
- "AI鐢熷浘" → 应该是 "AI生图"

### 2. 当前实现问题
- 使用火山引擎 API（volcengine.js）而非 Dify API
- AI对话、AI生图、AI扩图、AI改图四个模块需要重构

## 解决方案

### 方案概述
使用已部署的 Dify API 服务，集成到前端项目中：
- **AI对话**：使用 `磁力AI对话.yml` 配置，使用对话密钥 `app-jd05GWziMofrIu8sX7FFfLd2`
- **AI生图/扩图/改图**：使用 `磁力AI生图.yml` 配置，使用生图密钥 `app-fJTo6AKTDYgm4yes1yY1lgno`

## 实施步骤

### 步骤1：修复语法错误（优先级：高）
**目标**：修复 ProjectDetail.vue 中的所有中文乱码问题

**具体操作**：
1. 重写整个 ProjectDetail.vue 文件，使用正确的中文编码
2. 修复所有显示为乱码的中文字符串
3. 确保文件使用 UTF-8 编码保存

**受影响的代码段**：
- 第12行：`<span class="project-time">鍒涘缓浜?{{ project.createTime }}</span>`
- 第31行：`<span>AI瀵硅瘽</span>`
- 第42行：`<span>AI鐢熷浘</span>`
- 等等（全部约30+处乱码）

### 步骤2：重构AI对话模块（优先级：高）
**目标**：将AI对话功能改为使用 Dify 流式对话 API

**技术方案**：
1. 使用 fetch API 调用 `/dify-api/chat-messages` 端点
2. 实现流式响应处理，实时显示AI回复
3. 支持多轮对话，使用 conversation_id 维持会话上下文
4. UI保持原有的聊天界面设计

**API调用示例**：
```javascript
POST /dify-api/chat-messages
Authorization: Bearer app-jd05GWziMofrIu8sX7FFfLd2
Content-Type: application/json

{
  "inputs": {},
  "query": "用户输入的消息",
  "response_mode": "streaming",
  "conversation_id": "",
  "user": "user-123"
}
```

**响应处理**：
- 使用 `response.body.getReader()` 读取流式响应
- 解析 SSE 格式数据 `data: {...}`
- 提取 `data.answer` 字段更新UI
- 监听 `data.event === 'message_end'` 结束对话

### 步骤3：重构AI生图模块（优先级：中）
**目标**：将AI生图功能改为使用 Dify API

**技术方案**：
1. 修改参数表单以匹配 Dify 生图API
2. 调用 `/dify-api/chat-messages` 端点
3. 处理图片生成结果
4. 支持预览和下载生成图片

**Dify生图参数**（根据.yml配置）：
- `query`：提示词（必需）
- `size`：图像尺寸（默认 2048x2048）
  - 可选值：1:1 (2048x2048), 4:3 (2304x1728), 3:4 (1728x2304), 16:9 (2560x1440), 9:16 (1440x2560), 3:2 (2496x1664), 2:3 (1664x2496), 21:9 (3024x1296)
- `watermark`：水印（默认 true）
- `model`：模型版本（默认 doubao-seedream-5-0-260128）
  - 可选值：Seedream4.0, Seedream4.5, Seedream5.0 Lite

**返回值**：
- 从 `data.files` 或 `data.answer` 中提取图片URL
- 显示生成的图片列表

### 步骤4：重构AI扩图模块（优先级：中）
**目标**：将AI扩图功能改为使用 Dify API

**技术方案**：
1. 保留图片上传功能
2. 调用 Dify API 处理扩图请求
3. 显示扩图结果

**Dify扩图参数**：
- `query`：扩图描述（可选，默认 "将当前图片扩展为更大尺寸"）
- `input_image_file`：参考图片（必需，通过文件上传）
- `size`：目标尺寸
- `watermark`：水印设置
- `model`：模型版本

### 步骤5：重构AI改图模块（优先级：中）
**目标**：将AI改图功能改为使用 Dify API

**技术方案**：
1. 保留原图上传和蒙版绘制功能
2. 调用 Dify API 处理改图请求
3. 显示改图结果

**Dify改图参数**：
- `query`：修改描述（必需）
- `input_image_file`：原图（必需）
- `size`：图像尺寸
- `watermark`：水印设置
- `model`：模型版本

### 步骤6：测试和调试（优先级：高）
**目标**：确保所有功能正常工作

**测试内容**：
1. AI对话：发送消息，验证流式响应是否正常显示
2. AI生图：输入提示词，验证图片是否正确生成
3. AI扩图：上传图片，验证扩图是否成功
4. AI改图：上传图片+绘制蒙版，验证改图是否成功

**调试要点**：
- 检查浏览器控制台的错误信息
- 验证 API 请求是否正确发送
- 检查响应数据格式是否正确解析

## 技术要点

### 文件编码
- 确保所有 .vue 文件使用 UTF-8 编码保存
- 避免使用 GBK、GB2312 等编码

### API 代理配置
已配置的 vite.config.js：
```javascript
'/dify-api': {
  target: 'https://whhongyi.com.cn',
  changeOrigin: true,
  rewrite: (path) => path.replace(/^\/dify-api/, '/v1')
}
```

### 流式响应处理
```javascript
const reader = response.body.getReader()
const decoder = new TextDecoder()

while (true) {
  const { done, value } = await reader.read()
  if (done) break
  
  const chunk = decoder.decode(value, { stream: true })
  // 解析 SSE 格式数据...
}
```

### 错误处理
- 网络错误
- API 返回错误（如 rate limit、invalid parameters）
- 流式响应解析错误
- 文件上传错误

## 预期成果

1. ✅ 修复所有语法错误，页面正常加载
2. ✅ AI对话功能正常工作，支持流式输出
3. ✅ AI生图功能正常工作，生成指定尺寸的图片
4. ✅ AI扩图功能正常工作，支持参考图片上传
5. ✅ AI改图功能正常工作，支持蒙版编辑
6. ✅ 所有功能使用 Dify API 实现
