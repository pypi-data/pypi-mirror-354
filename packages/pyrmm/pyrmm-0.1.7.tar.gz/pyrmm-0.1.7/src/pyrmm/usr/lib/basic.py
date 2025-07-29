"""模块基本脚本
This file is part of PyRMM.

CUSTOMIZE_SH: customize.sh
SERVERS_SH: servers.sh
...

"""


CUSTOMIZE_SH = """
# This file is part of PyRMM.
ui_print "开始安装模块..."

"""

SERVERS_SH = """
# This file is part of PyRMM.
"""


README = """
# {project_name}

一个基于 RMM (Root Module Manager) 的模块项目。

## 功能特性

- 支持 Magisk、APatch、KernelSU
- 自动版本管理
- 构建输出优化
- GitHub 集成

## 安装方法

1. 下载最新的 release 文件
2. 通过 Magisk/APatch/KernelSU 安装模块
3. 重启设备

## 构建

```bash
# 构建模块
rmm build

# 发布到 GitHub
rmm publish
```

## 开发

```bash
# 安装开发依赖
uv tool install pyrmm

# 初始化项目
rmm init .

# 构建并测试
rmm build && rmm test
```

## 许可证

MIT License - 查看 [LICENSE](LICENSE) 文件了解详情。

## 作者

- {author_name}

---

使用 [RMM](https://github.com/LIghtJUNction/RootManage-Module-Model) 构建

"""

from datetime import datetime
CHANGELOG = f"""
# 更新日志

所有对该项目的重要更改都会记录在此文件中。

## [未发布]

### 新增
- 初始项目设置
- 基本模块结构

### 变更
- 无

### 修复
- 无

## [1.0.0] - {datetime.now().strftime('%Y-%m-%d')}

### 新增
- 项目初始版本
- 基本功能实现

---

## 版本格式说明

- **[未发布]** - 即将发布的更改
- **[版本号]** - 已发布的版本及发布日期

### 更改类型

- **新增** - 新功能
- **变更** - 现有功能的更改
- **弃用** - 即将移除的功能
- **移除** - 已移除的功能
- **修复** - Bug 修复
- **安全** - 安全相关的修复
"""

LICENSE = """
# LICENSES        
# ADD YOUR LICENSES HERE

# RMM Project License
MIT License

Copyright (c) 2025 LIghtJUNction

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


RMAKE = '''#!/usr/bin/env python3
"""
RMM 构建脚本
自定义构建逻辑，配合 rmmproject.toml 中的构建配置使用

正确的配置说明:
[build]
prebuild = "Rmake"     # 调用下面的 prebuild() 函数进行预构建处理
build = "default"      # 使用默认构建逻辑（打包zip和tar.gz文件）
postbuild = "Rmake"    # 调用下面的 postbuild() 函数进行后构建处理

注意：
- 推荐使用上述配置，利用 Rmake.py 的 prebuild() 和 postbuild() 函数
- build() 函数被注释是因为默认构建逻辑已经足够处理大多数情况
- 如果要完全自定义构建流程，可以取消注释 build() 函数并设置 build = "Rmake"

错误配置示例（请避免）:
prebuild = "default", build = "Rmake", postbuild = "default"
"""

def prebuild():
    """预构建阶段 - 在主构建之前执行"""
    print("🔧 执行预构建逻辑...")
    print("💡 如果你想自定义预构建流程，请修改这个函数")
    
    # 示例：检查依赖
    # check_dependencies()
    
    # 示例：清理临时文件
    # cleanup_temp_files()
    
    # 示例：生成配置文件
    # generate_config_files()

def postbuild():
    """后构建阶段 - 在主构建之后执行"""
    print("🔧 执行后构建逻辑...")
    print("💡 如果你想自定义构建后的逻辑，请修改这个函数")
    
    # 示例：复制额外文件
    # copy_additional_files()
    
    # 示例：验证输出
    # validate_output()
    
    # 示例：上传到服务器
    # upload_to_server()

# def build():
#     """
#     主构建逻辑 - 如果要完全自定义构建流程，取消这个函数的注释
#     并在 rmmproject.toml 中设置 build = "Rmake"
#     """
#     print("🏗️ 执行自定义构建逻辑...")
#     
#     # 你的自定义构建代码
#     # 例如：编译代码、打包资源、生成文档等
#     
#     # 注意：如果定义了这个函数，需要自己处理输出文件的生成
#     # 输出文件应该放在 .rmmp/dist/ 目录下
'''