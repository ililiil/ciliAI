#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
db_manager集成测试脚本
"""
import sys
import os

# 添加ciliAI目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'ciliAI'))

def test_db_manager():
    """测试数据库管理器"""
    print("=" * 60)
    print("db_manager 集成测试")
    print("=" * 60)
    
    try:
        # 导入数据库管理器
        from db_manager import db_manager
        
        print(f"\n✓ 数据库管理器导入成功")
        print(f"  数据库类型: {db_manager.db_type}")
        
        # 测试连接
        print("\n测试数据库连接...")
        conn = db_manager.get_connection()
        print(f"✓ 数据库连接成功")
        
        # 测试查询
        print("\n测试数据库查询...")
        cursor = conn.cursor()
        cursor.execute("SELECT 1 as test")
        result = cursor.fetchone()
        print(f"✓ 查询成功: {result}")
        conn.close()
        
        # 初始化数据库
        print("\n测试数据库初始化...")
        db_manager.init_database()
        print("✓ 数据库初始化成功")
        
        # 测试上下文管理器
        print("\n测试上下文管理器...")
        with db_manager.get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM sqlite_master")
            result = cursor.fetchone()
            if db_manager.db_type == 'mysql':
                count = list(result.values())[0]
            else:
                count = result[0]
            print(f"✓ 上下文管理器成功，当前有 {count} 个对象")
        
        # 测试get_count方法
        print("\n测试get_count方法...")
        count = db_manager.get_count("SELECT COUNT(*) as count FROM sqlite_master")
        print(f"✓ get_count方法成功: {count}")
        
        print("\n" + "=" * 60)
        print("所有测试通过！db_manager工作正常。")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = test_db_manager()
    sys.exit(0 if success else 1)
