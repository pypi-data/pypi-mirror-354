#!/usr/bin/env python3
"""
高性能文件索引器
优化特性：
- 多线程并发扫描
- 增量索引和变更检测
- 内存优化的批处理
- 智能跳过和过滤
"""

import os
import time
import threading
from pathlib import Path
from typing import List, Set, Optional, Callable, Iterator
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
import hashlib

from .config_manager import ConfigManager, IndexConfig
from .database import DatabaseManager, FileRecord


@dataclass
class IndexProgress:
    """索引进度信息"""
    total_files: int = 0
    processed_files: int = 0
    current_path: str = ""
    start_time: float = 0
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class FileIndexer:
    """高性能文件索引器"""
    
    def __init__(self, config_manager: ConfigManager, db_manager: DatabaseManager):
        self.config_manager = config_manager
        self.db_manager = db_manager
        self._stop_event = threading.Event()
        self._progress_callback: Optional[Callable[[IndexProgress], None]] = None
        
    def set_progress_callback(self, callback: Callable[[IndexProgress], None]):
        """设置进度回调函数"""
        self._progress_callback = callback
    
    def _calculate_path_hash(self, path: str) -> str:
        """计算路径哈希"""
        return hashlib.md5(path.encode('utf-8')).hexdigest()
    
    def _should_exclude_directory(self, dir_name: str, exclude_dirs: Set[str]) -> bool:
        """检查是否应该排除目录"""
        return dir_name in exclude_dirs or dir_name.startswith('.')
    
    def _should_exclude_file(self, file_path: Path, config: IndexConfig) -> bool:
        """检查是否应该排除文件"""
        # 检查隐藏文件
        if not config.index_hidden_files and file_path.name.startswith('.'):
            return True
        
        # 检查扩展名
        if file_path.suffix.lower() in config.exclude_extensions:
            return True
        
        # 检查文件大小
        try:
            if file_path.is_file():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                if size_mb > config.max_file_size_mb:
                    return True
        except (OSError, PermissionError):
            return True
        
        return False
    
    def _scan_directory_worker(self, root_path: str, config: IndexConfig) -> Iterator[FileRecord]:
        """单个目录扫描工作器"""
        exclude_dirs = set(config.exclude_dirs)
        
        try:
            root_path_obj = Path(root_path)
            if not root_path_obj.exists() or not root_path_obj.is_dir():
                return
            
            for current_path, dirs, files in os.walk(root_path):
                if self._stop_event.is_set():
                    break
                
                current_path_obj = Path(current_path)
                
                # 过滤目录
                dirs[:] = [d for d in dirs if not self._should_exclude_directory(d, exclude_dirs)]
                
                # 处理当前目录
                try:
                    stat_info = current_path_obj.stat()
                    parent_path = str(current_path_obj.parent)
                    
                    yield FileRecord(
                        id=None,
                        path=str(current_path_obj),
                        name=current_path_obj.name,
                        size=0,  # 目录大小设为0
                        mtime=stat_info.st_mtime,
                        is_dir=True,
                        extension="",
                        parent_path=parent_path,
                        path_hash=self._calculate_path_hash(str(current_path_obj))
                    )
                except (OSError, PermissionError):
                    continue
                
                # 处理文件
                for file_name in files:
                    if self._stop_event.is_set():
                        break
                    
                    file_path = current_path_obj / file_name
                    
                    if self._should_exclude_file(file_path, config):
                        continue
                    
                    try:
                        stat_info = file_path.stat()
                        
                        yield FileRecord(
                            id=None,
                            path=str(file_path),
                            name=file_name,
                            size=stat_info.st_size,
                            mtime=stat_info.st_mtime,
                            is_dir=False,
                            extension=file_path.suffix.lower(),
                            parent_path=str(current_path_obj),
                            path_hash=self._calculate_path_hash(str(file_path))
                        )
                        
                    except (OSError, PermissionError):
                        continue
                        
        except (OSError, PermissionError) as e:
            if self._progress_callback:
                progress = IndexProgress()
                progress.errors.append(f"无法访问目录 {root_path}: {e}")
                self._progress_callback(progress)
    
    def _collect_files_batch(self, file_iterator: Iterator[FileRecord], 
                           batch_size: int) -> Iterator[List[FileRecord]]:
        """批量收集文件记录"""
        batch = []
        for file_record in file_iterator:
            batch.append(file_record)
            if len(batch) >= batch_size:
                yield batch
                batch = []
        
        if batch:
            yield batch
    
    def build_full_index(self) -> IndexProgress:
        """构建完整索引"""
        config = self.config_manager.get_index_config()
        perf_config = self.config_manager.get_performance_config()
        
        progress = IndexProgress(start_time=time.time())
        
        print("🔄 开始构建完整索引...")
        
        # 清空现有索引
        self.db_manager.clear_all_files()
        
        # 并发扫描所有目录
        with ThreadPoolExecutor(max_workers=perf_config.max_workers) as executor:
            # 提交扫描任务
            future_to_path = {
                executor.submit(self._scan_directory_worker, directory, config): directory
                for directory in config.directories
                if Path(directory).exists()
            }
            
            total_processed = 0
            
            for future in as_completed(future_to_path):
                directory = future_to_path[future]
                
                try:
                    file_iterator = future.result()
                    
                    # 批量处理文件记录，使用较小的批次以提高进度回调频率
                    progress_batch_size = min(perf_config.batch_size, 100)  # 限制最大100个文件一批
                    for batch in self._collect_files_batch(file_iterator, progress_batch_size):
                        if self._stop_event.is_set():
                            break

                        self.db_manager.insert_files_batch(batch)
                        total_processed += len(batch)

                        progress.processed_files = total_processed
                        progress.current_path = directory

                        if self._progress_callback:
                            self._progress_callback(progress)
                
                except Exception as e:
                    error_msg = f"扫描目录 {directory} 失败: {e}"
                    progress.errors.append(error_msg)
                    print(f"⚠️  {error_msg}")
        
        # 更新索引元数据
        self.db_manager.set_metadata("last_full_index", time.time())
        self.db_manager.set_metadata("index_version", "1.0")
        
        progress.total_files = progress.processed_files
        elapsed_time = time.time() - progress.start_time

        print(f"\n✅ 索引构建完成！")
        print(f"📊 处理文件: {progress.processed_files:,}")
        print(f"⏱️  耗时: {elapsed_time:.2f} 秒")
        print(f"🚀 速度: {progress.processed_files/elapsed_time:.0f} 文件/秒")
        
        return progress
    
    def rebuild_index(self) -> IndexProgress:
        """重建索引（删除所有索引后重新构建）"""
        print("🔄 开始重建索引...")
        print("⚠️  这将删除所有现有索引数据")
        
        # 清空所有数据
        self.db_manager.clear_all_files()
        
        # 重新构建
        return self.build_full_index()
    
    def update_incremental_index(self, paths: Optional[List[str]] = None, check_deletions: bool = True) -> IndexProgress:
        """增量更新索引"""
        config = self.config_manager.get_index_config()
        perf_config = self.config_manager.get_performance_config()
        
        progress = IndexProgress(start_time=time.time())
        
        # 如果没有指定路径，使用配置中的所有目录
        if paths is None:
            paths = config.directories

        print(f"🔄 开始增量索引更新...")

        for directory in paths:
            if not Path(directory).exists():
                print(f"⚠️  目录不存在，跳过: {directory}")
                continue

            print(f"📁 扫描目录: {directory}")
            
            # 扫描目录获取当前文件
            current_files = {}
            for file_record in self._scan_directory_worker(directory, config):
                if self._stop_event.is_set():
                    break
                current_files[file_record.path] = file_record
            
            # 批量更新
            updates = []
            deleted_paths = []

            # 检查新文件和修改的文件
            for path, file_record in current_files.items():
                existing = self.db_manager.get_file_by_path(path)

                if existing is None:
                    # 新文件
                    updates.append(file_record)
                elif existing.mtime != file_record.mtime or existing.size != file_record.size:
                    # 文件已修改
                    updates.append(file_record)

            # 可选的删除检测（性能优化）
            if check_deletions:
                # 获取数据库中该目录下的现有文件
                existing_files = self.db_manager.get_files_in_directory(directory)

                # 检查已删除的文件
                for path in existing_files:
                    if path not in current_files:
                        deleted_paths.append(path)

            # 执行更新
            if updates:
                # 批量插入/更新，使用较小的批次以提高进度回调频率
                progress_batch_size = min(perf_config.batch_size, 100)  # 限制最大100个文件一批
                for i in range(0, len(updates), progress_batch_size):
                    batch = updates[i:i + progress_batch_size]
                    self.db_manager.insert_files_batch(batch)

                    progress.processed_files += len(batch)
                    progress.current_path = directory

                    if self._progress_callback:
                        self._progress_callback(progress)

            # 执行删除
            if deleted_paths:
                print(f"🗑️  删除 {len(deleted_paths)} 个不存在的文件")
                self.db_manager.delete_files_by_paths(deleted_paths)
        
        # 更新元数据
        self.db_manager.set_metadata("last_incremental_index", time.time())
        
        elapsed_time = time.time() - progress.start_time
        print(f"\n✅ 增量索引更新完成！")
        print(f"📊 更新文件: {progress.processed_files:,}")
        print(f"⏱️  耗时: {elapsed_time:.2f} 秒")
        
        return progress

    def cleanup_deleted_files(self) -> int:
        """清理已删除的文件（性能优化的独立操作）"""
        print("🧹 开始清理已删除的文件...")

        config = self.config_manager.get_index_config()
        total_deleted = 0

        for directory in config.directories:
            if not Path(directory).exists():
                # 如果整个目录都不存在了，删除该目录下的所有文件
                existing_files = self.db_manager.get_files_in_directory(directory)
                if existing_files:
                    deleted_count = self.db_manager.delete_files_by_paths(list(existing_files.keys()))
                    total_deleted += deleted_count
                    print(f"🗑️  目录 {directory} 不存在，删除 {deleted_count} 个文件")
                continue

            print(f"🔍 检查目录: {directory}")

            # 获取数据库中的文件
            existing_files = self.db_manager.get_files_in_directory(directory)
            deleted_paths = []

            # 检查文件是否还存在
            for path in existing_files:
                if not Path(path).exists():
                    deleted_paths.append(path)

            if deleted_paths:
                deleted_count = self.db_manager.delete_files_by_paths(deleted_paths)
                total_deleted += deleted_count
                print(f"🗑️  删除 {deleted_count} 个不存在的文件")

        print(f"✅ 清理完成，总共删除 {total_deleted} 个文件")
        return total_deleted

    def get_index_status(self) -> dict:
        """获取索引状态"""
        stats = self.db_manager.get_statistics()
        
        last_full = self.db_manager.get_metadata("last_full_index")
        last_incremental = self.db_manager.get_metadata("last_incremental_index")
        
        return {
            "total_files": stats["total_files"],
            "total_directories": stats["total_directories"],
            "total_regular_files": stats["total_regular_files"],
            "last_full_index": last_full,
            "last_incremental_index": last_incremental,
            "index_version": self.db_manager.get_metadata("index_version", "unknown")
        }
    
    def stop(self):
        """停止索引操作"""
        self._stop_event.set()
        print("🛑 正在停止索引操作...")
    
    def reset_stop(self):
        """重置停止标志"""
        self._stop_event.clear()
