#!/usr/bin/env python3
"""
高性能配置管理器
优化特性：
- 配置缓存避免重复IO
- 延迟加载和写入合并
- 路径规范化和验证
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, asdict
import threading
import time

from . import get_default_config_path


@dataclass
class IndexConfig:
    """索引配置数据类"""
    directories: List[str]
    exclude_dirs: List[str]
    exclude_extensions: List[str]
    max_file_size_mb: int
    follow_symlinks: bool
    index_hidden_files: bool


@dataclass
class SearchConfig:
    """搜索配置数据类"""
    case_sensitive: bool
    fuzzy_search: bool
    max_results: int
    result_cache_size: int


@dataclass
class PerformanceConfig:
    """性能配置数据类"""
    max_workers: int
    batch_size: int
    memory_limit_mb: int
    index_chunk_size: int


class ConfigManager:
    """高性能配置管理器"""

    def __init__(self, config_path: Optional[str] = None):
        # 如果没有指定路径，使用默认的用户数据目录路径
        if config_path is None:
            self.config_path = get_default_config_path()
        else:
            self.config_path = Path(config_path).resolve()

        self._config_cache: Optional[Dict[str, Any]] = None
        self._cache_lock = threading.RLock()
        self._last_modified = 0
        self._write_pending = False
        self._write_timer: Optional[threading.Timer] = None
        
        # 默认配置
        self._default_config = {
            "index": {
                "directories": [
                    str(Path.home() / "Desktop"),
                    str(Path.home() / "Downloads"),
                    str(Path.home() / "Documents")
                ],
                "exclude_dirs": [
                    ".git", ".svn", ".hg",
                    "node_modules", "__pycache__", ".venv", "venv",
                    ".pytest_cache", ".mypy_cache", ".tox",
                    "build", "dist", ".egg-info",
                    "Trash", ".Trash", ".DS_Store"
                ],
                "exclude_extensions": [
                    ".tmp", ".temp", ".log", ".cache",
                    ".pyc", ".pyo", ".pyd", ".so", ".dylib",
                    ".o", ".obj", ".exe", ".dll"
                ],
                "max_file_size_mb": 1024,
                "follow_symlinks": False,
                "index_hidden_files": False
            },
            "search": {
                "case_sensitive": False,
                "fuzzy_search": True,
                "max_results": 1000,
                "result_cache_size": 10000
            },
            "performance": {
                "max_workers": min(32, (os.cpu_count() or 1) * 2),
                "batch_size": 1000,
                "memory_limit_mb": 512,
                "index_chunk_size": 10000
            }
        }
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件，带缓存优化"""
        with self._cache_lock:
            try:
                # 检查文件修改时间
                if self.config_path.exists():
                    current_mtime = self.config_path.stat().st_mtime
                    if self._config_cache is not None and current_mtime <= self._last_modified:
                        return self._config_cache
                    
                    # 文件已修改，重新加载
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                    
                    # 合并默认配置
                    merged_config = self._merge_configs(self._default_config, config)
                    
                    self._config_cache = merged_config
                    self._last_modified = current_mtime
                    return merged_config
                else:
                    # 配置文件不存在，使用默认配置
                    self._config_cache = self._default_config.copy()
                    return self._config_cache
                    
            except (json.JSONDecodeError, OSError) as e:
                print(f"⚠️  配置文件加载失败，使用默认配置: {e}")
                self._config_cache = self._default_config.copy()
                return self._config_cache
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """递归合并配置，用户配置覆盖默认配置"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def _delayed_save(self):
        """延迟保存配置，避免频繁IO"""
        if self._write_timer:
            self._write_timer.cancel()
        
        def save_now():
            with self._cache_lock:
                if self._write_pending and self._config_cache:
                    try:
                        # 确保目录存在
                        self.config_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        # 原子写入
                        temp_path = self.config_path.with_suffix('.tmp')
                        with open(temp_path, 'w', encoding='utf-8') as f:
                            json.dump(self._config_cache, f, indent=2, ensure_ascii=False)
                        
                        temp_path.replace(self.config_path)
                        self._last_modified = self.config_path.stat().st_mtime
                        self._write_pending = False
                        
                    except OSError as e:
                        print(f"⚠️  配置保存失败: {e}")
        
        self._write_timer = threading.Timer(1.0, save_now)
        self._write_timer.start()
    
    def get_index_config(self) -> IndexConfig:
        """获取索引配置"""
        config = self._load_config()
        index_data = config["index"]
        
        # 路径规范化
        directories = [str(Path(d).expanduser().resolve()) for d in index_data["directories"]]
        
        return IndexConfig(
            directories=directories,
            exclude_dirs=index_data["exclude_dirs"],
            exclude_extensions=index_data["exclude_extensions"],
            max_file_size_mb=index_data["max_file_size_mb"],
            follow_symlinks=index_data["follow_symlinks"],
            index_hidden_files=index_data["index_hidden_files"]
        )
    
    def get_search_config(self) -> SearchConfig:
        """获取搜索配置"""
        config = self._load_config()
        search_data = config["search"]
        
        return SearchConfig(
            case_sensitive=search_data["case_sensitive"],
            fuzzy_search=search_data["fuzzy_search"],
            max_results=search_data["max_results"],
            result_cache_size=search_data["result_cache_size"]
        )
    
    def get_performance_config(self) -> PerformanceConfig:
        """获取性能配置"""
        config = self._load_config()
        perf_data = config["performance"]
        
        return PerformanceConfig(
            max_workers=perf_data["max_workers"],
            batch_size=perf_data["batch_size"],
            memory_limit_mb=perf_data["memory_limit_mb"],
            index_chunk_size=perf_data["index_chunk_size"]
        )
    
    def update_config(self, section: str, updates: Dict[str, Any]):
        """更新配置节"""
        with self._cache_lock:
            config = self._load_config()
            if section in config:
                config[section].update(updates)
                self._config_cache = config
                self._write_pending = True
                self._delayed_save()
    
    def add_index_directory(self, directory: str):
        """添加索引目录"""
        dir_path = str(Path(directory).expanduser().resolve())
        config = self._load_config()
        if dir_path not in config["index"]["directories"]:
            config["index"]["directories"].append(dir_path)
            self._config_cache = config
            self._write_pending = True
            self._delayed_save()
    
    def remove_index_directory(self, directory: str):
        """移除索引目录"""
        dir_path = str(Path(directory).expanduser().resolve())
        config = self._load_config()
        if dir_path in config["index"]["directories"]:
            config["index"]["directories"].remove(dir_path)
            self._config_cache = config
            self._write_pending = True
            self._delayed_save()
    
    def save_default_config(self):
        """保存默认配置到文件"""
        with self._cache_lock:
            self._config_cache = self._default_config.copy()
            self._write_pending = True
            self._delayed_save()
    
    def validate_directories(self) -> List[str]:
        """验证索引目录，返回无效目录列表"""
        config = self.get_index_config()
        invalid_dirs = []
        
        for directory in config.directories:
            path = Path(directory)
            if not path.exists() or not path.is_dir():
                invalid_dirs.append(directory)
        
        return invalid_dirs
    
    def cleanup(self):
        """清理资源"""
        if self._write_timer:
            self._write_timer.cancel()
            # 立即保存待写入的配置
            if self._write_pending:
                self._delayed_save()
