# CiliAI 项目 RuoYi 框架迁移方案

## 一、项目概述

### 1.1 现有系统架构
- **后端**：Flask + Python (app.py)
- **管理端前端**：Vue 3 + Element Plus (ciliAI/ruoyi/)
- **用户端前端**：Vue 3 + Element Plus (ciliAI/ciliAI/)
- **数据库**：MySQL
- **AI服务**：火山引擎即梦API

### 1.2 RuoYi 框架优势
✅ **完整的企业级权限管理系统**
- 用户管理、角色管理、菜单权限管理
- 部门管理、岗位管理
- JWT + Spring Security 安全认证
- 数据权限控制

✅ **丰富的内置功能**
- 操作日志、登录日志
- 定时任务调度
- 服务监控、缓存监控
- 代码生成器（快速生成 CRUD）
- 字典管理、参数配置
- 通知公告

✅ **成熟稳定的技术栈**
- Spring Boot 4.x + JDK 17+
- Vue 2 + Element UI
- MySQL + Redis
- 活跃的开源社区

## 二、RuoYi 能否替代当前系统？

### 2.1 完全兼容的功能
| 当前功能 | RuoYi 对应模块 | 说明 |
|---------|---------------|------|
| ✅ 用户管理 | sys_user | 完美匹配 |
| ✅ 管理员认证 | Spring Security + JWT | 更安全、更完善 |
| ✅ 角色权限 | sys_role + sys_menu | 完整的RBAC模型 |
| ✅ 日志记录 | sys_oper_log + sys_logininfor | 内置功能 |
| ✅ 定时任务 | sys_job | Quartz调度 |
| ✅ 文件上传 | sys_file | 通用文件服务 |

### 2.2 需要新增的业务模块
| 业务功能 | 需要新建的表 | 说明 |
|---------|------------|------|
| 🔧 邀请码管理 | cili_invite_code | 替代现有的 invite_codes 表 |
| 🔧 作品管理 | cili_works | 替代现有的 ip_works 表 |
| 🔧 算力管理 | cili_compute_power | 替代现有的 compute_power 表 |
| 🔧 订单管理 | cili_orders | 替代现有的 orders 表 |
| 🔧 广告管理 | cili_advertisement | 替代现有的 advertisements 表 |
| 🔧 项目管理 | cili_project | 替代现有的 projects 表 |
| 🔧 生成记录 | cili_generation_record | 替代现有的 generation_records 表 |
| 🔧 聊天管理 | cili_chat_session | 替代现有的 chat_sessions 表 |

### 2.3 需要保留的模块
| 模块 | 处理方式 | 说明 |
|-----|---------|------|
| ⚠️ 用户端前端 | 继续使用 | ciliAI/ciliAI/ 需要调整 API 对接 |
| ⚠️ 火山引擎集成 | 迁移到 Java | 需要在 Spring Boot 中重新实现 |
| ⚠️ 即梦AI API 调用 | 迁移到 Java | 使用 RestTemplate 或 WebClient |

## 三、迁移方案设计

### 3.1 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                    用户浏览器                             │
└────────────────┬────────────────────────┬──────────────┘
                 │                        │
          http://localhost:3003      http://localhost:8080
                 │                        │
                 ▼                        ▼
