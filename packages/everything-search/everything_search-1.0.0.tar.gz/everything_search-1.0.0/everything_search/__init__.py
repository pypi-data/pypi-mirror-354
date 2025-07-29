#!/usr/bin/env python3
"""
Everything Search - 高性能文件搜索工具

类似于Windows Everything的macOS解决方案，提供快速的文件索引和搜索功能。

主要功能：
- 快速文件索引
- 实时文件系统监控
- 高性能搜索引擎
- 图形用户界面
- 命令行工具

作者: duolabmeng6
仓库: https://github.com/duolabmeng6/everything-for-mac
"""

__version__ = "1.0.0"
__author__ = "duolabmeng6"
__email__ = "1715109585@qq.com"
__license__ = "MIT"

# 导出主要类和函数
from .core.config_manager import ConfigManager
from .core.database import DatabaseManager
from .core.file_indexer import FileIndexer
from .core.search_engine import SearchEngine
from .core.file_watcher import FileWatcher

__all__ = [
    "ConfigManager",
    "DatabaseManager", 
    "FileIndexer",
    "SearchEngine",
    "FileWatcher",
    "__version__",
    "__author__",
    "__email__",
    "__license__",
]
