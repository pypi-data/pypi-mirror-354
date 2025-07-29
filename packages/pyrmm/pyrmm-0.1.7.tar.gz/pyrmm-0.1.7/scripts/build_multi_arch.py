#!/usr/bin/env python3
"""
多架构构建脚本 for RMM Builder Rust Core
支持为多个平台和架构构建二进制文件
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json


# 支持的目标架构
TARGETS = {
    'linux': [
        'x86_64-unknown-linux-musl',
        'aarch64-unknown-linux-musl',
    ],
    'windows': [
        'x86_64-pc-windows-msvc',
        'i686-pc-windows-msvc',
    ],
    'macos': [
        'x86_64-apple-darwin',
        'aarch64-apple-darwin',
    ]
}

# 架构映射到目录名
ARCH_DIR_MAP = {
    'x86_64-unknown-linux-musl': 'linux-x64',
    'aarch64-unknown-linux-musl': 'linux-aarch64',
    'x86_64-pc-windows-msvc': 'windows-x64',
    'i686-pc-windows-msvc': 'windows-x86',
    'x86_64-apple-darwin': 'macos-x64',
    'aarch64-apple-darwin': 'macos-aarch64',
}

# 文件扩展名映射
EXTENSION_MAP = {
    'linux': '.so',
    'windows': '.pyd',
    'macos': '.so',
}


def run_command(cmd, cwd=None, env=None):
    """运行命令并返回结果"""
    print(f"🔧 运行命令: {' '.join(cmd)}")
    
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    
    result = subprocess.run(cmd, cwd=cwd, env=full_env, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and result.returncode != 0:
        print(f"⚠️ 错误输出: {result.stderr}")
    
    return result.returncode == 0, result.stdout, result.stderr


def get_static_build_env(target):
    """获取静态构建环境变量"""
    env = {}
    
    if 'linux-musl' in target:
        # Linux musl 静态编译
        env.update({
            'CC': 'musl-gcc',
            'CXX': 'musl-g++',
            'RUSTFLAGS': '-C target-feature=+crt-static -C link-arg=-static',
            'OPENSSL_STATIC': '1',
            'PKG_CONFIG_ALL_STATIC': '1',
        })
        
        if 'x86_64' in target:
            env['CARGO_TARGET_X86_64_UNKNOWN_LINUX_MUSL_LINKER'] = 'musl-gcc'
        elif 'aarch64' in target:
            env['CARGO_TARGET_AARCH64_UNKNOWN_LINUX_MUSL_LINKER'] = 'aarch64-linux-musl-gcc'
    
    return env


def install_target(target):
    """安装构建目标"""
    print(f"📦 安装构建目标: {target}")
    success, _, _ = run_command(["rustup", "target", "add", target])
    return success


def build_target(target, build_dir):
    """构建特定目标"""
    print(f"\n🔨 开始构建目标: {target}")
    
    # 设置环境变量
    env = get_static_build_env(target)
    
    # 构建命令
    build_cmd = ["cargo", "build", "--release", "--target", target]
    
    success, stdout, stderr = run_command(build_cmd, cwd=build_dir, env=env)
    
    if success:
        print(f"✅ {target} 构建成功")
        return True, None
    else:
        print(f"❌ {target} 构建失败")
        return False, stderr


def find_built_module(build_dir, target):
    """查找构建好的模块"""
    target_dir = build_dir / "target" / target / "release"
    
    # 根据目标平台确定文件名模式
    if 'windows' in target:
        patterns = ["build_core.dll", "libbuild_core.dll"]
    else:
        patterns = ["libbuild_core.so", "build_core.so"]
    
    for pattern in patterns:
        module_path = target_dir / pattern
        if module_path.exists():
            return module_path
    
    return None


def copy_to_bin_dir(module_path, target, project_root):
    """复制模块到对应的架构目录"""
    arch_dir = ARCH_DIR_MAP.get(target)
    if not arch_dir:
        print(f"⚠️ 未知的目标架构: {target}")
        return False
    
    # 确定文件扩展名
    platform_name = arch_dir.split('-')[0]
    extension = EXTENSION_MAP.get(platform_name, '.so')
    
    # 目标目录
    bin_dir = project_root / "src" / "pyrmm" / "usr" / "lib" / "build-core-bin" / arch_dir
    bin_dir.mkdir(parents=True, exist_ok=True)
    
    # 目标文件
    target_file = bin_dir / f"build_core{extension}"
    
    try:
        shutil.copy2(module_path, target_file)
        
        # 设置权限
        if platform_name != 'windows':
            os.chmod(target_file, 0o755)
        
        file_size = target_file.stat().st_size
        print(f"✅ 复制到 {arch_dir}: {target_file} ({file_size / 1024:.1f} KB)")
        return True
        
    except Exception as e:
        print(f"❌ 复制失败 {arch_dir}: {e}")
        return False


def build_all_targets(platforms=None):
    """构建所有或指定平台的目标"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    build_core_dir = project_root / "build-core"
    
    if not build_core_dir.exists():
        print(f"❌ 错误: build-core 目录不存在: {build_core_dir}")
        return False
    
    # 确定要构建的平台
    if platforms is None:
        # 默认构建当前平台
        current_platform = platform.system().lower()
        if current_platform == 'darwin':
            current_platform = 'macos'
        platforms = [current_platform] if current_platform in TARGETS else []
    
    if not platforms:
        print("❌ 没有指定有效的构建平台")
        return False
    
    print(f"🎯 将构建平台: {', '.join(platforms)}")
    
    # 收集所有目标
    all_targets = []
    for platform_name in platforms:
        all_targets.extend(TARGETS.get(platform_name, []))
    
    if not all_targets:
        print("❌ 没有找到要构建的目标")
        return False
    
    print(f"📋 构建目标列表: {', '.join(all_targets)}")
    
    # 安装目标
    print("\n📦 安装构建目标...")
    for target in all_targets:
        if not install_target(target):
            print(f"⚠️ 无法安装目标 {target}，跳过")
            all_targets.remove(target)
    
    # 构建结果
    build_results = {}
    failed_targets = []
    
    # 串行构建 (避免资源冲突)
    for target in all_targets:
        success, error = build_target(target, build_core_dir)
        build_results[target] = success
        
        if success:
            # 查找并复制模块
            module_path = find_built_module(build_core_dir, target)
            if module_path:
                copy_to_bin_dir(module_path, target, project_root)
            else:
                print(f"⚠️ 未找到 {target} 的构建产物")
                failed_targets.append(target)
        else:
            failed_targets.append(target)
    
    # 输出构建结果
    print("\n📊 构建结果汇总:")
    successful_targets = [t for t, success in build_results.items() if success]
    
    if successful_targets:
        print("✅ 成功构建:")
        for target in successful_targets:
            arch_dir = ARCH_DIR_MAP.get(target, target)
            print(f"  - {target} → {arch_dir}")
    
    if failed_targets:
        print("❌ 构建失败:")
        for target in failed_targets:
            print(f"  - {target}")
    
    return len(successful_targets) > 0


