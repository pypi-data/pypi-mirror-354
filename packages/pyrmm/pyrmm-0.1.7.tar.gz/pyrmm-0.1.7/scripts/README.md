# RMM Builder Rust Core 构建脚本

这个目录包含了用于编译、构建和部署 RMM Builder Rust Core 模块的脚本。

## 脚本说明

### 1. `compile_rust.py` - 单平台编译脚本

用于编译当前平台的 Rust 模块，特别优化了 Linux 平台的静态编译。

**功能特点:**
- 自动检测当前平台和架构
- Linux 平台使用 musl 进行静态编译，无动态库依赖
- 自动安装 Rust 目标和依赖检查
- 编译后自动测试模块功能

**使用方法:**
```bash
# 编译当前平台的模块
python scripts/compile_rust.py
```

**Linux 静态编译要求:**
```bash
# Ubuntu/Debian
sudo apt-get install musl-tools musl-dev python3-dev

# Alpine Linux  
apk add musl-dev gcc python3-dev

# CentOS/RHEL (需要额外配置)
# 可能需要从源码编译 musl
```

### 2. `build_multi_arch.py` - 多架构构建脚本

用于为多个平台和架构构建二进制文件。

**支持的目标:**
- **Linux**: x86_64, aarch64 (静态编译)
- **Windows**: x86_64, x86 
- **macOS**: x86_64, aarch64

**使用方法:**
```bash
# 构建当前平台的所有架构
python scripts/build_multi_arch.py

# 构建指定平台
python scripts/build_multi_arch.py --platforms linux

# 构建多个平台
python scripts/build_multi_arch.py --platforms linux windows macos

# 构建所有平台
python scripts/build_multi_arch.py --platforms all

# 生成构建信息文件
python scripts/build_multi_arch.py --info
```

### 3. `deploy.py` - 部署脚本

从预编译的二进制文件中选择合适的版本并部署到运行环境。

**使用方法:**
```bash
# 自动选择并部署适合当前平台的二进制文件
python scripts/deploy.py

# 列出所有可用的预编译二进制文件
python scripts/deploy.py --list

# 强制使用特定架构的二进制文件
python scripts/deploy.py --force-arch linux-x64

# 仅测试当前部署的模块
python scripts/deploy.py --test-only
```

## 目录结构

构建完成后，二进制文件将按以下结构存放：

```
src/pyrmm/usr/lib/
├── build-core-bin/           # 多架构二进制文件存放目录
│   ├── linux-x64/           # Linux x86_64 (静态编译)
│   │   └── build_core.so
│   ├── linux-aarch64/       # Linux ARM64 (静态编译)  
│   │   └── build_core.so
│   ├── windows-x64/         # Windows x86_64
│   │   └── build_core.pyd
│   ├── windows-x86/         # Windows x86
│   │   └── build_core.pyd
│   ├── macos-x64/           # macOS x86_64
│   │   └── build_core.so
│   ├── macos-aarch64/       # macOS ARM64
│   │   └── build_core.so
│   └── build_info.json     # 构建信息文件
├── build_core.so/.pyd       # 当前平台的兼容符号链接
└── build_rust.py           # Python 接口模块
```

## 工作流程

1. **开发阶段**: 使用 `compile_rust.py` 快速编译测试当前平台
2. **CI/CD**: 使用 `build_multi_arch.py` 构建所有平台的二进制文件
3. **部署阶段**: 使用 `deploy.py` 选择合适的二进制文件部署

## Linux 静态编译特性

### 优势
- **无依赖**: 不依赖系统的动态库，可在不同 Linux 发行版间移植
- **稳定性**: 避免动态库版本冲突问题
- **安全性**: 减少攻击面，提高安全性
- **分发简便**: 单个文件即可运行

### 技术实现
- 使用 `musl` libc 替代 `glibc`
- 启用 `crt-static` 特性进行静态链接
- 所有依赖库都静态编译进二进制文件

### 验证方法
```bash
# 检查动态库依赖 (应该显示 "not a dynamic executable")
ldd build_core.so

# 查看文件信息 (应该包含 "statically linked")
file build_core.so
```

## 故障排除

### 编译问题
1. **缺少 Rust 工具链**: 访问 https://rustup.rs/ 安装
2. **缺少系统依赖**: 参考脚本输出的安装提示
3. **目标架构不支持**: 检查 `rustup target list` 确认支持的目标

### 部署问题
1. **找不到兼容二进制**: 使用 `--list` 查看可用选项
2. **模块导入失败**: 检查 Python 版本兼容性和依赖
3. **权限问题**: 确保二进制文件有执行权限

### Linux 静态编译问题
1. **缺少 musl-gcc**: 安装 musl-tools 包
2. **链接错误**: 检查 musl 头文件是否完整安装
3. **OpenSSL 问题**: 确保设置了 `OPENSSL_STATIC=1`

## 性能优化

### 编译优化
- 使用 `--release` 模式编译
- 启用 LTO (Link Time Optimization)
- 针对目标 CPU 优化指令集

### 运行时优化  
- 静态编译避免了动态链接开销
- 减少了内存占用和启动时间
- 提高了缓存命中率

## 贡献指南

如需添加新的目标架构或优化构建过程:

1. 在 `TARGETS` 字典中添加新目标
2. 更新 `ARCH_DIR_MAP` 映射
3. 添加特定的环境变量配置
4. 更新文档和 CI 配置

## 许可证

遵循项目主许可证。
