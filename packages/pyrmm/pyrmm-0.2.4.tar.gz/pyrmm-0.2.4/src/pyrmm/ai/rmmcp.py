from pathlib import Path
import os
import toml
from typing import Any
from mcp.server.fastmcp import FastMCP

class RmMcp(FastMCP):
    """
    RmMcp class that extends FastMCP with configuration management capabilities.
    """
    
    def __init__(self, name: str = "RmMcp", host: str = "localhost", port: int = 8000, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.host = host
        self.port = port
        self.cache: dict[str, Any] = {
            "username": "LIghtJUNction[dev]",
            "email": "lightjuntion.me@gmail.com",
            "version": "0.2.3",
            "projects": {}
        }
        self._cache_last_modified: float = 0

    @property
    def ROOT(self) -> Path:
        """Get the root directory for RMM configuration."""
        return Path(os.getenv("RMM_ROOT", Path().home() / "data" / "adb" / ".rmm"))

    @property
    def META_FILE(self) -> Path:
        """Get the path to the metadata TOML file."""
        return self.ROOT / "meta.toml"

    @property
    def _true_last_modified(self) -> float:
        """Get the actual last modified time of the metadata file."""
        try:
            return self.META_FILE.stat().st_mtime
        except FileNotFoundError:
            return 0

    @property
    def is_changed(self) -> bool:
        """
        Check if the cache has changed since the last load.
        """
        true_modified = self._true_last_modified
        if self._cache_last_modified != true_modified:
            self._cache_last_modified = true_modified
            return True
        return False

    @property
    def META(self) -> dict[str, Any]:
        """
        Get the metadata from the TOML file, loading it if necessary.
        """
        if self._cache_last_modified == 0 or self._true_last_modified == 0 or self.is_changed:
            try:
                with open(self.META_FILE, "r", encoding="utf-8") as f:
                    self.cache = toml.load(f)
            except FileNotFoundError:
                # If file doesn't exist, create the directory and use default cache
                self.ROOT.mkdir(parents=True, exist_ok=True)        
        return self.cache
    
    @property
    def projects(self) -> dict[str, Any]:
        """
        Get the projects from the metadata.
        """
        return self.META.get("projects", {"tip": "暂未发现任何模块，提示用户使用rmm init 新建一个项目"})
    
    def project_path(self, project_id: str) -> Path:
        """
        Get the path of a project.
        """
        project_path = self.projects.get(project_id)
        if project_path:
            return Path(project_path)
        else:
            return Path("")

    def project_info(self, project_id: str) -> dict[str, Any]:
        """
        Get the project information from the metadata.
        """
        project_path = self.project_path(project_id)
        project_info_file: Path = project_path / "rmmproject.toml"
        if project_info_file.exists():
            try:
                with open(project_info_file, "r", encoding="utf-8") as f:
                    return toml.load(f)
            except Exception as e:
                print(f"读取项目 {project_id} 信息失败: {e}")
                return {}
        else:
            print(f"项目 {project_id} 的信息文件不存在: {project_info_file}")
            return {f"项目 {project_id} 的信息文件不存在": str(project_info_file)}

mcp = RmMcp("RmMcp")
#region tool

@mcp.tool()
def getRMMETA():
    """
    Get the metadata from the RMM (Magisk module project management).
    """
    return mcp.META

@mcp.tool()
def getRMProjects():
    """
    Get the projects from the RMM (Magisk module project management).
    """
    return mcp.projects

@mcp.tool()
def getRMMRoot():
    """
    Get the root directory for RMM configuration.
    """
    return str(mcp.ROOT)

@mcp.tool()
def getProjectInfo(project_name: str ):
    """
    Get information about a specific project.
    
    Args:
        project_name: The name of the project to retrieve information for.
    
    Returns:
        A dictionary containing project information or an error message if the project does not exist.
    """
    projects = mcp.projects
    if project_name in projects:
        project_path: Path = mcp.project_path(project_name)
        if project_path.exists():
            project_info = mcp.project_info(project_name)
            return project_info
        else:
            return {"error": f"项目 {project_name} 的路径不存在: {project_path}"}

@mcp.tool()
def initNewProject(project_name: str, template: str = "basic", project_path: str | None = None):
    """
    Initialize a new RMM project using rmm init command.
    
    Args:
        project_name: The name of the new project
        template: Project template (basic, library, ravd)
        project_path: Optional custom project path
    
    Returns:
        Result of the rmm init command
    """
    import subprocess
    import sys
    
    try:
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "init", project_name, "--template", template]
        if project_path:
            cmd.extend(["--path", project_path])
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(mcp.ROOT.parent))
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {"error": f"初始化项目失败: {str(e)}"}

