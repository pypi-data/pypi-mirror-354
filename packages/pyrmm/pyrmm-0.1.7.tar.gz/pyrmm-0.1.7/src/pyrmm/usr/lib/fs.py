import os
from pathlib import Path
from typing import Literal
import shutil

class RmmFileSystemMeta(type):
    @property
    def ROOT(cls) -> Path:
        """Return the root path of the RMM file system."""
        return Path(os.getenv('RMM_ROOT', Path().home() / "data" / "adb" / ".rmm" )).resolve()
    
    @property
    def TMP(cls) -> Path:
        """Return the temporary directory path of the RMM file system."""
        return cls.ROOT / 'tmp'
    
    @property
    def CACHE(cls) -> Path:
        """Return the cache directory path of the RMM file system."""
        return cls.ROOT / 'cache'

    @property
    def DATA(cls) -> Path:
        """Return the data directory path of the RMM file system."""
        return cls.ROOT / 'data'

    @property
    def BIN(cls) -> Path:
        """Return the binary directory path of the RMM file system."""
        return cls.ROOT / 'bin'

    @property
    def META(cls) -> Path:
        """Return the metadata directory path of the RMM file system."""
        return cls.ROOT / 'meta.toml'

    def __getattr__(cls, item: str):
        """Get an attribute from the RMM file system."""
        with open(cls.META, 'r') as f:
            import toml
            meta = toml.load(f)
        if item in meta["projects"]:
            return Path(meta["projects"][item])
        raise AttributeError(f"'{cls.__name__}' object has no attribute '{item}'!!!")
class RmmFileSystem(metaclass=RmmFileSystemMeta):
    """RMM File System class"""
    
    _path_initialized = False
    
    @classmethod
    def init(cls):
        """Ensure that all necessary directories exist."""
        cls.ROOT.mkdir(parents=True, exist_ok=True)
        cls.TMP.mkdir(parents=True, exist_ok=True)
        cls.CACHE.mkdir(parents=True, exist_ok=True)
        cls.DATA.mkdir(parents=True, exist_ok=True)
        cls.BIN.mkdir(parents=True, exist_ok=True)
        cls.META.touch(exist_ok=True)
        
        # 初始化 PATH 环境变量
        cls._init_path()
    
    @classmethod
    def _init_path(cls):
        """将 BIN 目录添加到当前进程的 PATH 环境变量，设置高优先级"""
        if cls._path_initialized:
            return
            
        bin_path = str(cls.BIN)
        current_path = os.environ.get('PATH', '')
        
        # 检查 BIN 路径是否已经在 PATH 中
        path_list = current_path.split(os.pathsep)
        
        # 如果已存在，先移除（避免重复）
        if bin_path in path_list:
            path_list.remove(bin_path)
        
        # 将 BIN 目录添加到 PATH 的最前面（高优先级）
        path_list.insert(0, bin_path)
        
        # 更新环境变量
        os.environ['PATH'] = os.pathsep.join(path_list)
        
        cls._path_initialized = True
        print(f"✅ RMM BIN 目录已添加到 PATH (高优先级): {bin_path}")
    
    @classmethod
    def ensure_bin_in_path(cls):
        """确保 BIN 目录在 PATH 中（可手动调用）"""
        cls._init_path()

    @classmethod
    def _remove_bin_from_path(cls):
        """从 PATH 环境变量中移除 BIN 目录"""
        bin_path = str(cls.BIN)
        current_path = os.environ.get('PATH', '')
        path_list = current_path.split(os.pathsep)
        
        # 移除所有匹配的 BIN 路径
        while bin_path in path_list:
            path_list.remove(bin_path)
        
        # 更新环境变量
        os.environ['PATH'] = os.pathsep.join(path_list)
        cls._path_initialized = False
        print(f"🗑️  RMM BIN 目录已从 PATH 中移除: {bin_path}")

    @classmethod
    def rm(cls, dir: Literal["ROOT","DATA","TMP","CACHE","META","BIN"] = "TMP"):
        """Remove the RMM DIRS."""
        # 如果要删除 BIN 目录，先从 PATH 中移除
        if dir == "BIN":
            cls._remove_bin_from_path()
        
        match dir:
            case "ROOT":
                shutil.rmtree(cls.ROOT, ignore_errors=True)
                # 删除 ROOT 时也要清理 PATH
                cls._remove_bin_from_path()
            case "DATA":
                shutil.rmtree(cls.DATA, ignore_errors=True)
            case "TMP":
                shutil.rmtree(cls.TMP, ignore_errors=True)
            case "CACHE":
                shutil.rmtree(cls.CACHE, ignore_errors=True)
            case "META":
                cls.META.unlink(missing_ok=True)
            case "BIN":
                shutil.rmtree(cls.BIN, ignore_errors=True)
            case _:
                raise ValueError(f"Unknown directory: {dir}")