# 修复 CORS 跨域图片加载错误

## 问题描述

在后台管理系统中加载广告位、作品或订单图片时，浏览器控制台出现以下错误：

```
[error] net::ERR_BLOCKED_BY_ORB https://example.com/ad.jpg
```

**错误原因**：
- `ERR_BLOCKED_BY_ORB` (Opaque Response Blocking) 是浏览器的一种安全机制
- 当图片URL指向不允许跨域访问的域名（如 `example.com`）时，浏览器会阻止加载
- 这些通常是测试数据中残留的无效URL

## 解决方案

### 1. 前端防护：添加URL验证函数

已在以下文件中添加图片URL验证逻辑：

#### `ruoyi/src/views/Advertisement.vue`
- 添加 `isValidImageUrl()` 函数
- 添加 `getValidImageUrl()` 函数
- 在显示图片时自动过滤无效URL

#### `ruoyi/src/views/Works.vue`
- 在现有的 `getFullImageUrl()` 函数中添加URL验证
- 过滤掉包含 `example.com`, `test.com`, `placeholder.com` 的URL

#### `ruoyi/src/views/OrderManagement.vue`
- 添加 `isValidImageUrl()` 和 `getFullImageUrl()` 函数
- 在表格和表单中统一使用有效图片URL

### 2. 后端清理：数据库脚本

创建了数据库清理脚本 `ciliAI/fix_invalid_image_urls.py`

**功能**：
- 自动扫描 `ip_works`, `orders`, `advertisements`, `projects` 表
- 查找并清除包含 `example.com` 和 `test.com` 的无效图片URL
- 将无效URL设置为空字符串

**使用方法**：
```bash
cd d:\fangtang\ciliAI\ciliAI
python fix_invalid_image_urls.py
```

### 3. 已清理的无效数据

从数据库中清理了以下无效记录：
- `advertisements` 表：2条包含 `https://example.com/ad.jpg` 的记录

## 验证步骤

1. **运行数据库清理脚本**
   ```bash
   python fix_invalid_image_urls.py
   ```

2. **检查前端代码**
   - 确认 `Advertisement.vue`、`Works.vue`、`OrderManagement.vue` 包含URL验证逻辑
   - 确认使用 `getValidImageUrl()` 或 `getFullImageUrl()` 函数

3. **测试图片加载**
   - 刷新后台管理页面
   - 打开浏览器开发者工具
   - 确认不再出现 `ERR_BLOCKED_BY_ORB` 错误

## 预防措施

### 添加新数据时的验证
在添加新的广告、作品或订单时，前端和后端都应该验证图片URL：

**前端验证（JavaScript）**：
```javascript
const isValidImageUrl = (url) => {
  if (!url || !url.trim()) return false
  
  const invalidPatterns = [
    'example.com',
    'test.com',
    'placeholder.com',
    'invalid-url'
  ]
  
  const lowerUrl = url.toLowerCase()
  return !invalidPatterns.some(pattern => lowerUrl.includes(pattern))
}
```

**后端验证（Python）**：
```python
import re

def is_valid_image_url(url):
    if not url:
        return True  # 空URL是允许的
    
    invalid_patterns = [
        r'example\.com',
        r'test\.com',
        r'placeholder\.com'
    ]
    
    for pattern in invalid_patterns:
        if re.search(pattern, url, re.IGNORECASE):
            return False
    
    return True
```

### CORS 配置
确保图片服务器正确配置了 CORS 头：

```apache
# Apache .htaccess
<IfModule mod_headers.c>
    <FilesMatch "\.(jpg|jpeg|png|gif|webp)$">
        Header set Access-Control-Allow-Origin "*"
    </FilesMatch>
</IfModule>
```

```nginx
# Nginx
location ~* \.(jpg|jpeg|png|gif|webp)$ {
    add_header Access-Control-Allow-Origin *;
}
```

## 相关文件

### 修改的文件
- `ruoyi/src/views/Advertisement.vue`
- `ruoyi/src/views/Works.vue`
- `ruoyi/src/views/OrderManagement.vue`

### 新增的文件
- `ciliAI/fix_invalid_image_urls.py` - 数据库清理脚本
- `ciliAI/check_invalid_urls.py` - URL检查脚本

## 参考资料

- [MDN: CORS](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS)
- [Chromium ORB Policy](https://www.chromium.org/Home/chromium-security/site-isolation/)
- [OWASP: HTML5 Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
