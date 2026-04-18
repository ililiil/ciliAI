@echo off
chcp 65001 >nul
docker exec ciliai-mysql mysql -uroot -proot_password -e "SET NAMES utf8mb4;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "ALTER TABLE sys_menu CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='CiliAI管理' WHERE menu_id=2000;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='邀请码管理' WHERE menu_id=2001;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='算力管理' WHERE menu_id=2002;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='作品管理' WHERE menu_id=2003;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='订单管理' WHERE menu_id=2004;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='AI生成记录' WHERE menu_id=2005;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='项目管理' WHERE menu_id=2006;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='广告管理' WHERE menu_id=2007;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET menu_name='聊天管理' WHERE menu_id=2008;" ry_cloud
docker exec ciliai-mysql mysql -uroot -proot_password -e "UPDATE sys_menu SET remark='CiliAI业务模块' WHERE menu_id=2000;" ry_cloud
echo 完成！请刷新前端页面
pause
