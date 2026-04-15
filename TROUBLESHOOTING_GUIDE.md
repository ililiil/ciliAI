# CiliAI 订单创建问题排查指南

## ✅ 已完成的修复

### 1. 数据库修复
✅ orders 表已添加所有缺失的列：
- deadline, tags, script, description, contact_info
- min_profit, share_ratio, power_subsidy, period

✅ user_id 列已修改为允许 NULL 值

### 2. 后端API修复
✅ create_order() 函数已更新：
- 添加了 invite_code 处理逻辑
- 正确获取和关联用户ID
- INSERT语句已更新

### 3. 前端代码修复
✅ Order.vue 已更新：
- 添加了 inject 导入
- 注入了 inviteCode
- handleSubmit 中添加了 invite_code 字段

## 🔍 如何排查问题

### 方法1: 使用诊断工具

1. **打开诊断页面**
   ```
   文件: diagnose_order_creation.html
   路径: d:\fangtang\ciliAI\diagnose_order_creation.html
   ```

2. **双击打开HTML文件** 或运行 `open_diagnose.bat`

3. **查看调试信息区域**
   - 确认"后端状态"显示"✅ 后端正常"
   - 如果显示"❌ 后端连接失败"，说明后端服务器未运行

4. **点击"测试创建订单"按钮**
   - 查看响应结果
   - 如果显示"✅ 订单创建成功"，说明API完全正常

### 方法2: 查看浏览器控制台

1. **打开前端页面**: http://localhost:3003/

2. **打开开发者工具**
   - 按 F12 或 Ctrl+Shift+I (Windows)

3. **点击"Console"标签**

4. **尝试创建订单**
   - 查看控制台中是否有错误信息
   - 典型的错误包括：
     - `Failed to fetch` - 后端服务器未运行
     - `Network Error` - 网络问题
     - `CORS error` - 跨域问题

5. **查看Network标签**
   - 找到 `/api/orders` 请求
   - 查看请求的 Headers、Payload 和 Response
   - 红色表示失败的请求

### 方法3: 测试API直接连接

在浏览器中打开新标签，输入：
```
http://localhost:5001/api/orders
```

应该看到JSON响应，包含订单列表。

## ❌ 常见问题及解决方案

### 问题1: 后端服务器未运行

**症状**: 浏览器控制台显示 `Failed to fetch` 或 `Network Error`

**解决**:
1. 打开终端
2. 进入目录: `cd d:\fangtang\ciliAI`
3. 启动服务器: `python app.py`
4. 确认看到 "Running on http://127.0.0.1:5001"

### 问题2: 前端开发服务器未运行

**症状**: 访问 localhost:3003 显示"无法访问"

**解决**:
1. 打开新的终端
2. 进入目录: `cd d:\fangtang\ciliAI`
3. 启动前端: `npm run dev`
4. 确认看到 "Local: http://localhost:3003"

### 问题3: 数据库问题

**症状**: API返回 500 错误，消息为 "table orders has no column..."

**解决**:
1. 停止后端服务器 (Ctrl+C)
2. 运行修复脚本:
   ```
   python fix_database_full.py
   python make_user_id_nullable.py
   ```
3. 重启后端服务器:
   ```
   python app.py
   ```

### 问题4: CORS跨域错误

**症状**: 浏览器控制台显示 CORS 相关错误

**解决**:
1. 确认Flask服务器正在运行
2. 检查 vite.config.js 中的代理配置
3. 确保前端通过代理访问API，而不是直接访问5001端口

## 📋 测试清单

在诊断页面中测试以下内容：

- [ ] 后端状态显示"✅ 正常"
- [ ] 点击测试按钮后返回"✅ 订单创建成功"
- [ ] 浏览器控制台无红色错误
- [ ] Network中/api/orders请求状态码为200

## 🔧 完整重启步骤

如果问题依然存在，按以下步骤完全重启：

### 1. 停止所有服务
- 关闭所有终端窗口
- 结束所有Python进程: `taskkill /f /im python.exe` (谨慎使用)
- 结束所有Node进程: `taskkill /f /im node.exe` (谨慎使用)

### 2. 重启后端
```bash
cd d:\fangtang\ciliAI
python app.py
```

### 3. 重启前端
```bash
cd d:\fangtang\ciliAI
npm run dev
```

### 4. 清除浏览器缓存
- Chrome: Ctrl+Shift+Delete → 选择"所有时间" → 点击"清除数据"
- 或者直接用无痕模式打开: Ctrl+Shift+N

### 5. 测试
- 访问 http://localhost:3003
- 登录系统
- 进入"接单广场"
- 尝试创建订单

## 📞 获取帮助

如果以上方法都无法解决问题：

1. **打开诊断页面** (diagnose_order_creation.html)
2. **截图或复制所有错误信息**
3. **提供以下信息**:
   - 诊断页面的完整输出
   - 浏览器控制台的错误信息
   - Network标签中的请求详情
   - 后端终端的输出日志

## 📊 验证修复成功

打开浏览器访问：
```
http://localhost:5001/api/orders
```

应该看到类似以下的JSON响应：
```json
{
  "data": {
    "list": [...],
    "total": 5
  },
  "status": "success"
}
```

然后在前端：
1. 登录系统
2. 进入接单广场
3. 点击发布商单
4. 填写表单
5. 点击提交审核
6. 应该看到成功提示
