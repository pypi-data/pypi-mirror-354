#!/usr/bin/env python3
"""
高性能数据库管理器
优化特性：
- 连接池和事务批处理
- 索引优化和查询缓存
- 内存映射和WAL模式
- 批量插入和更新
"""

import sqlite3
import threading
import time
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Iterator
from dataclasses import dataclass
from contextlib import contextmanager
import hashlib
import json

from . import get_default_db_path


@dataclass
class FileRecord:
    """文件记录数据类"""
    id: Optional[int]
    path: str
    name: str
    size: int
    mtime: float
    is_dir: bool
    extension: str
    parent_path: str
    path_hash: str


class DatabaseManager:
    """高性能数据库管理器"""

    def __init__(self, db_path: Optional[str] = None):
        # 如果没有指定路径，使用默认的用户数据目录路径
        if db_path is None:
            self.db_path = get_default_db_path()
        else:
            self.db_path = Path(db_path).resolve()

        self._local = threading.local()
        self._lock = threading.RLock()
        self._connection_count = 0
        self._max_connections = 10

        # 初始化数据库
        self._init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取线程本地连接"""
        if not hasattr(self._local, 'connection') or self._local.connection is None:
            with self._lock:
                if self._connection_count >= self._max_connections:
                    raise RuntimeError("数据库连接池已满")
                
                conn = sqlite3.connect(
                    str(self.db_path),
                    timeout=30.0,
                    check_same_thread=False
                )
                
                # 性能优化设置
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=10000")
                conn.execute("PRAGMA temp_store=MEMORY")
                conn.execute("PRAGMA mmap_size=268435456")  # 256MB
                
                conn.row_factory = sqlite3.Row
                self._local.connection = conn
                self._connection_count += 1
        
        return self._local.connection
    
    def _init_database(self):
        """初始化数据库结构"""
        with self._get_connection() as conn:
            # 创建文件表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    name TEXT NOT NULL,
                    size INTEGER NOT NULL,
                    mtime REAL NOT NULL,
                    is_dir BOOLEAN NOT NULL,
                    extension TEXT NOT NULL,
                    parent_path TEXT NOT NULL,
                    path_hash TEXT NOT NULL UNIQUE,
                    created_at REAL DEFAULT (julianday('now')),
                    updated_at REAL DEFAULT (julianday('now'))
                )
            """)
            
            # 创建索引表
            conn.execute("""
                CREATE TABLE IF NOT EXISTS index_metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at REAL DEFAULT (julianday('now'))
                )
            """)

            # 创建目录元数据表（用于智能增量索引）
            conn.execute("""
                CREATE TABLE IF NOT EXISTS directory_metadata (
                    path TEXT PRIMARY KEY,
                    last_scan_time REAL NOT NULL,
                    last_mtime REAL NOT NULL,
                    file_count INTEGER DEFAULT 0,
                    created_at REAL DEFAULT (julianday('now')),
                    updated_at REAL DEFAULT (julianday('now'))
                )
            """)
            
            # 创建高性能索引
            indexes = [
                "CREATE INDEX IF NOT EXISTS idx_files_name ON files(name)",
                "CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension)",
                "CREATE INDEX IF NOT EXISTS idx_files_parent_path ON files(parent_path)",
                "CREATE INDEX IF NOT EXISTS idx_files_is_dir ON files(is_dir)",
                "CREATE INDEX IF NOT EXISTS idx_files_size ON files(size)",
                "CREATE INDEX IF NOT EXISTS idx_files_mtime ON files(mtime)",
                "CREATE INDEX IF NOT EXISTS idx_files_name_lower ON files(lower(name))",
                "CREATE INDEX IF NOT EXISTS idx_files_path_hash ON files(path_hash)"
            ]
            
            for index_sql in indexes:
                conn.execute(index_sql)
            
            conn.commit()
    
    @contextmanager
    def transaction(self):
        """事务上下文管理器"""
        conn = self._get_connection()
        try:
            conn.execute("BEGIN IMMEDIATE")
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
    
    def _calculate_path_hash(self, path: str) -> str:
        """计算路径哈希"""
        return hashlib.md5(path.encode('utf-8')).hexdigest()
    
    def insert_files_batch(self, files: List[FileRecord], batch_size: int = 1000):
        """批量插入文件记录"""
        if not files:
            return
        
        with self.transaction() as conn:
            # 准备批量插入数据
            insert_sql = """
                INSERT OR REPLACE INTO files 
                (path, name, size, mtime, is_dir, extension, parent_path, path_hash, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, julianday('now'))
            """
            
            # 分批处理
            for i in range(0, len(files), batch_size):
                batch = files[i:i + batch_size]
                batch_data = [
                    (
                        file_record.path,
                        file_record.name,
                        file_record.size,
                        file_record.mtime,
                        file_record.is_dir,
                        file_record.extension,
                        file_record.parent_path,
                        file_record.path_hash
                    )
                    for file_record in batch
                ]
                
                conn.executemany(insert_sql, batch_data)
    
    def update_file(self, file_record: FileRecord):
        """更新单个文件记录"""
        with self.transaction() as conn:
            conn.execute("""
                UPDATE files SET 
                    name = ?, size = ?, mtime = ?, is_dir = ?, 
                    extension = ?, parent_path = ?, updated_at = julianday('now')
                WHERE path_hash = ?
            """, (
                file_record.name, file_record.size, file_record.mtime,
                file_record.is_dir, file_record.extension, file_record.parent_path,
                file_record.path_hash
            ))
    
    def delete_files_by_paths(self, paths: List[str]):
        """批量删除文件记录"""
        if not paths:
            return
        
        path_hashes = [self._calculate_path_hash(path) for path in paths]
        
        with self.transaction() as conn:
            placeholders = ','.join(['?'] * len(path_hashes))
            conn.execute(f"DELETE FROM files WHERE path_hash IN ({placeholders})", path_hashes)
    
    def delete_files_by_parent(self, parent_path: str):
        """删除指定父目录下的所有文件"""
        with self.transaction() as conn:
            conn.execute("DELETE FROM files WHERE parent_path LIKE ?", (f"{parent_path}%",))
    
    def file_exists(self, path: str) -> bool:
        """检查文件是否存在于索引中"""
        path_hash = self._calculate_path_hash(path)
        conn = self._get_connection()
        cursor = conn.execute("SELECT 1 FROM files WHERE path_hash = ? LIMIT 1", (path_hash,))
        return cursor.fetchone() is not None
    
    def get_file_by_path(self, path: str) -> Optional[FileRecord]:
        """根据路径获取文件记录"""
        path_hash = self._calculate_path_hash(path)
        conn = self._get_connection()
        cursor = conn.execute("""
            SELECT id, path, name, size, mtime, is_dir, extension, parent_path, path_hash
            FROM files WHERE path_hash = ?
        """, (path_hash,))

        row = cursor.fetchone()
        if row:
            return FileRecord(
                id=row['id'], path=row['path'], name=row['name'],
                size=row['size'], mtime=row['mtime'], is_dir=bool(row['is_dir']),
                extension=row['extension'], parent_path=row['parent_path'],
                path_hash=row['path_hash']
            )
        return None

    def get_files_in_directory(self, directory: str) -> Dict[str, FileRecord]:
        """获取指定目录及其子目录下的所有文件"""
        conn = self._get_connection()

        # 使用LIKE查询获取目录下的所有文件
        cursor = conn.execute("""
            SELECT id, path, name, size, mtime, is_dir, extension, parent_path, path_hash
            FROM files
            WHERE path LIKE ? OR path = ?
            ORDER BY path
        """, (f"{directory}%", directory))

        files = {}
        for row in cursor:
            file_record = FileRecord(
                id=row['id'], path=row['path'], name=row['name'],
                size=row['size'], mtime=row['mtime'], is_dir=bool(row['is_dir']),
                extension=row['extension'], parent_path=row['parent_path'],
                path_hash=row['path_hash']
            )
            files[file_record.path] = file_record

        return files

    def delete_files_by_paths(self, paths: List[str]) -> int:
        """根据路径列表删除文件"""
        if not paths:
            return 0

        conn = self._get_connection()
        deleted_count = 0

        try:
            # 批量删除
            path_hashes = [self._calculate_path_hash(path) for path in paths]
            placeholders = ','.join(['?' for _ in path_hashes])

            cursor = conn.execute(f"""
                DELETE FROM files WHERE path_hash IN ({placeholders})
            """, path_hashes)

            deleted_count = cursor.rowcount
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e

        return deleted_count
    
    def search_files(self, query: str, case_sensitive: bool = False, 
                    max_results: int = 1000, file_types: Optional[List[str]] = None) -> List[FileRecord]:
        """高性能文件搜索"""
        conn = self._get_connection()
        
        # 构建搜索条件
        conditions = []
        params = []
        
        if query:
            if case_sensitive:
                conditions.append("name LIKE ?")
                params.append(f"%{query}%")
            else:
                conditions.append("lower(name) LIKE lower(?)")
                params.append(f"%{query}%")
        
        if file_types:
            type_conditions = []
            for file_type in file_types:
                if file_type == 'dir':
                    type_conditions.append("is_dir = 1")
                elif file_type == 'file':
                    type_conditions.append("is_dir = 0")
                else:
                    type_conditions.append("extension = ?")
                    params.append(file_type)
            
            if type_conditions:
                conditions.append(f"({' OR '.join(type_conditions)})")
        
        # 构建SQL查询
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        sql = f"""
            SELECT id, path, name, size, mtime, is_dir, extension, parent_path, path_hash
            FROM files 
            WHERE {where_clause}
            ORDER BY 
                CASE WHEN lower(name) = lower(?) THEN 0 ELSE 1 END,
                length(name),
                name
            LIMIT ?
        """
        
        params.extend([query or '', max_results])
        cursor = conn.execute(sql, params)
        
        results = []
        for row in cursor:
            results.append(FileRecord(
                id=row['id'], path=row['path'], name=row['name'],
                size=row['size'], mtime=row['mtime'], is_dir=bool(row['is_dir']),
                extension=row['extension'], parent_path=row['parent_path'],
                path_hash=row['path_hash']
            ))
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取数据库统计信息"""
        conn = self._get_connection()
        
        stats = {}
        
        # 总文件数
        cursor = conn.execute("SELECT COUNT(*) as total FROM files")
        stats['total_files'] = cursor.fetchone()['total']
        
        # 目录数
        cursor = conn.execute("SELECT COUNT(*) as dirs FROM files WHERE is_dir = 1")
        stats['total_directories'] = cursor.fetchone()['dirs']
        
        # 文件数
        stats['total_regular_files'] = stats['total_files'] - stats['total_directories']

        # 最后更新时间
        cursor = conn.execute("SELECT MAX(updated_at) as last_update FROM files")
        result = cursor.fetchone()
        stats['last_update'] = result['last_update']
        
        return stats
    
    def clear_all_files(self):
        """清空所有文件记录（重建索引用）"""
        with self.transaction() as conn:
            conn.execute("DELETE FROM files")

        # VACUUM需要在事务外执行
        conn = self._get_connection()
        conn.execute("VACUUM")
    
    def set_metadata(self, key: str, value: Any):
        """设置元数据"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO index_metadata (key, value, updated_at)
                VALUES (?, ?, julianday('now'))
            """, (key, json.dumps(value)))
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """获取元数据"""
        conn = self._get_connection()
        cursor = conn.execute("SELECT value FROM index_metadata WHERE key = ?", (key,))
        row = cursor.fetchone()
        if row:
            return json.loads(row['value'])
        return default

    def set_directory_metadata(self, path: str, last_scan_time: float, last_mtime: float, file_count: int = 0):
        """设置目录元数据"""
        with self.transaction() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO directory_metadata
                (path, last_scan_time, last_mtime, file_count, updated_at)
                VALUES (?, ?, ?, ?, julianday('now'))
            """, (path, last_scan_time, last_mtime, file_count))

    def get_directory_metadata(self, path: str) -> Optional[Dict[str, Any]]:
        """获取目录元数据"""
        conn = self._get_connection()
        cursor = conn.execute("""
            SELECT path, last_scan_time, last_mtime, file_count, created_at, updated_at
            FROM directory_metadata WHERE path = ?
        """, (path,))
        row = cursor.fetchone()
        if row:
            return {
                'path': row['path'],
                'last_scan_time': row['last_scan_time'],
                'last_mtime': row['last_mtime'],
                'file_count': row['file_count'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
        return None

    def get_all_directory_metadata(self) -> Dict[str, Dict[str, Any]]:
        """获取所有目录元数据"""
        conn = self._get_connection()
        cursor = conn.execute("""
            SELECT path, last_scan_time, last_mtime, file_count, created_at, updated_at
            FROM directory_metadata
            ORDER BY path
        """)

        result = {}
        for row in cursor:
            result[row['path']] = {
                'path': row['path'],
                'last_scan_time': row['last_scan_time'],
                'last_mtime': row['last_mtime'],
                'file_count': row['file_count'],
                'created_at': row['created_at'],
                'updated_at': row['updated_at']
            }
        return result

    def delete_directory_metadata(self, path: str):
        """删除目录元数据"""
        with self.transaction() as conn:
            conn.execute("DELETE FROM directory_metadata WHERE path = ?", (path,))
    
    def close(self):
        """关闭数据库连接"""
        if hasattr(self._local, 'connection') and self._local.connection:
            self._local.connection.close()
            self._local.connection = None
            with self._lock:
                self._connection_count -= 1