@mcp.tool()
def buildProject(project_name: str | None = None, debug: bool = False, skip_shellcheck: bool = False):
    """
    Build a RMM project using rmm build command.
    
    Args:
        project_name: Optional project name (if not provided, builds current directory)
        debug: Enable debug mode
        skip_shellcheck: Skip shell script checking
    
    Returns:
        Result of the rmm build command
    """
    import subprocess
    import sys
    
    try:
        projects = mcp.projects
        if project_name and project_name in projects:
            project_path = mcp.project_path(project_name)
            work_dir = str(project_path)
        else:
            work_dir = str(mcp.ROOT.parent)
        
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "build"]
        if debug:
            cmd.append("--debug")
        if skip_shellcheck:
            cmd.append("--skip-shellcheck")
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "work_dir": work_dir
        }
    except Exception as e:
        return {"error": f"构建项目失败: {str(e)}"}

@mcp.tool()
def testModule(project_name: str | None = None, device_id: str | None = None, interactive: bool = False):
    """
    Test a module on device using rmm test command.
    
    Args:
        project_name: Optional project name
        device_id: Target device ID (adb device)
        interactive: Enable interactive mode
    
    Returns:
        Result of the rmm test command
    """
    import subprocess
    import sys
    
    try:
        projects = mcp.projects
        if project_name and project_name in projects:
            project_path = mcp.project_path(project_name)
            work_dir = str(project_path)
        else:
            work_dir = str(mcp.ROOT.parent)
        
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "test"]
        if device_id:
            cmd.extend(["--device", device_id])
        if interactive:
            cmd.append("--interactive")
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "work_dir": work_dir
        }
    except Exception as e:
        return {"error": f"测试模块失败: {str(e)}"}

@mcp.tool()
def publishRelease(project_name: str | None = None, draft: bool = False, prerelease: bool = False):
    """
    Publish a release to GitHub using rmm publish command.
    
    Args:
        project_name: Optional project name
        draft: Create as draft release
        prerelease: Mark as prerelease
    
    Returns:
        Result of the rmm publish command
    """
    import subprocess
    import sys
    
    try:
        projects = mcp.projects
        if project_name and project_name in projects:
            project_path = mcp.project_path(project_name)
            work_dir = str(project_path)
        else:
            work_dir = str(mcp.ROOT.parent)
        
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "publish"]
        if draft:
            cmd.append("--draft")
        if prerelease:
            cmd.append("--prerelease")
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "work_dir": work_dir
        }
    except Exception as e:
        return {"error": f"发布项目失败: {str(e)}"}

@mcp.tool()
def listDevices():
    """
    List connected ADB devices using rmm device list command.
    
    Returns:
        List of connected devices
    """
    import subprocess
    import sys
    
    try:
        # 执行命令
        cmd = [sys.executable, "-m", "pyrmm", "device", "list"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {"error": f"获取设备列表失败: {str(e)}"}

@mcp.tool()
def installModule(project_name: str | None = None, device_id: str | None = None):
    """
    Install module to device using rmm device install command.
    
    Args:
        project_name: Optional project name
        device_id: Target device ID
    
    Returns:
        Result of the installation
    """
    import subprocess
    import sys
    
    try:
        projects = mcp.projects
        if project_name and project_name in projects:
            project_path = mcp.project_path(project_name)
            work_dir = str(project_path)
        else:
            work_dir = str(mcp.ROOT.parent)
        
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "device", "install"]
        if device_id:
            cmd.extend(["--device", device_id])
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "work_dir": work_dir
        }
    except Exception as e:
        return {"error": f"安装模块失败: {str(e)}"}

@mcp.tool()
def checkProjectSyntax(project_name: str | None = None):
    """
    Check project syntax using rmm check command.
    
    Args:
        project_name: Optional project name
    
    Returns:
        Result of syntax checking
    """
    import subprocess
    import sys
    
    try:
        projects = mcp.projects
        if project_name and project_name in projects:
            project_path = mcp.project_path(project_name)
            work_dir = str(project_path)
        else:
            work_dir = str(mcp.ROOT.parent)
        
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "check"]
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "work_dir": work_dir
        }
    except Exception as e:
        return {"error": f"语法检查失败: {str(e)}"}

@mcp.tool()
def getRMMConfig():
    """
    Get RMM configuration using rmm config list command.
    
    Returns:
        Current RMM configuration
    """
    import subprocess
    import sys
    
    try:
        # 执行命令
        cmd = [sys.executable, "-m", "pyrmm", "config", "list"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {"error": f"获取配置失败: {str(e)}"}

@mcp.tool()
def setRMMConfig(key: str, value: str):
    """
    Set RMM configuration using rmm config set command.
    
    Args:
        key: Configuration key
        value: Configuration value
    
    Returns:
        Result of setting configuration
    """
    import subprocess
    import sys
    
    try:
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "config", "set", key, value]
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {"error": f"设置配置失败: {str(e)}"}












