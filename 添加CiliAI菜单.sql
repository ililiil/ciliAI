-- CiliAI 业务菜单SQL
-- 在 RuoYi 数据库中执行此脚本添加CiliAI业务菜单

-- CiliAI顶级目录
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2000, 'CiliAI业务', 0, 10, 'cili', NULL, '', 'cili', 1, 0, 'M', '0', '0', '', 'cili', 'admin', NOW(), '', NULL, 'CiliAI业务模块目录');

-- 邀请码管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2001, '邀请码管理', 2000, 1, 'invitecode', 'system/invitecode/index', '', 'invitecode', 1, 0, 'C', '0', '0', 'cili:invitecode:list', 'user', 'admin', NOW(), '', NULL, '邀请码管理菜单');

-- 算力管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2002, '算力管理', 2000, 2, 'computepower', 'system/computepower/index', '', 'computepower', 1, 0, 'C', '0', '0', 'cili:computepower:list', 'user', 'admin', NOW(), '', NULL, '算力管理菜单');

-- 作品管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2003, '作品管理', 2000, 3, 'works', 'system/works/index', '', 'works', 1, 0, 'C', '0', '0', 'cili:works:list', 'image', 'admin', NOW(), '', NULL, '作品管理菜单');

-- 订单管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2004, '订单管理', 2000, 4, 'orders', 'system/orders/index', '', 'orders', 1, 0, 'C', '0', '0', 'cili:orders:list', 'shopping', 'admin', NOW(), '', NULL, '订单管理菜单');

-- AI生成记录
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2005, 'AI生成记录', 2000, 5, 'generationrecord', 'system/generationrecord/index', '', 'generationrecord', 1, 0, 'C', '0', '0', 'cili:generationrecord:list', 'bug', 'admin', NOW(), '', NULL, 'AI生成记录菜单');

-- 项目管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2006, '项目管理', 2000, 6, 'project', 'system/project/index', '', 'project', 1, 0, 'C', '0', '0', 'cili:project:list', 'tree', 'admin', NOW(), '', NULL, '项目管理菜单');

-- 广告管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2007, '广告管理', 2000, 7, 'advertisement', 'system/advertisement/index', '', 'advertisement', 1, 0, 'C', '0', '0', 'cili:advertisement:list', 'shopping', 'admin', NOW(), '', NULL, '广告管理菜单');

-- 聊天会话管理
INSERT INTO sys_menu (menu_id, menu_name, parent_id, order_num, path, component, query, route_name, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
VALUES (2008, '聊天管理', 2000, 8, 'chatsession', 'system/chatsession/index', '', 'chatsession', 1, 0, 'C', '0', '0', 'cili:chatsession:list', 'message', 'admin', NOW(), '', NULL, '聊天会话管理菜单');

-- 为超级管理员添加所有CiliAI菜单权限
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2000);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2001);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2002);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2003);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2004);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2005);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2006);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2007);
INSERT INTO sys_role_menu (role_id, menu_id) VALUES (1, 2008);

-- 提交事务
COMMIT;
