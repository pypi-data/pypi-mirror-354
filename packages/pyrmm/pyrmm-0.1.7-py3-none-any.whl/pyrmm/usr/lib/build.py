from pathlib import Path
from collections.abc import Callable
from typing import Any, TypeVar
import time
import traceback
import shutil
import subprocess

from .base import RmmBaseMeta, RmmBase
from .build_core import RmmBuildCore

F = TypeVar('F', bound=Callable[..., Any])

class RmmBuilderMeta(RmmBaseMeta):
    """Meta class for RMM Builder"""
    
    @property
    def META(cls) -> dict[str, Any]:
        """Get the build metadata from current project."""
        # 延迟导入避免循环导入
        from .project import RmmProject
        
        # 尝试从当前工作目录获取项目配置
        current_path = Path.cwd()
        
        # 向上查找项目根目录（包含 rmmproject.toml 的目录）
        project_path = cls._find_project_root(current_path)
        
        if project_path and RmmProject.is_rmmproject(project_path):
            try:
                project_info = RmmProject.project_info(project_path)
                build_config = project_info.get("build", {
                    "prebuild": "default",
                    "build": "default", 
                    "postbuild": "default",
                })
                if isinstance(build_config, dict):
                    return build_config
            except Exception as e:
                print(f"警告: 读取项目构建配置失败: {e}")
        
        # 如果无法从项目配置读取，返回默认配置
        return {
            "prebuild": "default",
            "build": "default",
            "postbuild": "default",
        }
    
    @classmethod
    def _find_project_root(cls, start_path: Path) -> Path | None:
        """向上查找包含 rmmproject.toml 的项目根目录"""
        current = start_path.resolve()

        # 最多向上查找3级目录，避免无限循环
        for _ in range(3):
            if (current / "rmmproject.toml").exists():
                return current
            
            parent = current.parent
            if parent == current:  # 到达根目录
                break            
            current = parent
        
        return None
    
    def get_config_key(cls) -> str:
        """获取配置键名"""
        return "build"
    
    def get_reserved_key(cls) -> str:
        """获取保留关键字"""
        return "default"
    
    def get_item_config(cls, item_name: str) -> dict[str, Any]:
        """获取指定项目的构建配置"""
        # 延迟导入避免循环导入
        from .project import RmmProject
        
        # 如果是特殊配置项，从META中获取
        if item_name in cls.META:
            return {item_name: cls.META[item_name]}
        
        # 尝试从项目配置获取指定的构建配置项
        current_path = Path.cwd()
        project_path = cls._find_project_root(current_path)
        
        if project_path and RmmProject.is_rmmproject(project_path):
            try:
                project_info = RmmProject.project_info(project_path)
                build_config = project_info.get("build", {})
                if isinstance(build_config, dict) and item_name in build_config:
                    return {item_name: build_config[item_name]}
            except Exception as e:
                print(f"警告: 读取项目构建配置失败: {e}")
        
        # 如果找不到配置项，抛出KeyError
        raise KeyError(f"构建配置项 '{item_name}' 未找到")
    
    def _set_item_config(cls, name: str, value: Any) -> None:
        """设置构建配置项"""
        # 延迟导入避免循环导入
        from .project import RmmProject
        
        current_path = Path.cwd()
        project_path = cls._find_project_root(current_path)
        
        if project_path and RmmProject.is_rmmproject(project_path):
            try:
                # 获取当前项目配置
                project_info = RmmProject.project_info(project_path)
                
                # 确保build配置存在且为字典类型
                if "build" not in project_info:
                    project_info["build"] = {}
                
                build_config = project_info.get("build", {})
                if isinstance(build_config, dict):
                    # 设置配置值
                    build_config[name] = value
                    
                    # 使用 __setattr__ 魔术方法自动保存
                    project_name = project_path.name
                    setattr(RmmProject, project_name, {"build": build_config})
                else:
                    print(f"警告: 构建配置不是字典类型，无法设置")
                    
            except Exception as e:
                print(f"警告: 设置构建配置失败: {e}")
        else:
            print(f"警告: 无法设置构建配置，未找到有效的项目根目录")
    
    def _delete_item_config(cls, name: str) -> None:
        """删除构建配置项"""
        # 延迟导入避免循环导入
        from .project import RmmProject
        
        current_path = Path.cwd()
        project_path = cls._find_project_root(current_path)
        
        if project_path and RmmProject.is_rmmproject(project_path):
            try:
                # 获取当前项目配置
                project_info = RmmProject.project_info(project_path)
                
                # 删除配置项
                build_config = project_info.get("build", {})
                if isinstance(build_config, dict) and name in build_config:
                    del build_config[name]
                    
                    # 使用 __setattr__ 魔术方法自动保存
                    project_name = project_path.name
                    setattr(RmmProject, project_name, {"build": build_config})
                        
            except Exception as e:
                print(f"警告: 删除构建配置失败: {e}")
        else:
            print(f"警告: 无法删除构建配置，未找到有效的项目根目录")