@mcp.tool()
def syncProjects():
    """
    Sync projects metadata using rmm sync command.
    
    Returns:
        Result of syncing projects
    """
    import subprocess
    import sys
    
    try:
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "sync"]
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {"error": f"同步项目失败: {str(e)}"}

@mcp.tool()
def cleanProject(project_name: str | None = None, deep: bool = False):
    """
    Clean project build artifacts using rmm clean command.
    
    Args:
        project_name: Optional project name
        deep: Perform deep clean (remove all build artifacts)
    
    Returns:
        Result of cleaning project
    """
    import subprocess
    import sys
    
    try:
        projects = mcp.projects
        if project_name and project_name in projects:
            project_path = mcp.project_path(project_name)
            work_dir = str(project_path)
        else:
            work_dir = str(mcp.ROOT.parent)
        
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "clean"]
        if deep:
            cmd.append("--deep")
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "work_dir": work_dir
        }
    except Exception as e:
        return {"error": f"清理项目失败: {str(e)}"}

@mcp.tool()
def runCustomScript(project_name: str | None = None, script_type: str = "service"):
    """
    Run custom script in project using rmm run command.
    
    Args:
        project_name: Optional project name
        script_type: Type of script to run (service, post_fs_data, late_start)
    
    Returns:
        Result of running script
    """
    import subprocess
    import sys
    
    try:
        projects = mcp.projects
        if project_name and project_name in projects:
            project_path = mcp.project_path(project_name)
            work_dir = str(project_path)
        else:
            work_dir = str(mcp.ROOT.parent)
        
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "run", script_type]
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=work_dir)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "work_dir": work_dir
        }
    except Exception as e:
        return {"error": f"运行脚本失败: {str(e)}"}

@mcp.tool()
def getDeviceInfo(device_id: str | None = None):
    """
    Get detailed information about connected device.
    
    Args:
        device_id: Optional device ID (if not provided, uses first available device)
    
    Returns:
        Device information and status
    """
    import subprocess
    import sys
    
    try:
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "device", "info"]
        if device_id:
            cmd.extend(["--device", device_id])
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {"error": f"获取设备信息失败: {str(e)}"}

@mcp.tool()
def generateCompletion(shell: str = "powershell"):
    """
    Generate shell completion scripts using rmm completion command.
    
    Args:
        shell: Target shell (bash, zsh, fish, powershell)
    
    Returns:
        Generated completion script
    """
    import subprocess
    import sys
    
    try:
        # 构建命令
        cmd = [sys.executable, "-m", "pyrmm", "completion", shell]
        
        # 执行命令
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "command": " ".join(cmd),
            "shell": shell
        }
    except Exception as e:
        return {"error": f"生成补全脚本失败: {str(e)}"}

# Resources for providing documentation and help
@mcp.resource("docs://rmm-cli-help")
def rmmHelp():
    """
    RMM (Root Module Manager) 完整帮助文档和使用指南
    """
    from pyrmm.ai.resources import RMMCLIHELP
    return RMMCLIHELP

@mcp.resource("docs://magisk-module-guide")
def magiskModuleGuide():
    """
    Magisk 模块开发指南和最佳实践
    """
    from pyrmm.ai.resources import MODULEDEVGUIDE
    return MODULEDEVGUIDE

@mcp.resource("docs://shell-script-best-practices")
def shellScriptBestPractices():
    """
    Shell 脚本编写最佳实践和 ShellCheck 规范
    """
    from pyrmm.ai.resources import SHELLSCRIPTBESTPRACTICES
    return SHELLSCRIPTBESTPRACTICES

def start_mcp_server(transport: str = "stdio", host: str = "localhost", port: int = 8000, verbose: bool = False):
    """
    启动 MCP 服务器的入口函数
    
    Args:
        transport: 传输方式 ("stdio" 或 "sse")
        host: 服务器主机地址 (仅用于 sse 模式)
        port: 服务器端口 (仅用于 sse 模式)
        verbose: 是否启用详细日志
    """
    
    #region 注册mcp功能！！！
    mcp.host = host
    mcp.port = port
    print(f"🚀 启动 RMM MCP 服务器...")
    print(f"📡 传输方式: {transport}")
    if transport == "sse":
        print(f"📍 地址: {host}:{port}")
    try:
        if transport == "stdio":
            mcp.run(transport="stdio")
        elif transport == "sse":
            mcp.run(transport="sse")
        else:
            raise ValueError(f"不支持的传输方式: {transport}")
    except KeyboardInterrupt:
        if verbose:
            print("\n👋 MCP 服务器已停止")
    except Exception as e:
        if verbose:
            print(f"❌ MCP 服务器错误: {e}")
        raise

if __name__ == "__main__":
    start_mcp_server()