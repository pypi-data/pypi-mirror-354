#!/usr/bin/env python3
"""
Test script for the Rust build_core module
"""
import sys
import os
from pathlib import Path

# Add the lib directory to path
lib_dir = Path(__file__).parent / "src" / "pyrmm" / "usr" / "lib"
sys.path.insert(0, str(lib_dir))

print(f"🔍 搜索路径: {lib_dir}")
print(f"🖥️ Python 版本: {sys.version}")
print(f"🖥️ 架构: {sys.platform} - {os.name}")

# Test 1: Try direct import
print("\n=== 测试 1: 直接导入 build_core ===")
try:
    import build_core
    print("✅ 直接导入 build_core 成功!")
    
    # Test creating an instance
    core = build_core.RmmBuilderCore()
    print("✅ 创建 RmmBuilderCore 实例成功!")
    
    # Test calling a method
    result = core.build()
    print(f"✅ 调用 build 方法成功: {result}")
    
    # Test utility functions
    network_ok = build_core.check_network_connection("https://www.baidu.com")
    print(f"✅ 网络连接测试: {network_ok}")
    
    dir_size = build_core.calculate_dir_size(str(lib_dir))
    print(f"✅ 目录大小计算: {dir_size} 字节")
    
except Exception as e:
    print(f"❌ 直接测试失败: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Try wrapper import
print("\n=== 测试 2: 通过 build_rust 包装器导入 ===")
try:
    import build_rust
    print("✅ 导入 build_rust 包装器成功!")
    
    builder = build_rust.RmmBuilderRust()
    print("✅ 创建 RmmBuilderRust 包装器成功!")
    
    print(f"✅ 模块可用性: {builder.is_available()}")
    
    if builder.is_available():
        # Test build functionality
        result = builder.build(project_name="test")
        print(f"✅ 构建测试: {result}")
        
except Exception as e:
    print(f"❌ 包装器测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 测试完成 ===")
