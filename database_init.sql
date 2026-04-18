-- CiliAI 数据库初始化脚本
-- 创建日期: 2026-04-16

-- 1. 作品表
CREATE TABLE IF NOT EXISTS `cili_works` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `title` varchar(200) NOT NULL COMMENT '作品名称',
  `author` varchar(100) NOT NULL COMMENT '作者',
  `user_id` bigint DEFAULT NULL COMMENT '用户ID',
  `category` varchar(50) NOT NULL COMMENT '分类: novel-小说, video-视频, comic-漫剧',
  `description` text COMMENT '作品描述',
  `cover_image` varchar(500) DEFAULT NULL COMMENT '封面图片',
  `images` text COMMENT '作品图片，多个用逗号分隔',
  `video_url` varchar(500) DEFAULT NULL COMMENT '视频URL',
  `status` varchar(20) NOT NULL DEFAULT 'pending' COMMENT '状态: pending-待审核, approved-已通过, rejected-已拒绝',
  `is_top` tinyint NOT NULL DEFAULT 0 COMMENT '是否置顶: 0-否, 1-是',
  `like_count` int NOT NULL DEFAULT 0 COMMENT '点赞数',
  `view_count` int NOT NULL DEFAULT 0 COMMENT '浏览数',
  `audit_time` datetime DEFAULT NULL COMMENT '审核时间',
  `audit_reason` varchar(500) DEFAULT NULL COMMENT '审核理由',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_category` (`category`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='作品表';

-- 2. 订单表
CREATE TABLE IF NOT EXISTS `cili_orders` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `order_no` varchar(64) NOT NULL COMMENT '订单号',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `product_type` varchar(50) NOT NULL COMMENT '商品类型: compute_power-算力充值, vip-会员, service-服务',
  `product_id` bigint DEFAULT NULL COMMENT '商品ID',
  `compute_power` int NOT NULL COMMENT '算力数量',
  `amount` decimal(10,2) NOT NULL COMMENT '订单金额',
  `status` varchar(20) NOT NULL DEFAULT 'pending' COMMENT '状态: pending-待支付, paid-已支付, completed-已完成, cancelled-已取消, refunded-已退款',
  `pay_method` varchar(50) DEFAULT NULL COMMENT '支付方式: alipay-支付宝, wechat-微信',
  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
  `complete_time` datetime DEFAULT NULL COMMENT '完成时间',
  `refund_time` datetime DEFAULT NULL COMMENT '退款时间',
  `refund_reason` varchar(500) DEFAULT NULL COMMENT '退款原因',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_order_no` (`order_no`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 3. 广告表
CREATE TABLE IF NOT EXISTS `cili_advertisement` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `title` varchar(200) NOT NULL COMMENT '广告名称',
  `position` varchar(50) NOT NULL COMMENT '广告位置: home_top-首页顶部, home_bottom-首页底部, sidebar-侧边栏, popup-弹窗',
  `type` varchar(20) NOT NULL COMMENT '广告类型: image-图片, code-代码',
  `image_url` varchar(500) DEFAULT NULL COMMENT '图片URL',
  `link_url` varchar(500) DEFAULT NULL COMMENT '跳转链接',
  `code` text COMMENT '广告代码',
  `start_time` datetime NOT NULL COMMENT '开始时间',
  `end_time` datetime NOT NULL COMMENT '结束时间',
  `status` varchar(20) NOT NULL DEFAULT 'pending' COMMENT '状态: pending-待上线, active-上线, inactive-下线',
  `sort` int NOT NULL DEFAULT 0 COMMENT '排序',
  `view_count` int NOT NULL DEFAULT 0 COMMENT '曝光数',
  `click_count` int NOT NULL DEFAULT 0 COMMENT '点击数',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  KEY `idx_position` (`position`),
  KEY `idx_status` (`status`),
  KEY `idx_time` (`start_time`, `end_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='广告表';

-- 4. AI生成记录表
CREATE TABLE IF NOT EXISTS `cili_generation_record` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `task_id` varchar(100) NOT NULL COMMENT '任务ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `type` varchar(50) NOT NULL COMMENT '任务类型: text2img-文生图, img2img-图生图, video-视频生成',
  `status` varchar(20) NOT NULL COMMENT '状态: processing-进行中, success-成功, failed-失败, cancelled-已取消',
  `prompt` text COMMENT '提示词',
  `result_url` varchar(500) DEFAULT NULL COMMENT '结果URL',
  `error_message` text COMMENT '错误信息',
  `compute_power` int DEFAULT 0 COMMENT '消耗算力',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `complete_time` datetime DEFAULT NULL COMMENT '完成时间',
  PRIMARY KEY (`id`),
  KEY `idx_task_id` (`task_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='AI生成记录表';

-- 5. 项目表
CREATE TABLE IF NOT EXISTS `cili_project` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(200) NOT NULL COMMENT '项目名称',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `type` varchar(50) NOT NULL COMMENT '项目类型: novel-小说, comic-漫剧',
  `description` text COMMENT '项目描述',
  `status` varchar(20) DEFAULT 'active' COMMENT '状态: active-进行中, completed-已完成',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='项目管理表';

-- 6. 聊天会话表
CREATE TABLE IF NOT EXISTS `cili_chat_session` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `session_id` varchar(100) NOT NULL COMMENT '会话ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `status` varchar(20) DEFAULT 'active' COMMENT '状态: active-活跃, archived-归档',
  `message_count` int DEFAULT 0 COMMENT '消息数',
  `last_message` text COMMENT '最后一条消息',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_session_id` (`session_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天会话表';

-- 7. 聊天消息表
CREATE TABLE IF NOT EXISTS `cili_chat_message` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `session_id` bigint NOT NULL COMMENT '会话ID',
  `role` varchar(20) NOT NULL COMMENT '角色: user-用户, assistant-AI助手',
  `content` text NOT NULL COMMENT '消息内容',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_session_id` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='聊天消息表';

-- 8. 算力日志表
CREATE TABLE IF NOT EXISTS `cili_power_log` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `type` varchar(20) NOT NULL COMMENT '类型: recharge-充值, consume-消耗, refund-退款, reward-奖励',
  `amount` int NOT NULL COMMENT '变动金额(正负)',
  `balance_before` int NOT NULL COMMENT '变动前余额',
  `balance_after` int NOT NULL COMMENT '变动后余额',
  `reason` varchar(500) DEFAULT NULL COMMENT '原因',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_type` (`type`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='算力变动日志表';

-- 9. 邀请码表
CREATE TABLE IF NOT EXISTS `cili_invite_code` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `code` varchar(50) NOT NULL COMMENT '邀请码',
  `compute_power` int NOT NULL DEFAULT 1000 COMMENT '算力值',
  `status` varchar(20) NOT NULL DEFAULT 'active' COMMENT '状态: active-未使用, used-已使用, disabled-已禁用',
  `use_count` int NOT NULL DEFAULT 0 COMMENT '已使用次数',
  `max_use_count` int NOT NULL DEFAULT 1 COMMENT '最大使用次数',
  `expire_time` datetime DEFAULT NULL COMMENT '过期时间',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `create_by` varchar(64) DEFAULT '' COMMENT '创建者',
  `update_by` varchar(64) DEFAULT '' COMMENT '更新者',
  `remark` varchar(500) DEFAULT NULL COMMENT '备注',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_code` (`code`),
  KEY `idx_status` (`status`),
  KEY `idx_create_time` (`create_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='邀请码表';

-- 10. 算力表
CREATE TABLE IF NOT EXISTS `cili_compute_power` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `balance` int NOT NULL DEFAULT 0 COMMENT '当前算力余额',
  `total_recharged` int NOT NULL DEFAULT 0 COMMENT '累计充值',
  `total_consumed` int NOT NULL DEFAULT 0 COMMENT '累计消耗',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户算力表';
