#!/usr/bin/env python3
"""
高性能文件系统监控器
优化特性：
- 使用macOS FSEvents API
- 事件批处理和去重
- 智能过滤和延迟处理
- 内存优化的事件队列
"""

import os
import time
import threading
from pathlib import Path
from typing import List, Dict, Set, Optional, Callable
from dataclasses import dataclass
from queue import Queue, Empty
import hashlib

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    # 创建占位符类
    class FileSystemEventHandler:
        pass
    class FileSystemEvent:
        pass
    class Observer:
        pass
    print("⚠️  watchdog 未安装，实时监控功能不可用")

from .config_manager import ConfigManager, IndexConfig
from .database import DatabaseManager, FileRecord
from .file_indexer import FileIndexer


@dataclass
class FileChangeEvent:
    """文件变更事件"""
    event_type: str  # created, modified, deleted, moved
    path: str
    old_path: Optional[str] = None
    timestamp: float = 0
    
    def __post_init__(self):
        if self.timestamp == 0:
            self.timestamp = time.time()


class BatchProcessor:
    """事件批处理器"""
    
    def __init__(self, batch_size: int = 100, flush_interval: float = 2.0):
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.events: List[FileChangeEvent] = []
        self.last_flush = time.time()
        self.lock = threading.Lock()
        self.processor_callback: Optional[Callable[[List[FileChangeEvent]], None]] = None
    
    def set_processor(self, callback: Callable[[List[FileChangeEvent]], None]):
        """设置批处理回调"""
        self.processor_callback = callback
    
    def add_event(self, event: FileChangeEvent):
        """添加事件到批处理队列"""
        with self.lock:
            self.events.append(event)
            
            # 检查是否需要刷新
            should_flush = (
                len(self.events) >= self.batch_size or
                time.time() - self.last_flush >= self.flush_interval
            )
            
            if should_flush:
                self._flush_events()
    
    def _flush_events(self):
        """刷新事件批次"""
        if not self.events or not self.processor_callback:
            return
        
        # 去重和合并事件
        deduplicated = self._deduplicate_events(self.events)
        
        if deduplicated:
            self.processor_callback(deduplicated)
        
        self.events.clear()
        self.last_flush = time.time()
    
    def _deduplicate_events(self, events: List[FileChangeEvent]) -> List[FileChangeEvent]:
        """去重和合并事件"""
        # 按路径分组
        path_events: Dict[str, List[FileChangeEvent]] = {}
        for event in events:
            if event.path not in path_events:
                path_events[event.path] = []
            path_events[event.path].append(event)
        
        # 合并每个路径的事件
        merged_events = []
        for path, path_event_list in path_events.items():
            # 按时间排序
            path_event_list.sort(key=lambda e: e.timestamp)
            
            # 取最后一个事件（最新状态）
            last_event = path_event_list[-1]
            merged_events.append(last_event)
        
        return merged_events
    
    def force_flush(self):
        """强制刷新所有待处理事件"""
        with self.lock:
            self._flush_events()


class EverythingFileHandler(FileSystemEventHandler):
    """Everything搜索文件系统事件处理器"""
    
    def __init__(self, config: IndexConfig, batch_processor: BatchProcessor):
        super().__init__()
        self.config = config
        self.batch_processor = batch_processor
        self.exclude_dirs = set(config.exclude_dirs)
        self.exclude_extensions = set(config.exclude_extensions)
    
    def _should_ignore_path(self, path: str) -> bool:
        """检查是否应该忽略路径"""
        path_obj = Path(path)
        
        # 检查隐藏文件
        if not self.config.index_hidden_files and path_obj.name.startswith('.'):
            return True
        
        # 检查排除目录
        for part in path_obj.parts:
            if part in self.exclude_dirs:
                return True
        
        # 检查排除扩展名
        if path_obj.suffix.lower() in self.exclude_extensions:
            return True
        
        return False
    
    def on_created(self, event: FileSystemEvent):
        """文件/目录创建事件"""
        if not self._should_ignore_path(event.src_path):
            self.batch_processor.add_event(FileChangeEvent(
                event_type="created",
                path=event.src_path
            ))
    
    def on_modified(self, event: FileSystemEvent):
        """文件/目录修改事件"""
        if not event.is_directory and not self._should_ignore_path(event.src_path):
            self.batch_processor.add_event(FileChangeEvent(
                event_type="modified",
                path=event.src_path
            ))
    
    def on_deleted(self, event: FileSystemEvent):
        """文件/目录删除事件"""
        if not self._should_ignore_path(event.src_path):
            self.batch_processor.add_event(FileChangeEvent(
                event_type="deleted",
                path=event.src_path
            ))
    
    def on_moved(self, event: FileSystemEvent):
        """文件/目录移动事件"""
        if hasattr(event, 'dest_path'):
            # 检查源路径和目标路径
            ignore_src = self._should_ignore_path(event.src_path)
            ignore_dest = self._should_ignore_path(event.dest_path)
            
            if not ignore_src or not ignore_dest:
                self.batch_processor.add_event(FileChangeEvent(
                    event_type="moved",
                    path=event.dest_path,
                    old_path=event.src_path
                ))


