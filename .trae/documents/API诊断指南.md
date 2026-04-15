# API 调用诊断指南

## 🔍 问题诊断

### 当前错误
```
[error] 解析响应数据失败: SyntaxError: Expected property name or '}' in JSON at position 1 (line 1 column 2)
[error] net::ERR_ABORTED http://localhost:5001/dify-api/chat-messages
```

### 可能原因

1. **API 返回了错误信息**（不是 JSON 格式）
2. **代理配置问题**（请求未正确转发到 Dify）
3. **CORS 跨域问题**
4. **API 密钥无效或过期**
5. **请求格式不符合 Dify API 规范**

## 📝 查看详细错误日志

### 步骤 1：打开浏览器开发者工具
1. 按 `F12` 打开开发者工具
2. 切换到 **Console（控制台）** 标签
3. 清空控制台（点击🗑️图标）

### 步骤 2：发送测试消息
1. 在 AI 对话输入框中输入：`你好`
2. 点击发送按钮
3. 查看控制台输出的详细日志

### 步骤 3：分析日志

请将以下日志信息分享给我：

```
1. "发送请求到 Dify API:" - 显示请求信息
2. "Dify API 响应状态:" - 显示HTTP状态码
3. "响应头:" - 显示响应头信息
4. "接收到数据块:" - 显示实际返回的数据
5. "API错误响应:" - 如果有错误，显示错误详情
```

## 🔧 快速排查清单

### ✅ 检查 1：网络连接
```bash
ping whhongyi.com.cn
```
- 如果 ping 失败 → 检查网络连接

### ✅ 检查 2：API 服务状态
访问：https://whhongyi.com.cn/v1/chat-messages
- 应该返回 405 Method Not Allowed 或其他 API 响应
- 如果连接超时 → 服务可能不可用

### ✅ 检查 3：代理配置
确认 vite.config.js 中的代理配置：
```javascript
'/dify-api': {
  target: 'https://whhongyi.com.cn',
  changeOrigin: true,
  rewrite: (path) => path.replace(/^\/dify-api/, '/v1')
}
```

### ✅ 检查 4：API 密钥
确认密钥格式正确：
- 对话密钥：`app-jd05GWziMofrIu8sX7FFfLd2`
- 生图密钥：`app-fJTo6AKTDYgm4yes1yY1lgno`

## 📋 常见错误及解决方案

### 错误 1：ERR_ABORTED
**原因**：请求被中止，通常是网络问题或服务器无响应

**解决**：
1. 检查网络连接
2. 确认 Dify 服务正在运行
3. 检查浏览器控制台的网络请求，看是否有 CORS 错误

### 错误 2：JSON 解析失败
**原因**：API 返回的不是 JSON 格式

**解决**：
1. 查看控制台的 "接收到数据块:" 日志
2. 如果显示 HTML 或其他文本 → 检查代理配置
3. 如果显示 `{"code": xxx, "message": "xxx"}` → 这是 API 返回的错误

### 错误 3：CORS 错误
**原因**：跨域请求被阻止

**解决**：
1. 检查浏览器控制台是否有 CORS 错误
2. 确认 Dify 服务配置了正确的 CORS 头
3. 如果无法解决，可能需要后端配置代理

## 🧪 测试 API 直连

### 使用 curl 测试
```bash
curl -X POST 'https://whhongyi.com.cn/v1/chat-messages' \
  -H 'Authorization: Bearer app-jd05GWziMofrIu8sX7FFfLd2' \
  -H 'Content-Type: application/json' \
  -d '{
    "inputs": {},
    "query": "你好",
    "response_mode": "blocking",
    "user": "test-user"
  }'
```

**请将 curl 命令的输出分享给我**

## 📊 需要您提供的信息

为了更好地诊断问题，请提供：

1. **浏览器控制台的完整日志**（步骤 2 中的所有日志）
2. **curl 测试的输出**（如果可以运行）
3. **您是否能看到任何网络请求**（在 Network 标签中）
4. **是否看到 CORS 错误**（在 Console 或 Network 标签中）

## 🔄 下一步

1. **请先刷新页面**（Ctrl + Shift + R）
2. **重新发送消息**并观察控制台日志
3. **将控制台中以 `发送请求`、`Dify API`、`接收到数据块` 开头的日志复制给我**

我会根据日志信息进一步诊断问题！ 🚀
