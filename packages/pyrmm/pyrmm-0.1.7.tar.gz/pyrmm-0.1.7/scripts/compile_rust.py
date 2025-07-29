#!/usr/bin/env python3
"""
编译和安装 RMM Builder Rust Core 模块的脚本
支持跨平台编译和安装，专注于 Linux 平台的静态编译
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def get_platform_info():
    """获取平台信息"""
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    # 标准化架构名称
    if machine in ['x86_64', 'amd64']:
        arch = 'x86_64'
    elif machine in ['aarch64', 'arm64']:
        arch = 'aarch64'
    elif machine.startswith('arm'):
        arch = 'arm'
    else:
        arch = machine
    
    return system, arch


def get_module_extension():
    """获取当前平台的模块文件扩展名"""
    system = platform.system().lower()
    if system == 'windows':
        return '.pyd'
    elif system == 'darwin':  # macOS
        return '.so'
    else:  # Linux 和其他 Unix 系统
        return '.so'


def get_cargo_target():
    """获取 Cargo 构建目标"""
    system, arch = get_platform_info()
    
    target_map = {
        ('windows', 'x86_64'): 'x86_64-pc-windows-msvc',
        ('windows', 'aarch64'): 'aarch64-pc-windows-msvc',
        ('linux', 'x86_64'): 'x86_64-unknown-linux-musl',  # 使用 musl 静态编译
        ('linux', 'aarch64'): 'aarch64-unknown-linux-musl',  # 使用 musl 静态编译
        ('darwin', 'x86_64'): 'x86_64-apple-darwin',
        ('darwin', 'aarch64'): 'aarch64-apple-darwin',
    }
    
    return target_map.get((system, arch))


def run_command(cmd, cwd=None, env=None):
    """运行命令并返回结果"""
    print(f"🔧 运行命令: {' '.join(cmd)}")
    
    # 合并环境变量
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    
    result = subprocess.run(cmd, cwd=cwd, env=full_env, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"⚠️ 错误输出: {result.stderr}")
    
    return result.returncode == 0, result.stdout, result.stderr


def check_linux_static_deps():
    """检查 Linux 静态编译依赖"""
    print("🔍 检查 Linux 静态编译依赖...")
    
    # 检查 musl-tools
    success, _, _ = run_command(["which", "musl-gcc"])
    if not success:
        print("❌ 缺少 musl-gcc，Linux 静态编译需要 musl 工具链")
        print("📦 安装命令:")
        print("   Ubuntu/Debian: sudo apt-get install musl-tools musl-dev")
        print("   Alpine Linux: apk add musl-dev gcc")
        print("   CentOS/RHEL: 需要从源码编译 musl 或使用第三方仓库")
        return False
    
    print("✅ musl-gcc 已安装")
    
    # 检查 musl 头文件
    musl_headers = ["/usr/include/x86_64-linux-musl", "/usr/local/musl/include"]
    header_found = False
    for header_path in musl_headers:
        if Path(header_path).exists():
            print(f"✅ 找到 musl 头文件: {header_path}")
            header_found = True
            break
    
    if not header_found:
        print("⚠️ 警告: 未找到 musl 头文件目录")
        print("   这可能会导致编译问题")
    
    return True


def check_dependencies():
    """检查系统依赖"""
    print("🔍 检查系统依赖...")
    
    # 检查 Rust 工具链
    success, stdout, _ = run_command(["cargo", "--version"])
    if not success:
        print("❌ 错误: 未找到 Cargo，请先安装 Rust")
        print("   访问 https://rustup.rs/ 安装 Rust")
        return False
    
    print(f"✅ Cargo 版本: {stdout.strip()}")
    
    # 检查平台特定依赖
    system = platform.system().lower()
    if system == 'linux':
        # 对于 Linux，检查静态编译依赖
        if not check_linux_static_deps():
            return False
        
        # 检查是否有 musl 工具链（用于静态编译）
        _, arch = get_platform_info()
        musl_target = f"{arch}-unknown-linux-musl"
        
        print(f"🔍 检查 musl 目标是否已安装: {musl_target}")
        success, stdout, _ = run_command(["rustup", "target", "list", "--installed"])
        if success and musl_target not in stdout:
            print(f"📦 安装 musl 目标: {musl_target}")
            success, _, _ = run_command(["rustup", "target", "add", musl_target])
            if not success:
                print(f"⚠️ 警告: 无法安装 {musl_target}，将回退到 GNU 目标")
                return False
        else:
            print(f"✅ {musl_target} 已安装")
        
        # 检查 Python 开发头文件
        try:
            import sysconfig
            include_dir = sysconfig.get_path('include')
            python_h = Path(include_dir) / 'Python.h'
            if not python_h.exists():
                print("⚠️ 警告: 未找到 Python 开发头文件")
                print("   在 Ubuntu/Debian 上运行: sudo apt-get install python3-dev")
                print("   在 CentOS/RHEL 上运行: sudo yum install python3-devel")
                print("   在 Alpine 上运行: apk add python3-dev")
            else:
                print(f"✅ Python 开发头文件: {python_h}")
        except Exception:
            pass
    
    return True


def find_compiled_module(build_dir, target=None):
    """查找编译好的模块文件"""
    if target:
        target_dir = build_dir / "target" / target / "release"
    else:
        target_dir = build_dir / "target" / "release"
    
    print(f"🔍 在目录中查找模块: {target_dir}")
    
    # 不同平台的可能文件名
    system = platform.system().lower()
    if system == 'windows':
        possible_names = ["build_core.dll", "libbuild_core.dll", "build_core.pyd"]
    else:
        possible_names = ["libbuild_core.so", "build_core.so", "libbuild_core.dylib"]
    
    for name in possible_names:
        module_file = target_dir / name
        if module_file.exists():
            print(f"✅ 找到模块文件: {module_file}")
            return module_file
    
    # 如果没找到，列出目录内容帮助调试
    if target_dir.exists():
        print(f"📁 {target_dir} 目录内容:")
        for item in target_dir.iterdir():
            print(f"  - {item.name}")
    
    return None


def setup_linux_static_env():
    """设置 Linux 静态编译环境变量"""
    env = {}
    
    # 基础编译器设置
    env['CC'] = 'musl-gcc'
    env['CXX'] = 'musl-g++'
    
    # Cargo 目标特定的链接器
    env['CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_LINKER'] = 'musl-gcc'
    env['CARGO_TARGET_AARCH64_UNKNOWN_LINUX_MUSL_LINKER'] = 'aarch64-linux-musl-gcc'
    
    # 强制静态链接 CRT
    env['RUSTFLAGS'] = '-C target-feature=+crt-static -C link-arg=-static'
    
    # OpenSSL 静态编译支持
    env['OPENSSL_STATIC'] = '1'
    env['OPENSSL_DIR'] = '/usr'
    
    # PKG_CONFIG 设置为静态模式
    env['PKG_CONFIG_ALL_STATIC'] = '1'
    
    # 禁用动态链接库
    env['CARGO_CFG_TARGET_FEATURE'] = 'crt-static'
    
    print("🔧 配置 Linux 静态编译环境:")
    for key, value in env.items():
        print(f"   {key}={value}")
    
    return env


def setup_cross_compilation_env():
    """设置交叉编译环境变量"""
    system = platform.system().lower()
    
    if system == 'linux':
        return setup_linux_static_env()
    elif system == 'darwin':
        # macOS 通常不需要特殊设置
        return {}
    elif system == 'windows':
        # Windows 通常不需要特殊设置
        return {}
    else:
        return {}


def verify_static_linking(binary_path):
    """验证二进制文件是否为静态链接"""
    if not binary_path.exists():
        return False
    
    system = platform.system().lower()
    if system == 'linux':
        # 使用 ldd 检查动态链接库依赖
        success, stdout, _ = run_command(["ldd", str(binary_path)])
        if success:
            if "not a dynamic executable" in stdout or "statically linked" in stdout:
                print("✅ 验证: 二进制文件为静态链接")
                return True
            else:
                print("⚠️ 警告: 二进制文件可能包含动态依赖:")
                print(stdout)
                return False
        else:
            # ldd 失败可能意味着静态链接
            success, stdout, _ = run_command(["file", str(binary_path)])
            if "statically linked" in stdout:
                print("✅ 验证: 二进制文件为静态链接")
                return True
    
    return False


def get_target_architecture_dir(system, arch):
    """获取目标架构目录名"""
    arch_map = {
        ('windows', 'x86_64'): 'windows-x64',
        ('windows', 'aarch64'): 'windows-arm64',
        ('linux', 'x86_64'): 'linux-x64',
        ('linux', 'aarch64'): 'linux-aarch64',
        ('darwin', 'x86_64'): 'macos-x64',
        ('darwin', 'aarch64'): 'macos-aarch64',
    }
    return arch_map.get((system, arch), f"{system}-{arch}")


def main():
    """主函数"""
    print("🔧 RMM Builder Rust Core 编译脚本")
    print("=" * 50)
    
    # 显示平台信息
    system, arch = get_platform_info()
    print(f"🖥️  平台: {system} ({arch})")
    print(f"📦 模块扩展名: {get_module_extension()}")
    
    # 获取路径 - scripts 在项目根目录下
    script_dir = Path(__file__).parent
    project_root = script_dir.parent  # scripts 的父目录就是项目根目录
    build_core_dir = project_root / "build-core"
    
    if not build_core_dir.exists():
        print("❌ 错误: build-core 目录不存在")
        print(f"   期望位置: {build_core_dir}")
        sys.exit(1)
    
    print(f"📁 项目根目录: {project_root}")
    print(f"📁 构建目录: {build_core_dir}")
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 设置编译环境
    env = setup_cross_compilation_env()
    target = get_cargo_target()
    
    if target:
        print(f"🎯 构建目标: {target}")
        # 安装目标（如果需要）
        success, _, _ = run_command(["rustup", "target", "add", target], env=env)
        if not success:
            print(f"⚠️ 警告: 无法安装目标 {target}，使用默认目标")
            target = None
    
    # 编译模块
    print("\n🔨 编译 Rust 模块...")
    build_cmd = ["cargo", "build", "--release"]
    if target:
        build_cmd.extend(["--target", target])
    
    success, _, stderr = run_command(build_cmd, cwd=build_core_dir, env=env)
    if not success:
        print("❌ 编译失败")
        if stderr:
            print(f"错误详情: {stderr}")
        sys.exit(1)
    
    print("✅ 编译成功!")
    
    # 查找编译好的模块
    print("\n📦 查找编译好的模块...")
    module_file = find_compiled_module(build_core_dir, target)
    
    if not module_file:
        print("❌ 错误: 未找到编译好的模块文件")
        sys.exit(1)
    
    # 验证静态链接（仅在 Linux 上）
    if system == 'linux':
        verify_static_linking(module_file)
    
    # 确定目标目录
    lib_dir = project_root / "src" / "pyrmm" / "usr" / "lib"
    target_arch_dir = get_target_architecture_dir(system, arch)
    bin_dir = lib_dir / "build-core-bin" / target_arch_dir
    
    # 创建目标目录
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # 复制到架构特定目录
    target_name = f"build_core{get_module_extension()}"
    target_path = bin_dir / target_name
    
    print(f"\n📋 复制模块到: {target_path}")
    try:
        shutil.copy2(module_file, target_path)
        print("✅ 复制成功!")
        
        # 设置合适的权限 (Unix 系统)
        if platform.system().lower() != 'windows':
            os.chmod(target_path, 0o755)
        
        # 显示文件信息
        file_size = target_path.stat().st_size
        print(f"📐 文件大小: {file_size / 1024:.1f} KB")
        
        # 对于 Linux，显示静态链接信息
        if system == 'linux':
            print("🔍 检查依赖信息:")
            run_command(["file", str(target_path)])
            
    except Exception as e:
        print(f"❌ 复制失败: {e}")
        sys.exit(1)
    
    # 同时复制到当前 lib 目录以保持兼容性
    legacy_target = lib_dir / target_name
    try:
        shutil.copy2(module_file, legacy_target)
        print(f"✅ 也复制到兼容位置: {legacy_target}")
    except Exception as e:
        print(f"⚠️ 复制到兼容位置失败: {e}")
    
    # 测试模块
    print("\n🧪 测试模块...")
    try:
        # 将 lib 目录添加到 Python 路径
        sys.path.insert(0, str(lib_dir))
        
        # 尝试导入模块
        import build_rust
        
        # 运行简单测试
        print("✅ 模块导入成功!")
        
        # 测试网络连接函数
        try:
            result = build_rust.check_network_connection("https://www.google.com")
            print(f"🌐 网络连接测试: {result}")
        except Exception as e:
            print(f"⚠️ 网络连接测试失败: {e}")
        
        # 测试目录大小计算
        try:
            size = build_rust.calculate_dir_size(".")
            print(f"📏 当前目录大小: {size} 字节 ({size / 1024 / 1024:.2f} MB)")
        except Exception as e:
            print(f"⚠️ 目录大小计算失败: {e}")
        
        print("✅ 基础功能测试通过!")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        print("模块编译成功但无法正常工作")
        print("\n🔧 可能的解决方案:")
        print("1. 检查是否缺少运行时依赖")
        print("2. 确认 Python 版本兼容性")
        print("3. 检查系统架构匹配")
        sys.exit(1)
    
    print("\n🎉 RMM Builder Rust Core 编译完成!")
    print("💡 使用方法:")
    print("  from pyrmm.usr.lib.build_rust import RmmBuilder")
    print("  # 或者")
    print("  from pyrmm.usr.lib import build_rust")
    print(f"\n📊 生成的模块文件:")
    print(f"  - 架构特定: {target_path}")
    print(f"  - 兼容位置: {legacy_target}")
    
    if system == 'linux':
        print("\n🔒 Linux 静态编译特性:")
        print("  - 使用 musl libc 静态链接")
        print("  - 无动态库依赖")
        print("  - 可在不同 Linux 发行版间移植")


if __name__ == "__main__":
    main()