class FileWatcher:
    """高性能文件系统监控器"""
    
    def __init__(self, config_manager: ConfigManager, db_manager: DatabaseManager, 
                 file_indexer: FileIndexer):
        self.config_manager = config_manager
        self.db_manager = db_manager
        self.file_indexer = file_indexer
        
        self.observer: Optional[Observer] = None
        self.batch_processor = BatchProcessor(batch_size=50, flush_interval=1.0)
        self.batch_processor.set_processor(self._process_events_batch)
        
        self._running = False
        self._watch_handles = []
        
        if not WATCHDOG_AVAILABLE:
            raise RuntimeError("watchdog 库未安装，无法使用实时监控功能")
    
    def _calculate_path_hash(self, path: str) -> str:
        """计算路径哈希"""
        return hashlib.md5(path.encode('utf-8')).hexdigest()
    
    def _create_file_record(self, path: str) -> Optional[FileRecord]:
        """从路径创建文件记录"""
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return None
            
            stat_info = path_obj.stat()
            
            return FileRecord(
                id=None,
                path=str(path_obj),
                name=path_obj.name,
                size=stat_info.st_size if path_obj.is_file() else 0,
                mtime=stat_info.st_mtime,
                is_dir=path_obj.is_dir(),
                extension=path_obj.suffix.lower() if path_obj.is_file() else "",
                parent_path=str(path_obj.parent),
                path_hash=self._calculate_path_hash(str(path_obj))
            )
        except (OSError, PermissionError):
            return None
    
    def _process_events_batch(self, events: List[FileChangeEvent]):
        """批量处理文件变更事件"""
        if not events:
            return
        
        print(f"🔄 处理 {len(events)} 个文件变更事件")
        
        created_files = []
        modified_files = []
        deleted_paths = []
        moved_files = []
        
        for event in events:
            if event.event_type == "created":
                file_record = self._create_file_record(event.path)
                if file_record:
                    created_files.append(file_record)
            
            elif event.event_type == "modified":
                file_record = self._create_file_record(event.path)
                if file_record:
                    modified_files.append(file_record)
            
            elif event.event_type == "deleted":
                deleted_paths.append(event.path)
            
            elif event.event_type == "moved" and event.old_path:
                # 处理移动：删除旧路径，添加新路径
                deleted_paths.append(event.old_path)
                file_record = self._create_file_record(event.path)
                if file_record:
                    created_files.append(file_record)
        
        try:
            # 批量更新数据库
            if created_files:
                self.db_manager.insert_files_batch(created_files)
                print(f"✅ 添加 {len(created_files)} 个文件")
            
            if modified_files:
                for file_record in modified_files:
                    self.db_manager.update_file(file_record)
                print(f"🔄 更新 {len(modified_files)} 个文件")
            
            if deleted_paths:
                self.db_manager.delete_files_by_paths(deleted_paths)
                print(f"🗑️  删除 {len(deleted_paths)} 个文件")
        
        except Exception as e:
            print(f"⚠️  批量处理事件失败: {e}")
    
    def start_watching(self) -> bool:
        """开始监控文件系统"""
        if self._running:
            print("⚠️  文件监控已在运行")
            return False
        
        if not WATCHDOG_AVAILABLE:
            print("❌ watchdog 库未安装")
            return False
        
        config = self.config_manager.get_index_config()
        
        try:
            self.observer = Observer()
            
            # 为每个监控目录添加处理器
            for directory in config.directories:
                if Path(directory).exists():
                    handler = EverythingFileHandler(config, self.batch_processor)
                    watch = self.observer.schedule(handler, directory, recursive=True)
                    self._watch_handles.append(watch)
                    print(f"📁 开始监控目录: {directory}")
                else:
                    print(f"⚠️  目录不存在，跳过监控: {directory}")
            
            if not self._watch_handles:
                print("❌ 没有有效的监控目录")
                return False
            
            self.observer.start()
            self._running = True
            
            print("🔍 文件系统实时监控已启动")
            return True
        
        except Exception as e:
            print(f"❌ 启动文件监控失败: {e}")
            return False
    
    def stop_watching(self):
        """停止监控文件系统"""
        if not self._running:
            return
        
        print("🛑 正在停止文件系统监控...")
        
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=5.0)
            self.observer = None
        
        # 强制处理剩余事件
        self.batch_processor.force_flush()
        
        self._watch_handles.clear()
        self._running = False
        
        print("✅ 文件系统监控已停止")
    
    def is_running(self) -> bool:
        """检查监控是否正在运行"""
        return self._running
    
    def get_status(self) -> Dict[str, any]:
        """获取监控状态"""
        config = self.config_manager.get_index_config()
        
        return {
            "running": self._running,
            "watched_directories": len(self._watch_handles),
            "total_directories": len(config.directories),
            "watchdog_available": WATCHDOG_AVAILABLE
        }
