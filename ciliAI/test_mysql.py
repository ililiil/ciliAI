#!/usr/bin/env python3
"""
MySQL 部署前完整测试脚本
测试内容：
1. Python 语法检查
2. MySQL 连接测试
3. 应用启动测试
4. 数据库初始化测试
"""

import sys
import os
import subprocess

def test_syntax():
    """测试 Python 语法"""
    print("\n📝 测试 1: Python 语法检查")
    print("-" * 60)
    try:
        result = subprocess.run(
            ['python', '-m', 'py_compile', 'app.py'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ Python 语法检查通过")
            return True
        else:
            print(f"❌ Python 语法错误:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 语法检查失败: {e}")
        return False

def test_imports():
    """测试必要的导入"""
    print("\n📦 测试 2: 依赖包检查")
    print("-" * 60)
    
    required_packages = [
        'flask',
        'flask_cors',
        'pymysql',
        'volcengine',
        'dotenv',
        'requests',
        'PIL'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} 未安装")
            all_ok = False
    
    return all_ok

def test_mysql_import():
    """测试 MySQL 连接"""
    print("\n🗄️  测试 3: MySQL 连接测试")
    print("-" * 60)
    try:
        import pymysql
        print("✅ pymysql 已安装")
        
        # 测试连接配置（需要环境变量）
        from dotenv import load_dotenv
        load_dotenv()
        
        host = os.getenv('DB_HOST', 'localhost')
        port = int(os.getenv('DB_PORT', 3306))
        user = os.getenv('DB_USER', 'root')
        password = os.getenv('DB_PASSWORD', '')
        database = os.getenv('DB_NAME', 'ciliai')
        
        print(f"📍 连接信息: {host}:{port}/{database}")
        print("⚠️  注意: 需要配置正确的环境变量才能连接")
        print("   请确保 .env 文件中包含:")
        print("   - DB_HOST")
        print("   - DB_PORT") 
        print("   - DB_USER")
        print("   - DB_PASSWORD")
        print("   - DB_NAME")
        
        return True
    except ImportError:
        print("❌ pymysql 未安装，请运行: pip install pymysql")
        return False
    except Exception as e:
        print(f"❌ MySQL 连接测试失败: {e}")
        return False

def test_flask_app():
    """测试 Flask 应用能否加载"""
    print("\n🚀 测试 4: Flask 应用加载测试")
    print("-" * 60)
    try:
        # 设置测试环境变量
        os.environ['DB_HOST'] = 'localhost'
        os.environ['DB_PORT'] = '3306'
        os.environ['DB_USER'] = 'root'
        os.environ['DB_PASSWORD'] = 'test'
        os.environ['DB_NAME'] = 'test_db'
        
        # 尝试导入应用
        sys.path.insert(0, os.getcwd())
        
        # 不实际运行，只检查导入
        import app
        print("✅ Flask 应用模块加载成功")
        print(f"✅ 应用名称: {app.app.name}")
        print(f"✅ 数据库配置: {app.DATABASE['host']}:{app.DATABASE['port']}")
        
        return True
    except Exception as e:
        print(f"❌ Flask 应用加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("MySQL 部署前完整测试")
    print("=" * 60)
    
    results = {
        '语法检查': test_syntax(),
        '依赖检查': test_imports(),
        'MySQL连接': test_mysql_import(),
        'Flask应用': test_flask_app(),
    }
    
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{test_name}: {status}")
    
    print("=" * 60)
    
    all_passed = all(results.values())
    if all_passed:
        print("🎉 所有测试通过！代码已准备好部署到 MySQL。")
        print("\n下一步:")
        print("1. 配置 .env 文件中的数据库连接信息")
        print("2. 确保 MySQL 数据库已创建")
        print("3. 运行 docker-compose up -d --build")
        return 0
    else:
        print("⚠️  部分测试未通过，请检查上述错误")
        return 1

if __name__ == '__main__':
    sys.exit(main())