def create_build_info():
    """创建构建信息文件"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    bin_dir = project_root / "src" / "pyrmm" / "usr" / "lib" / "build-core-bin"
    
    build_info = {
        "build_time": subprocess.check_output(["date", "-u"], text=True).strip(),
        "rust_version": subprocess.check_output(["rustc", "--version"], text=True).strip(),
        "targets": {},
    }
    
    # 扫描所有架构目录
    for arch_dir in bin_dir.iterdir():
        if arch_dir.is_dir():
            module_files = list(arch_dir.glob("build_core.*"))
            if module_files:
                module_file = module_files[0]
                file_size = module_file.stat().st_size
                build_info["targets"][arch_dir.name] = {
                    "file": module_file.name,
                    "size": file_size,
                    "size_kb": round(file_size / 1024, 1),
                }
    
    # 保存构建信息
    info_file = bin_dir / "build_info.json"
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(build_info, f, indent=2, ensure_ascii=False)
    
    print(f"📋 构建信息已保存: {info_file}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RMM Builder Rust Core 多架构构建脚本")
    parser.add_argument(
        "--platforms", 
        nargs="+", 
        choices=["linux", "windows", "macos", "all"],
        help="要构建的平台"
    )
    parser.add_argument(
        "--info", 
        action="store_true",
        help="创建构建信息文件"
    )
    
    args = parser.parse_args()
    
    print("🔧 RMM Builder Rust Core 多架构构建脚本")
    print("=" * 60)
    
    # 处理 --info 参数
    if args.info:
        create_build_info()
        return
    
    # 处理平台参数
    platforms = args.platforms
    if platforms and "all" in platforms:
        platforms = list(TARGETS.keys())
    
    # 开始构建
    success = build_all_targets(platforms)
    
    if success:
        # 创建构建信息
        create_build_info()
        print("\n🎉 多架构构建完成!")
    else:
        print("\n❌ 构建过程中出现错误")
        sys.exit(1)


if __name__ == "__main__":
    main()