class RmmBuilder(RmmBase, metaclass=RmmBuilderMeta):
    """RMM Builder class - 简化版本，只使用一个 Rmake.py 文件"""
      # 构建脚本缓存
    _build_cache: dict[str, Any] = {}
    _build_mtime: dict[str, float] = {}
    
    # 存储钩子函数
    _prebuilds: list[tuple[str, Callable[..., Any]]] = []
    _postbuilds: list[tuple[str, Callable[..., Any]]] = []
    _custom_build: Callable[..., Any] | None = None
    _build_context: dict[str, Any] = {}
    
    @classmethod
    def reset_hooks(cls):
        """清空所有钩子函数，用于重新构建时清理状态"""
        cls._prebuilds.clear()
        cls._postbuilds.clear()
        cls._custom_build = None
        cls._build_context.clear()
    
    @classmethod
    def clear_cache(cls):
        """清空构建脚本缓存，强制重新加载"""
        cls._build_cache.clear()
        cls._build_mtime.clear()
        print(f"🧹 已清空构建脚本缓存")
        return True
    
    @classmethod
    def load(cls, project_path: Path) -> bool:
        """加载 .rmmp/Rmake.py 文件（如果存在）"""
        # 清空之前的钩子函数
        cls.reset_hooks()
        
        # 使用核心模块加载脚本
        success, module = RmmBuildCore.load_rmake_script(
            project_path, 
            cls._build_cache, 
            cls._build_mtime
        )
        
        if not success:
            return False
        
        # 尝试从模块中获取标准函数
        if hasattr(module, 'prebuild') and callable(getattr(module, 'prebuild')):
            cls._prebuilds.append(('prebuild', getattr(module, 'prebuild')))
        if hasattr(module, 'postbuild') and callable(getattr(module, 'postbuild')):
            cls._postbuilds.append(('postbuild', getattr(module, 'postbuild')))
        if hasattr(module, 'build') and callable(getattr(module, 'build')):
            cls._custom_build = getattr(module, 'build')
        
        return True
    @classmethod
    def build(
        cls, 
        project_name: str | None = None,
        project_path: Path | None = None, 
        output_dir: Path | None = None,
        clean: bool = False,
        debug: bool = False
    ) -> dict[str, Any]:
        """执行构建过程"""
        module_zip: None | Path = None
        start_time = time.time()
        
        try:
            # 如果没有提供project_path但提供了project_name，从配置获取路径
            if project_path is None and project_name:
                from .project import RmmProject
                project_path = RmmProject.project_path(project_name)
            elif project_path is None:
                project_path = Path.cwd()
            
            print(f"🔨 开始构建项目: {project_path}\n")
            
            # 设置默认输出目录到 .rmmp/dist
            if output_dir is None:
                output_dir = project_path / ".rmmp" / "dist"
              # 确保 .rmmp 目录存在
            rmmp_dir = project_path / ".rmmp"
            rmmp_dir.mkdir(exist_ok=True)
            
            # 更新 .gitignore 文件
            RmmBuildCore.update_gitignore(project_path)
            
            # 清理输出目录
            if clean and output_dir.exists():
               print(f"🧹 清理输出目录: {output_dir}")
               shutil.rmtree(output_dir)

            # 确保输出目录存在
            output_dir.mkdir(parents=True, exist_ok=True)

            # 设置构建上下文
            cls._build_context = {
                "project_name": project_name or project_path.name,
                "project_path": project_path,
                "output_dir": output_dir,
                "clean": clean,
                "debug": debug
            }
            # 加载构建脚本
            script_loaded = cls.load(project_path)

            # 获取构建配置
            build_config = cls.META


            if script_loaded:
                print(f"✅ 找到 Rmake.py，已加载自定义构建逻辑")
            else:
                print(f"ℹ️  未找到 Rmake.py，使用配置中的构建逻辑")
        
            # 执行 prebuild 阶段
            prebuild_config = build_config.get("prebuild", "default")
            if prebuild_config != "default":
                
                print(f"🔧 执行预构建阶段...")
                if prebuild_config == "Rmake":
                    # 执行 Rmake.py 中的 prebuild 钩子
                    if cls._prebuilds:
                        for hook_name, hook_func in cls._prebuilds:
                            
                            print(f"  ➤ 执行预构建钩子: {hook_name}")
                            hook_func()
                else:
                    # 执行自定义可执行文件
                    if not RmmBuildCore.execute_script(prebuild_config, "prebuild", project_path):
                        raise Exception(f"预构建脚本执行失败: {prebuild_config}")
            elif cls._prebuilds:
                # 即使是 default，如果有 Rmake.py 中的 prebuild 钩子，也要执行
                
                print(f"🔧 执行 {len(cls._prebuilds)} 个预构建钩子...")
                for hook_name, hook_func in cls._prebuilds:
                    
                    print(f"  ➤ 执行预构建钩子: {hook_name}")
                    hook_func()
              # 执行构建阶段
            build_config_type = build_config.get("build", "default")
            if build_config_type == "default":
                if cls._custom_build:
                    
                    print(f"🎯 执行 Rmake.py 中的自定义构建逻辑...")
                    cls._custom_build()                
                else:
                    
                    print(f"🏗️  执行默认构建逻辑...")
                    module_zip: None | Path = RmmBuildCore.default_build(project_path, output_dir)
            elif build_config_type == "Rmake":
                if cls._custom_build:
                    
                    print(f"🎯 执行 Rmake.py 中的自定义构建逻辑...")
                    cls._custom_build()                
                else:
                    
                    print(f"⚠️  配置要求使用 Rmake 构建，但未找到 build 函数，使用默认构建...")
                    RmmBuildCore.default_build(project_path, output_dir)
            else:
                # 执行自定义可执行文件
                
                print(f"🔧 执行自定义构建脚本...\n")
                if not RmmBuildCore.execute_script(build_config_type, "build", project_path):
                    raise Exception(f"构建脚本执行失败: {build_config_type}")
            
            # 执行 postbuild 阶段
            postbuild_config = build_config.get("postbuild", "default")
            if postbuild_config != "default":
                
                print(f"🔧 执行后构建阶段...\n")
                if postbuild_config == "Rmake":
                    # 执行 Rmake.py 中的 postbuild 钩子
                    if cls._postbuilds:
                        for hook_name, hook_func in cls._postbuilds:
                            
                            print(f"  ➤ 执行后构建钩子: {hook_name}")
                            hook_func()
                else:
                    # 执行自定义可执行文件
                    if not RmmBuildCore.execute_script(postbuild_config, "postbuild", project_path):
                        raise Exception(f"后构建脚本执行失败: {postbuild_config}")
            elif cls._postbuilds:
                # 即使是 default，如果有 Rmake.py 中的 postbuild 钩子，也要执行
                
                print(f"🔧 执行 {len(cls._postbuilds)} 个后构建钩子...")
                for hook_name, hook_func in cls._postbuilds:
                    
                    print(f"  ➤ 执行后构建钩子: {hook_name}")
                    hook_func()
              # 计算构建时间
            build_time = time.time() - start_time
            
            # 查找输出文件
            zip_files = list(output_dir.glob("*.zip"))
            tar_files = list(output_dir.glob("*.tar.gz"))
            all_output_files = zip_files + tar_files
            result: dict[str, Any] = {
                "success": True,
                "build_time": build_time,
                "module_zip": module_zip,
            }
            
            if all_output_files:
                result["output_files"] = [str(f) for f in all_output_files]
            
            
                print(f"✅ 构建完成，耗时 {build_time:.2f} 秒")
            
            return result
            
        except Exception as e:
            build_time = time.time() - start_time
            error_msg = str(e)
            
            if debug:
                error_msg = f"{error_msg}\n详细错误信息:\n{traceback.format_exc()}"
            
            
                print(f"❌ 构建失败，耗时 {build_time:.2f} 秒")
                print(f"错误: {error_msg}")
            
            return {
                "success": False,
                "build_time": build_time,
                "error": error_msg
            }    
    @classmethod
    def is_valid_item(cls, item_name: str) -> bool:
        """检查指定构建配置项是否有效"""
        valid_items = {"prebuild", "build", "postbuild"}
        return item_name in valid_items
    @classmethod
    def get_sync_prompt(cls, item_name: str) -> str:
        """获取同步提示信息"""
        return f"构建配置项 '{item_name}' 已过期或无效，是否重置为默认值？"    

    @classmethod
    def build_from_git(cls, source: str, r_project_path: str = "."):
        """从Git仓库构建项目
        source: Git仓库URL
        r_project_path: 项目路径(相对于仓库路径)，默认在仓库根目录下 : .
        """
        from .fs import RmmFileSystem
        # 从url中提取项目名称
        repo_name = source.split("/")[-1].replace(".git", "")
        
        # 使用固定的目录名（不再使用时间戳）
        tmp_base = RmmFileSystem.TMP / "build"
        tmp = tmp_base / repo_name
        
        print(f"🔧 使用构建目录: {tmp}")
        
        # 确保父目录存在
        tmp_base.mkdir(parents=True, exist_ok=True)
          # 如果目录已存在，尝试更新而不是删除重建
        should_clone = True
        if tmp.exists():
            print(f"📁 检测到已存在的构建目录: {tmp}")
            
            # 检查是否是有效的Git仓库
            git_dir = tmp / ".git"
            if git_dir.exists():
                print(f"🔄 检测到Git仓库，尝试更新现有代码...")
                try:
                    # 检查远程URL是否匹配
                    result = subprocess.run(
                        ["git", "-C", str(tmp), "remote", "get-url", "origin"],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    
                    if result.returncode == 0:
                        current_url = result.stdout.strip()
                        # 简单的URL比较（去除.git后缀）
                        current_clean = current_url.rstrip('/').replace('.git', '')
                        source_clean = source.rstrip('/').replace('.git', '')
                        if current_clean == source_clean:
                            print(f"✅ 远程URL匹配，执行 git pull 更新...")
                            
                            # 执行 git pull
                            pull_result = subprocess.run(
                                ["git", "-C", str(tmp), "pull"],
                                timeout=300  # 5分钟超时
                            )
                            
                            if pull_result.returncode == 0:
                                print(f"✅ 更新成功")
                                should_clone = False
                            else:
                                print(f"⚠️ Git pull 失败，返回码: {pull_result.returncode}")
                                print(f"将重新克隆仓库...")
                        else:
                            print(f"⚠️ 远程URL不匹配:")
                            print(f"   当前: {current_url}")
                            print(f"   目标: {source}")
                            print(f"将重新克隆仓库...")
                    else:
                        print(f"⚠️ 无法获取远程URL: {result.stderr}")
                        print(f"将重新克隆仓库...")
                        
                except subprocess.TimeoutExpired:
                    print(f"⚠️ Git 操作超时，将重新克隆仓库...")
                except Exception as e:
                    print(f"⚠️ Git 操作失败: {e}")
                    print(f"将重新克隆仓库...")
              # 如果需要重新克隆，先清理目录
            if should_clone:
                print(f"🧹 清理旧目录以重新克隆...")
                try:
                    RmmBuildCore.cleanup_directory(tmp)
                    print(f"✅ 已清理旧的构建目录")
                except Exception as e:
                    print(f"⚠️ 清理构建目录失败: {e}")
                    print("尝试使用备份目录...")
                    import time
                    timestamp = int(time.time())
                    tmp = tmp_base / f"{repo_name}_{timestamp}"
                    print(f"🔧 使用备份构建目录: {tmp}")
          # 检查网络连接
        print(f"🌐 检查网络连接...")
        if not RmmBuildCore.check_network_connection(source):
            print(f"❌ 无法连接到Git服务器，请检查:")
            print(f"   1. 网络连接是否正常")
            print(f"   2. 代理设置是否正确")
            print(f"   3. 防火墙是否阻止了连接")
            if "github.com" in source:
                print(f"   💡 如果在中国大陆，可能需要配置代理访问GitHub")
                print(f"   💡 可以尝试使用镜像站点或设置HTTP/HTTPS代理")
            return False
          # 检查临时构建目录是否太大，如果超过 1GB 就清理
        RmmBuildCore.manage_temp_directory_size(tmp_base, repo_name)
        try:            # 如果需要克隆，执行克隆操作
            if should_clone:
                # 克隆仓库到临时目录
                print(f"📥 正在克隆仓库: {source}")
                result = subprocess.run(
                    ["git", "clone", "--depth", "1", source, str(tmp)],
                    timeout=300  # 5分钟超时
                )
                
                if result.returncode != 0:
                    print(f"❌ 克隆失败，返回码: {result.returncode}")
                    return False
                    
                print(f"✅ 克隆成功")
            
            # 构建项目路径
            project_path = tmp / r_project_path if r_project_path != "." else tmp
            
            print(f"📁 项目路径: {project_path}")
            
            if not project_path.exists():
                print(f"❌ 项目路径不存在: {project_path}")
                # 列出tmp目录的内容以帮助调试
                if tmp.exists():
                    print(f"📋 {tmp} 目录内容:")
                    for item in tmp.iterdir():
                        print(f"  - {item.name}{'/' if item.is_dir() else ''}")
                return False
            
            # 检查是否是有效的RMM项目
            from .project import RmmProject
            if not RmmProject.is_rmmproject(project_path):
                print(f"⚠️ 警告: {project_path} 不是一个有效的RMM项目")
                print("将使用默认构建逻辑...")
            
            print(f"🔨 开始构建项目: {repo_name}")
            
            # 创建构建输出目录
            output_dir = tmp_base / "dist" / repo_name
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 执行构建
            build_result = cls.build(
                project_name=repo_name,
                project_path=project_path,
                output_dir=output_dir,
                clean=True,
                debug=False
            )

            if not build_result.get("success", False):
                print(f"❌ 构建失败: {build_result.get('error', '未知错误')}")
                return False

            module_zip = build_result.get("module_zip", None)
            if not module_zip:
                print(f"❌ 构建完成但没有生成模块包")
                return False
            
            print(f"✅ 构建成功，生成的模块包: {module_zip}")
            return module_zip
            
        except subprocess.TimeoutExpired:
            print(f"❌ 克隆超时（超过5分钟）")
            return False
        except Exception as e:
            print(f"❌ 构建过程中发生错误: {e}")
            return False          
        finally:            # 清理临时目录（可选，也可以保留用于调试）
            if tmp.exists():
                try:
                    RmmBuildCore.cleanup_directory(tmp)
                    print(f"🧹 已清理临时目录: {tmp}")
                except Exception as e:
                    print(f"⚠️ 清理临时目录失败: {e}")
                    print(f"   临时文件将保留在: {tmp}")
                    print("   可以手动删除或下次构建时会自动清理")