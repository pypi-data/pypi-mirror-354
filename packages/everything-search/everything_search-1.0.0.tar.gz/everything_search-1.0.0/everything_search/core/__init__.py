"""
Everything Search - 高性能文件搜索工具核心模块
"""

import os
from pathlib import Path

__version__ = "1.0.0"
__author__ = "Everything Search Team"


def get_user_data_dir() -> Path:
    """
    获取用户数据目录

    Returns:
        Path: 用户数据目录路径
    """
    # 检查环境变量自定义路径
    custom_dir = os.environ.get('EVERYTHING_SEARCH_DATA_DIR')
    if custom_dir:
        data_dir = Path(custom_dir).expanduser().resolve()
    else:
        # 使用系统标准数据目录
        home = Path.home()
        if os.name == 'nt':  # Windows
            data_dir = home / 'AppData' / 'Local' / 'EverythingSearch'
        elif os.name == 'posix':
            import platform
            if platform.system() == 'Darwin':  # macOS
                data_dir = home / 'Library' / 'Application Support' / 'EverythingSearch'
            else:  # Linux
                data_dir = home / '.local' / 'share' / 'EverythingSearch'
        else:
            # 默认情况
            data_dir = home / '.everything-search'

    # 确保目录存在
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_default_db_path() -> Path:
    """
    获取默认数据库文件路径

    Returns:
        Path: 数据库文件路径
    """
    return get_user_data_dir() / 'everything_index.db'


def get_default_config_path() -> Path:
    """
    获取默认配置文件路径

    Returns:
        Path: 配置文件路径
    """
    return get_user_data_dir() / 'config.json'





from .config_manager import ConfigManager
from .database import DatabaseManager
from .file_indexer import FileIndexer
from .search_engine import SearchEngine
from .file_watcher import FileWatcher

__all__ = [
    'ConfigManager',
    'DatabaseManager',
    'FileIndexer',
    'SearchEngine',
    'FileWatcher',
    'get_user_data_dir',
    'get_default_db_path',
    'get_default_config_path'
]
