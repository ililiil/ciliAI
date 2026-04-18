# CiliAI 业务模块代码 - 使用指南

**版本**：v1.0  
**日期**：2026-04-16  
**状态**：✅ **核心模块完成**

---

## 📦 已生成的代码

### 1. 邀请码管理模块 ✅

| 文件 | 说明 | 状态 |
|------|------|------|
| CiliInviteCode.java | 实体类 | ✅ |
| CiliInviteCodeMapper.java | Mapper接口 | ✅ |
| CiliInviteCodeMapper.xml | Mapper XML | ✅ |
| ICiliInviteCodeService.java | 服务接口 | ✅ |
| CiliInviteCodeServiceImpl.java | 服务实现 | ✅ |
| CiliInviteCodeController.java | 控制器 | ✅ |

### 2. 算力管理模块 ✅

| 文件 | 说明 | 状态 |
|------|------|------|
| CiliComputePower.java | 实体类 | ✅ |
| CiliComputePowerMapper.java | Mapper接口 | ✅ |
| CiliComputePowerMapper.xml | Mapper XML | ✅ |
| ICiliComputePowerService.java | 服务接口 | ✅ |
| CiliComputePowerServiceImpl.java | 服务实现 | ✅ |
| CiliComputePowerController.java | 控制器 | ✅ |

### 3. 订单模块 ✅

| 文件 | 说明 | 状态 |
|------|------|------|
| CiliOrders.java | 实体类 | ✅ |

### 4. AI生成记录模块 ✅

| 文件 | 说明 | 状态 |
|------|------|------|
| CiliGenerationRecord.java | 实体类 | ✅ |

### 5. 火山引擎API集成 ✅

| 文件 | 说明 | 状态 |
|------|------|------|
| VolcanoEngineService.java | 服务接口 | ✅ |
| VolcanoEngineServiceImpl.java | 服务实现 | ✅ |

---

## 🚀 快速开始

### 步骤1：复制代码到RuoYi项目

```bash
# 复制到 ruoyi-system 模块
cp *.java /path/to/ruoyi-system/src/main/java/com/ruoyi/system/
cp *.xml /path/to/ruoyi-system/src/main/resources/mapper/system/
```

### 步骤2：配置数据库连接

确保 `application-druid.yml` 中配置了正确的数据库：

```yaml
spring:
  datasource:
    druid:
      master:
        url: jdbc:mysql://localhost:3306/ry_cloud?useUnicode=true&characterEncoding=utf8
        username: root
        password: root_password
```

### 步骤3：配置火山引擎密钥

在 `application.yml` 中添加：

```yaml
volcano:
  access-key: your_access_key
  secret-key: your_secret_key
```

### 步骤4：添加菜单

在数据库中执行：

```sql
-- CiliAI目录
INSERT INTO sys_menu VALUES(2000, 'CiliAI管理', 1, 10, 'cili', NULL, '', 'cili', 1, 0, 'M', '0', '0', '', ' cilixxx', 'admin', NOW(), '', NULL, 'CiliAI业务模块');

-- 邀请码管理
INSERT INTO sys_menu VALUES(2001, '邀请码管理', 2000, 1, 'invitecode', 'system/invitecode/index', '', 'invitecode', 1, 0, 'C', '0', '0', 'cili:invitecode:list', 'user', 'admin', NOW(), '', NULL, '邀请码管理菜单');

-- 算力管理
INSERT INTO sys_menu VALUES(2002, '算力管理', 2000, 2, 'computepower', 'system/computepower/index', '', 'computepower', 1, 0, 'C', '0', '0', 'cili:computepower:list', 'user', 'admin', NOW(), '', NULL, '算力管理菜单');
```

### 步骤5：编译并重启

```bash
cd d:/fangtang/RuoYi-Vue-master
mvn clean package -DskipTests
java -jar ruoyi-admin/target/ruoyi-admin.jar
```

---

## 📡 API接口

### 邀请码管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /system/invitecode/list | 查询列表 |
| GET | /system/invitecode/{id} | 查询详情 |
| POST | /system/invitecode | 新增 |
| PUT | /system/invitecode | 修改 |
| DELETE | /system/invitecode/{ids} | 删除 |
| POST | /system/invitecode/validate | 验证邀请码 |
| POST | /system/invitecode/batchGenerate | 批量生成 |

### 算力管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /system/computepower/list | 查询列表 |
| GET | /system/computepower/user/{userId} | 查询用户算力 |
| POST | /system/computepower/recharge/{userId} | 充值算力 |
| POST | /system/computepower/consume/{userId} | 消费算力 |

---

## 📚 还需要生成的模块

| 序号 | 模块 | 说明 | 状态 |
|------|------|------|------|
| 1 | cili_power_log | 算力日志 | ⏳ 待生成 |
| 2 | cili_works | 作品管理 | ⏳ 待生成 |
| 3 | cili_orders | 订单管理 | ⏳ 待生成 |
| 4 | cili_generation_record | AI生成记录 | ⏳ 待生成 |
| 5 | cili_project | 项目管理 | ⏳ 待生成 |
| 6 | cili_advertisement | 广告管理 | ⏳ 待生成 |
| 7 | cili_chat_session | 聊天会话 | ⏳ 待生成 |
| 8 | cili_chat_message | 聊天消息 | ⏳ 待生成 |

**建议使用RuoYi代码生成器完成剩余模块**

访问：**http://localhost:8080/tool/gen**

---

## ⚠️ 注意事项

1. **权限配置**：确保为管理员角色添加了对应的权限
2. **数据库表**：确保业务表已经创建在 `ry_cloud` 数据库中
3. **Redis**：确保Redis服务正在运行（用于会话管理）
4. **火山引擎密钥**：请替换为真实的密钥

---

## 🛠️ 故障排除

### 问题1：找不到Mapper XML
**解决**：将XML文件复制到 `resources/mapper/system/` 目录

### 问题2：权限不足
**解决**：在 `sys_role_menu` 表中添加对应的菜单权限

### 问题3：数据库连接失败
**解决**：检查 `application-druid.yml` 中的数据库配置

---

## 📞 帮助

- RuoYi 官方文档：http://doc.ruoyi.vip
- Gitee Issues：https://gitee.com/y_project/RuoYi-Vue/issues

---

**最后更新**：2026-04-16
