# Dify API people 参数修复说明

## 🔍 问题原因

根据您提供的 `磁力AI对话.yml` 配置文件，发现了一个关键问题：

### 配置中的变量定义
```yaml
variables:
  - label: people
    variable: people
    type: select
    required: true
    options:
      - '1'
      - '2'
      - '3'
```

### 问题
- **people** 是一个**必需的 select 参数**
- 但之前的代码中 `inputs: {}` 是**空对象**
- **没有传递 people 参数**，导致 Dify 后端无法处理请求

### 为什么 Dify 后台看不到调用记录？
因为请求缺少必需参数，Dify 服务可能在解析阶段就拒绝了请求，所以没有记录到调用日志。

---

## ✅ 修复内容

### 1. 添加 people 参数到 API 请求

**修改前**：
```javascript
const requestBody = {
  inputs: {},  // ❌ 空对象，缺少必需参数
  query: query,
  response_mode: 'streaming',
  user: 'user-' + Date.now()
}
```

**修改后**：
```javascript
const requestBody = {
  inputs: {
    people: peopleValue  // ✅ 传递必需的 people 参数
  },
  query: query,
  response_mode: 'streaming',
  user: 'user-' + Date.now()
}
```

### 2. 添加用户界面选择器

在聊天输入区域上方添加了角色选择器：

```vue
<div class="people-selector">
  <label>选择角色：</label>
  <el-select v-model="selectedPeople" placeholder="选择角色" size="small">
    <el-option label="角色 1" value="1" />
    <el-option label="角色 2" value="2" />
    <el-option label="角色 3" value="3" />
  </el-select>
</div>
```

### 3. 添加样式美化

新增了 `.people-selector` 的样式：
- 暗色主题配色
- 悬停效果
- 圆角设计
- 统一的字体大小

---

## 📋 API 请求格式

### 完整的请求体示例
```json
{
  "inputs": {
    "people": "1"
  },
  "query": "你好，请帮我设计一个剧本",
  "response_mode": "streaming",
  "conversation_id": "",
  "user": "user-1741862400000"
}
```

### 参数说明

| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| inputs | object | ✅ | 应用变量 |
| inputs.people | string | ✅ | 角色选择：'1', '2', '3' |
| query | string | ✅ | 用户输入的消息 |
| response_mode | string | ✅ | 响应模式：'streaming' |
| user | string | ✅ | 用户标识 |

---

## 🧪 测试步骤

### 1. 刷新页面
```
Ctrl + Shift + R  (Windows)
Cmd + Shift + R  (Mac)
```

### 2. 查看界面变化
- 在 AI 对话输入区域上方
- 应该看到"**选择角色**"下拉框
- 默认选中"**角色 1**"

### 3. 发送测试消息
1. 选择一个角色（例如：角色 2）
2. 在输入框中输入："你好"
3. 点击发送按钮

### 4. 检查 Dify 后台
1. 访问 Dify 管理后台
2. 查看调用日志
3. **应该能看到调用记录**
4. **inputs.people 的值应该是 '2'**

---

## 📊 预期结果

### 浏览器控制台日志
```
发送请求到 Dify API: {
  url: "/dify-api/chat-messages",
  body: {
    inputs: {
      people: "2"  // ✅ 正确传递
    },
    query: "你好",
    response_mode: "streaming",
    user: "user-1741862400000"
  }
}
```

### Dify 后台调用记录
应该显示：
- **inputs.people**: '2'（或您选择的值）
- **query**: 您的输入消息
- **状态**: 成功或进行中

---

## 🔍 工作流对应关系

根据 `磁力AI对话.yml` 配置，`people` 参数对应不同的分支：

| people 值 | 触发的工作流分支 | 说明 |
|-----------|----------------|------|
| '1' | true 分支 | 角色1的工作流 |
| '2' | e3489c3b 分支 | 角色2的工作流 |
| '3' | a54daa67 分支 | 角色3的工作流 |

### 工作流配置
```yaml
cases:
  - case_id: 'true'
    conditions:
      - comparison_operator: contains
        value: '1'
        variable_selector:
          - '1776059724557'
          - people
  - case_id: e3489c3b...
    conditions:
      - comparison_operator: contains
        value: '2'
        ...
  - case_id: a54daa67...
    conditions:
      - comparison_operator: contains
        value: '3'
        ...
```

---

## 🚀 进一步测试

### 测试不同角色
1. **测试角色 1**：
   - 选择"角色 1"
   - 发送消息："我是角色1"
   - 确认触发正确的分支

2. **测试角色 2**：
   - 选择"角色 2"
   - 发送消息："我是角色2"
   - 确认触发正确的分支

3. **测试角色 3**：
   - 选择"角色 3"
   - 发送消息："我是角色3"
   - 确认触发正确的分支

### 检查响应差异
不同角色应该：
- 有不同的系统提示词（根据工作流配置）
- 不同的对话风格
- 不同的响应内容

---

## 📝 注意事项

### 1. people 参数必须提供
- 这是 Dify 应用配置的必需参数
- 如果不提供，Dify 会拒绝请求

### 2. 值必须是 '1', '2', '3'
- 不能是其他值
- 不能是数字 1, 2, 3（必须是字符串）

### 3. 多轮对话中的 people 参数
- 第一条消息必须提供 people 参数
- 后续消息通过 conversation_id 关联
- people 参数可以更改（切换角色）

---

## 🎯 下一步

### 对于您（开发者）
1. ✅ 刷新页面测试
2. ✅ 检查角色选择器是否显示
3. ✅ 发送消息并观察控制台日志

### 对于 Dify 管理员
1. 🔧 检查 Dify 后台是否能看到调用记录
2. 🔧 确认 inputs.people 参数是否正确传递
3. 🔧 检查工作流是否正确触发

---

## 📞 如果仍然有问题

### 1. 检查控制台日志
```
发送请求到 Dify API: {...}
```
- 确认 inputs.people 的值

### 2. 检查 Dify 后台
- 是否有新的调用记录
- 错误信息是什么

### 3. 提供以下信息
- 浏览器控制台的请求日志
- Dify 后台的调用记录
- 任何错误信息

我会继续帮助您诊断和解决问题！ 💪