┌─────────────────────────────────────────────────────────┐
│               Vue 3 用户端前端                            │
│          (ciliAI/ciliAI/)                              │
│                                                         │
│  • 调用 RuoYi 后端 API                                  │
│  • AI 创作功能、文生图、视频生成                        │
└─────────────────────────────────────────────────────────┘
                 │
                 │  /api/* (JWT Token)
                 ▼
┌─────────────────────────────────────────────────────────┐
│            RuoYi Spring Boot 后端                       │
│         (RuoYi-Vue-master/ruoyi-admin/)                 │
│                                                         │
│  • 用户认证：Spring Security + JWT                     │
│  • 业务模块：cili_* 业务表                              │
│  • AI 服务：火山引擎即梦API调用                         │
│  • 文件服务：本地文件存储                               │
└─────────────────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                   MySQL 数据库                          │
│                                                         │
│  • RuoYi 基础表：sys_*                                  │
│  • CiliAI 业务表：cili_*                                │
│  • 缓存：Redis                                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 项目结构调整

```
d:\fangtang\ciliAI\
│
├── 📦 RuoYi-Vue-master/           # RuoYi 官方框架
│   ├── ruoyi-admin/               # 后台管理模块（主入口）
│   ├── ruoyi-system/             # 系统管理模块（可扩展）
│   ├── ruoyi-framework/          # 框架核心
│   ├── ruoyi-common/            # 公共组件
│   ├── ruoyi-ui/                 # 管理后台前端 Vue 2
│   ├── ruoyi-generator/         # 代码生成器
│   └── ruoyi-quartz/            # 定时任务
│
├── 🎨 ciliAI/                    # 用户端前端（保留）
│   └── ciliAI/
│       └── src/
│           ├── views/            # 页面组件
│           ├── api/              # API 调用
│           └── utils/            # 工具函数
│
└── 📚 docs/                      # 文档
```

### 3.3 数据库设计

#### 3.3.1 RuoYi 基础表（官方提供）
```sql
-- 用户表
sys_user (user_id, user_name, nick_name, email, phonenumber, ...)

-- 角色表
sys_role (role_id, role_name, role_key, ...)

-- 菜单表
sys_menu (menu_id, menu_name, parent_id, path, component, perms, ...)

-- 部门表
sys_dept (dept_id, dept_name, parent_id, ...)
```

#### 3.3.2 CiliAI 业务表（需要新增）
```sql
-- 邀请码表
CREATE TABLE cili_invite_code (
    id              BIGINT(20)      NOT NULL AUTO_INCREMENT,
    code            VARCHAR(50)     NOT NULL UNIQUE,
    used            TINYINT(1)     DEFAULT 0,
    used_by         BIGINT(20)     DEFAULT NULL,
    created_by      BIGINT(20)     NOT NULL,
    created_at      DATETIME       DEFAULT CURRENT_TIMESTAMP,
    expires_at     DATETIME       NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB COMMENT='邀请码表';

-- 作品表
CREATE TABLE cili_works (
    id              BIGINT(20)      NOT NULL AUTO_INCREMENT,
    user_id         BIGINT(20)      NOT NULL,
    title           VARCHAR(255)     NOT NULL,
    description     TEXT,
    image_url       VARCHAR(500),
    category        VARCHAR(50),
    is_public       TINYINT(1)      DEFAULT 1,
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_user_id (user_id)
) ENGINE=InnoDB COMMENT='作品表';

-- 算力表
CREATE TABLE cili_compute_power (
    id              BIGINT(20)      NOT NULL AUTO_INCREMENT,
    user_id         BIGINT(20)      NOT NULL UNIQUE,
    balance         DECIMAL(10,2)   DEFAULT 0.00,
    total_used      DECIMAL(10,2)   DEFAULT 0.00,
    updated_at      DATETIME        DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY idx_user_id (user_id)
) ENGINE=InnoDB COMMENT='算力表';

-- 订单表
CREATE TABLE cili_orders (
    id              BIGINT(20)      NOT NULL AUTO_INCREMENT,
    user_id         BIGINT(20)      NOT NULL,
    order_no        VARCHAR(50)      NOT NULL UNIQUE,
    amount          DECIMAL(10,2)   NOT NULL,
    power_amount    DECIMAL(10,2)   NOT NULL,
    status          VARCHAR(20)     DEFAULT 'pending',
    created_at      DATETIME        DEFAULT CURRENT_TIMESTAMP,
    paid_at         DATETIME,
    PRIMARY KEY (id),
    KEY idx_user_id (user_id),
    KEY idx_order_no (order_no)
) ENGINE=InnoDB COMMENT='订单表';
```

## 四、迁移步骤

### 阶段一：环境准备（1-2天）
1. ✅ 下载并解压 RuoYi-Vue 框架
2. 安装 JDK 17+
3. 安装 Maven
4. 配置 MySQL 数据库
5. 配置 Redis（可选）

### 阶段二：基础部署（2-3天）
1. 导入 RuoYi 数据库脚本（ry_20260321.sql）
2. 配置数据库连接（application-druid.yml）
3. 编译并启动 RuoYi 后端
4. 部署 RuoYi 前端（ruoyi-ui）
5. 验证基础功能（登录、用户管理）

### 阶段三：业务迁移（5-7天）
1. 创建 CiliAI 业务表
2. 在 ruoyi-system 中添加业务模块
3. 使用代码生成器生成基础 CRUD
4. 实现火山引擎 API 集成
5. 开发业务接口

### 阶段四：前端对接（3-5天）
1. 调整用户端前端 API 调用
2. 对接 RuoYi 的 JWT 认证
3. 测试完整业务流程
4. 界面优化和调整

### 阶段五：测试与优化（2-3天）
1. 功能测试
2. 性能测试
3. 安全测试
4. 部署上线

## 五、技术要点

### 5.1 JWT 认证流程
```
用户端前端                    RuoYi 后端                    MySQL
    │                           │                          │
    │──── POST /login ─────────>│                          │
    │                           │──── 验证用户 ────────────>│
    │                           │<─── 用户信息 ─────────────│
    │<─── {token} ─────────────│                          │
    │                           │                          │
    │──── GET /user/info ──────>│                          │
    │      (携带token)          │                          │
    │                           │──── 验证token ───────────>│
    │<─── {user_info} ──────────│                          │
```

### 5.2 火山引擎 API 集成
在 Spring Boot 中使用 RestTemplate 或 WebClient 调用火山引擎 API：

```java
@Service
public class VolcanoEngineService {

    @Value("${volcano.access-key}")
    private String accessKey;

    @Value("${volcano.secret-key}")
    private String secretKey;

    public String textToImage(TextToImageRequest request) {
        // 实现火山引擎 API 调用
    }
}
```

### 5.3 代码生成器的使用
RuoYi 内置强大的代码生成器，可以快速生成：
- Controller（控制器）
- Service（服务层）
- Mapper（数据访问层）
- Entity（实体类）
- Vue 前端页面

使用方法：
1. 在数据库中创建业务表
2. 访问 `/tool/gen` 生成代码
3. 下载生成的代码
4. 整合到项目中

## 六、优势对比

| 对比项 | 现有 Flask 系统 | RuoYi Spring Boot |
|-------|--------------|------------------|
| **安全性** | ⚠️ 基础 Token | ✅ JWT + Spring Security |
| **权限控制** | ⚠️ 简单判断 | ✅ 完整 RBAC + 数据权限 |
| **日志系统** | ⚠️ 手动记录 | ✅ 自动 AOP 切面 |
| **代码质量** | ⚠️ 脚本式 | ✅ 分层架构 |
| **扩展性** | ⚠️ 受限 | ✅ 模块化设计 |
| **社区支持** | ❌ 独立维护 | ✅ 活跃开源社区 |
| **文档完善** | ❌ 需要自建 | ✅ 丰富的文档 |
| **代码生成** | ❌ 手动编写 | ✅ 一键生成 |
| **监控运维** | ❌ 需要集成 | ✅ 内置监控 |
| **团队协作** | ⚠️ 困难 | ✅ 标准化开发流程 |

## 七、风险评估

### 7.1 主要风险
1. **技术栈切换成本**
   - 影响：团队需要学习 Java/Spring Boot
   - 缓解：RuoYi 文档完善，社区活跃

2. **Vue 2 vs Vue 3**
   - 影响：RuoYi 当前版本使用 Vue 2
   - 缓解：可考虑使用 RuoYi-Vue3 版本

3. **火山引擎 API 重写**
   - 影响：Python 代码需要重写为 Java
   - 缓解：API 调用逻辑相对简单

### 7.2 建议
1. **分支策略**：保留现有系统，新建 RuoYi 分支
2. **渐进式迁移**：先迁移管理后台，再迁移用户端
3. **充分测试**：每个功能点都需要测试验证

## 八、结论

**RuoYi 完全能够替代当前系统**，理由如下：

✅ **功能覆盖**：RuoYi 提供了比当前系统更完善的用户管理、权限控制、日志系统

✅ **技术优势**：Spring Boot + JWT + Spring Security 比现有 Flask 系统更安全、更稳定

✅ **开发效率**：代码生成器可以大大加速业务开发

✅ **社区支持**：活跃的开源社区，持续更新维护

✅ **代码质量**：分层架构，易于维护和扩展

**迁移建议**：
1. 采用渐进式迁移策略
2. 保留用户端前端，逐步对接新后端
3. 充分利用 RuoYi 的代码生成器
4. 保持与现有数据库的兼容性

## 九、下一步行动

1. **立即执行**：
   - 确认 JDK 17+ 环境
   - 初始化 RuoYi 项目
   - 导入数据库脚本
   - 启动 RuoYi 后端和前端

2. **本周内完成**：
   - 验证 RuoYi 基础功能
   - 设计 CiliAI 业务表结构
   - 开始迁移邀请码功能

3. **下个月内完成**：
   - 完成所有业务模块迁移
   - 完成用户端前端对接
   - 完成测试和优化

---

**文档版本**：v1.0
**创建时间**：2026-04-16
**维护者**：CiliAI Team
