#!/usr/bin/env python3
"""
部署脚本 for RMM Builder Rust Core
从构建产物中选择合适的二进制文件并部署到运行环境
"""

import os
import sys
import shutil
import platform
import json
from pathlib import Path


def get_current_platform_info():
    """获取当前平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # 标准化系统名称
    if system == 'darwin':
        system = 'macos'
    
    # 标准化架构名称
    if machine in ['x86_64', 'amd64']:
        arch = 'x64'
    elif machine in ['aarch64', 'arm64']:
        arch = 'aarch64'
    elif machine in ['i386', 'i686']:
        arch = 'x86'
    else:
        arch = machine
    
    return system, arch


def get_module_extension():
    """获取模块文件扩展名"""
    system = platform.system().lower()
    if system == 'windows':
        return '.pyd'
    else:
        return '.so'


def find_compatible_binary(bin_dir, system, arch):
    """查找兼容的二进制文件"""
    # 精确匹配
    exact_match = f"{system}-{arch}"
    exact_dir = bin_dir / exact_match
    
    if exact_dir.exists():
        module_files = list(exact_dir.glob("build_core.*"))
        if module_files:
            return exact_dir, module_files[0]
    
    # 兼容性匹配
    compatible_patterns = []
    
    if system == 'linux' and arch == 'x64':
        compatible_patterns = ['linux-x86_64', 'linux-amd64']
    elif system == 'macos' and arch == 'aarch64':
        compatible_patterns = ['macos-arm64']
    elif system == 'windows' and arch == 'x64':
        compatible_patterns = ['windows-x86_64', 'windows-amd64']
    
    for pattern in compatible_patterns:
        compat_dir = bin_dir / pattern
        if compat_dir.exists():
            module_files = list(compat_dir.glob("build_core.*"))
            if module_files:
                return compat_dir, module_files[0]
    
    return None, None


def list_available_binaries(bin_dir):
    """列出所有可用的二进制文件"""
    print("📋 可用的预编译二进制文件:")
    
    if not bin_dir.exists():
        print(f"❌ 二进制目录不存在: {bin_dir}")
        return []
    
    available = []
    for arch_dir in sorted(bin_dir.iterdir()):
        if arch_dir.is_dir():
            module_files = list(arch_dir.glob("build_core.*"))
            if module_files:
                module_file = module_files[0]
                file_size = module_file.stat().st_size
                print(f"  - {arch_dir.name}: {module_file.name} ({file_size / 1024:.1f} KB)")
                available.append(arch_dir.name)
    
    return available


def deploy_binary(source_file, target_dir):
    """部署二进制文件"""
    target_name = f"build_core{get_module_extension()}"
    target_path = target_dir / target_name
    
    print(f"📦 部署二进制文件:")
    print(f"  源文件: {source_file}")
    print(f"  目标: {target_path}")
    
    try:
        # 备份现有文件
        if target_path.exists():
            backup_path = target_path.with_suffix(target_path.suffix + '.bak')
            shutil.copy2(target_path, backup_path)
            print(f"  备份现有文件: {backup_path}")
        
        # 复制新文件
        shutil.copy2(source_file, target_path)
        
        # 设置权限
        if platform.system().lower() != 'windows':
            os.chmod(target_path, 0o755)
        
        file_size = target_path.stat().st_size
        print(f"✅ 部署成功! 文件大小: {file_size / 1024:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ 部署失败: {e}")
        return False


def test_deployment(lib_dir):
    """测试部署的模块"""
    print("\n🧪 测试部署的模块...")
    
    # 临时添加到 Python 路径
    original_path = sys.path.copy()
    sys.path.insert(0, str(lib_dir))
    
    try:
        # 尝试导入
        import build_rust
        print("✅ 模块导入成功")
        
        # 简单功能测试
        try:
            result = build_rust.check_network_connection("https://www.google.com")
            print(f"🌐 网络连接测试: {result}")
        except Exception as e:
            print(f"⚠️ 网络连接测试失败: {e}")
        
        try:
            size = build_rust.calculate_dir_size(".")
            print(f"📏 目录大小计算测试: {size} 字节")
        except Exception as e:
            print(f"⚠️ 目录大小计算测试失败: {e}")
        
        print("✅ 基础功能测试通过")
        return True
        
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False
    finally:
        # 恢复 Python 路径
        sys.path = original_path


def load_build_info(bin_dir):
    """加载构建信息"""
    info_file = bin_dir / "build_info.json"
    if info_file.exists():
        try:
            with open(info_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ 无法读取构建信息: {e}")
    return None


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RMM Builder Rust Core 部署脚本")
    parser.add_argument(
        "--force-arch",
        help="强制使用指定架构的二进制文件"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出所有可用的二进制文件"
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="仅测试当前部署的模块"
    )
    
    args = parser.parse_args()
    
    print("🚀 RMM Builder Rust Core 部署脚本")
    print("=" * 50)
    
    # 获取路径
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    bin_dir = project_root / "src" / "pyrmm" / "usr" / "lib" / "build-core-bin"
    lib_dir = project_root / "src" / "pyrmm" / "usr" / "lib"
    
    # 仅测试模式
    if args.test_only:
        success = test_deployment(lib_dir)
        sys.exit(0 if success else 1)
    
    # 列出可用二进制文件
    available = list_available_binaries(bin_dir)
    if args.list:
        return
    
    if not available:
        print("❌ 没有找到任何预编译的二进制文件")
        print("💡 请先运行构建脚本: python scripts/build_multi_arch.py")
        sys.exit(1)
    
    # 获取当前平台信息
    system, arch = get_current_platform_info()
    print(f"\n🖥️  当前平台: {system} ({arch})")
    
    # 加载构建信息
    build_info = load_build_info(bin_dir)
    if build_info:
        print(f"📅 构建时间: {build_info.get('build_time', '未知')}")
        print(f"🦀 Rust 版本: {build_info.get('rust_version', '未知')}")
    
    # 确定要使用的架构
    if args.force_arch:
        target_arch = args.force_arch
        print(f"🎯 强制使用架构: {target_arch}")
    else:
        target_arch = f"{system}-{arch}"
        print(f"🎯 自动选择架构: {target_arch}")
    
    # 查找兼容的二进制文件
    arch_dir, binary_file = find_compatible_binary(bin_dir, system, arch if not args.force_arch else args.force_arch.split('-')[1])
    
    if not binary_file:
        print(f"❌ 未找到兼容 {target_arch} 的二进制文件")
        print("\n可用的架构:")
        for avail in available:
            print(f"  - {avail}")
        print("\n💡 使用 --force-arch 参数强制指定架构")
        sys.exit(1)
    
    print(f"✅ 找到兼容的二进制文件: {arch_dir.name}/{binary_file.name}")
    
    # 部署二进制文件
    success = deploy_binary(binary_file, lib_dir)
    
    if success:
        # 测试部署
        test_success = test_deployment(lib_dir)
        
        if test_success:
            print("\n🎉 部署完成并测试通过!")
            print("💡 现在可以使用 RMM Builder Rust Core 了")
        else:
            print("\n⚠️ 部署完成但测试失败")
            print("💡 模块可能存在兼容性问题")
            sys.exit(1)
    else:
        print("\n❌ 部署失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
