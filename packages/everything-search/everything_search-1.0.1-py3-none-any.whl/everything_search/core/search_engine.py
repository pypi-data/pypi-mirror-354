#!/usr/bin/env python3
"""
高性能搜索引擎
优化特性：
- 多级缓存系统
- 智能查询优化
- 模糊搜索和正则表达式
- 结果排序和分页
"""

import re
import time
import threading
import os
from typing import List, Dict, Optional, Tuple, Set, Any
from dataclasses import dataclass
from collections import OrderedDict
import difflib

from .config_manager import ConfigManager, SearchConfig
from .database import DatabaseManager, FileRecord


@dataclass
class SearchResult:
    """搜索结果"""
    file_record: FileRecord
    relevance_score: float
    match_type: str  # exact, prefix, contains, fuzzy
    highlighted_name: str


class LRUCache:
    """高性能LRU缓存"""
    
    def __init__(self, max_size: int = 1000):
        self.max_size = max_size
        self.cache: OrderedDict = OrderedDict()
        self.lock = threading.RLock()
    
    def get(self, key: str) -> Optional[Any]:
        with self.lock:
            if key in self.cache:
                # 移到末尾（最近使用）
                self.cache.move_to_end(key)
                return self.cache[key]
            return None
    
    def put(self, key: str, value: Any):
        with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                if len(self.cache) >= self.max_size:
                    # 删除最久未使用的项
                    self.cache.popitem(last=False)
            self.cache[key] = value
    
    def clear(self):
        with self.lock:
            self.cache.clear()


class SearchEngine:
    """高性能搜索引擎"""
    
    def __init__(self, config_manager: ConfigManager, db_manager: DatabaseManager):
        self.config_manager = config_manager
        self.db_manager = db_manager
        
        # 多级缓存
        self._result_cache = LRUCache(max_size=1000)
        self._query_cache = LRUCache(max_size=500)
        
        # 预编译的正则表达式缓存
        self._regex_cache: Dict[str, re.Pattern] = {}
        self._regex_cache_lock = threading.RLock()
    
    def _get_compiled_regex(self, pattern: str, flags: int = 0) -> Optional[re.Pattern]:
        """获取编译后的正则表达式（带缓存）"""
        cache_key = f"{pattern}:{flags}"
        
        with self._regex_cache_lock:
            if cache_key in self._regex_cache:
                return self._regex_cache[cache_key]
            
            try:
                compiled = re.compile(pattern, flags)
                # 限制缓存大小
                if len(self._regex_cache) > 100:
                    # 清除一半缓存
                    keys_to_remove = list(self._regex_cache.keys())[:50]
                    for key in keys_to_remove:
                        del self._regex_cache[key]
                
                self._regex_cache[cache_key] = compiled
                return compiled
            except re.error:
                return None
    
    def _calculate_relevance_score(self, query: str, file_record: FileRecord, 
                                 match_type: str) -> float:
        """计算相关性分数"""
        score = 0.0
        name = file_record.name.lower()
        query_lower = query.lower()
        
        # 基础分数
        if match_type == "exact":
            score = 100.0
        elif match_type == "prefix":
            score = 90.0
        elif match_type == "contains":
            score = 70.0
        elif match_type == "fuzzy":
            score = 50.0
        else:
            score = 30.0
        
        # 长度奖励（短文件名优先）
        length_bonus = max(0, 50 - len(name))
        score += length_bonus * 0.1
        
        # 目录vs文件奖励
        if not file_record.is_dir:
            score += 5.0
        
        # 扩展名匹配奖励
        if query_lower in file_record.extension.lower():
            score += 10.0
        
        # 路径深度惩罚
        path_depth = file_record.path.count(os.sep)
        score -= path_depth * 0.5
        
        return max(0.0, score)
    
    def _highlight_match(self, text: str, query: str, case_sensitive: bool = False) -> str:
        """高亮匹配文本"""
        if not query:
            return text
        
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = re.escape(query)
        regex = self._get_compiled_regex(pattern, flags)
        
        if regex:
            return regex.sub(f"**{query}**", text)
        return text
    
    def _fuzzy_match(self, query: str, text: str, threshold: float = 0.6) -> bool:
        """模糊匹配"""
        if not query or not text:
            return False
        
        # 使用序列匹配器计算相似度
        similarity = difflib.SequenceMatcher(None, query.lower(), text.lower()).ratio()
        return similarity >= threshold
    
    def _search_database(self, query: str, config: SearchConfig, 
                        file_types: Optional[List[str]] = None) -> List[FileRecord]:
        """在数据库中搜索"""
        # 检查查询缓存
        cache_key = f"{query}:{config.case_sensitive}:{config.max_results}:{file_types}"
        cached_result = self._query_cache.get(cache_key)
        if cached_result:
            return cached_result
        
        # 执行数据库搜索
        results = self.db_manager.search_files(
            query=query,
            case_sensitive=config.case_sensitive,
            max_results=config.max_results * 2,  # 获取更多结果用于后续过滤
            file_types=file_types
        )
        
        # 缓存结果
        self._query_cache.put(cache_key, results)
        return results
    
    def search(self, query: str, file_types: Optional[List[str]] = None,
              max_results: Optional[int] = None, use_regex: bool = False,
              fuzzy_threshold: float = 0.6) -> List[SearchResult]:
        """执行搜索"""
        if not query.strip():
            return []
        
        config = self.config_manager.get_search_config()
        max_results = max_results or config.max_results
        
        # 检查结果缓存
        cache_key = f"search:{query}:{file_types}:{max_results}:{use_regex}:{fuzzy_threshold}"
        cached_results = self._result_cache.get(cache_key)
        if cached_results:
            return cached_results
        
        start_time = time.time()

        # 正则表达式搜索需要特殊处理
        if use_regex:
            regex_pattern = self._get_compiled_regex(
                query,
                0 if config.case_sensitive else re.IGNORECASE
            )
            if not regex_pattern:
                return []

            # 正则表达式搜索：获取所有文件进行匹配
            db_results = self.db_manager.search_files(
                query="",  # 空查询获取所有文件
                case_sensitive=config.case_sensitive,
                max_results=config.max_results * 10,  # 获取更多文件用于正则匹配
                file_types=file_types
            )
        else:
            # 普通搜索：使用数据库查询
            db_results = self._search_database(query, config, file_types)

        search_results = []
        query_lower = query.lower()
        
        for file_record in db_results:
            name = file_record.name
            name_lower = name.lower()
            
            match_type = ""
            is_match = False
            
            if use_regex and regex_pattern:
                # 正则表达式匹配
                if regex_pattern.search(name):
                    match_type = "regex"
                    is_match = True
            else:
                # 标准匹配
                if config.case_sensitive:
                    search_name = name
                    search_query = query
                else:
                    search_name = name_lower
                    search_query = query_lower
                
                # 精确匹配
                if search_name == search_query:
                    match_type = "exact"
                    is_match = True
                # 前缀匹配
                elif search_name.startswith(search_query):
                    match_type = "prefix"
                    is_match = True
                # 包含匹配
                elif search_query in search_name:
                    match_type = "contains"
                    is_match = True
                # 模糊匹配
                elif config.fuzzy_search and self._fuzzy_match(query, name, fuzzy_threshold):
                    match_type = "fuzzy"
                    is_match = True
            
            if is_match:
                relevance_score = self._calculate_relevance_score(query, file_record, match_type)
                highlighted_name = self._highlight_match(name, query, config.case_sensitive)
                
                search_results.append(SearchResult(
                    file_record=file_record,
                    relevance_score=relevance_score,
                    match_type=match_type,
                    highlighted_name=highlighted_name
                ))
        
        # 按相关性排序
        search_results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # 限制结果数量
        search_results = search_results[:max_results]
        
        # 缓存结果
        self._result_cache.put(cache_key, search_results)
        
        search_time = time.time() - start_time
        print(f"🔍 搜索完成: {len(search_results)} 个结果，耗时 {search_time:.3f} 秒")
        
        return search_results
    
    def search_by_extension(self, extension: str, max_results: Optional[int] = None) -> List[SearchResult]:
        """按扩展名搜索"""
        config = self.config_manager.get_search_config()
        max_results = max_results or config.max_results
        
        # 规范化扩展名
        if not extension.startswith('.'):
            extension = '.' + extension
        extension = extension.lower()
        
        # 直接查询数据库
        db_results = self.db_manager.search_files(
            query="",
            case_sensitive=False,
            max_results=max_results,
            file_types=[extension]
        )
        
        search_results = []
        for file_record in db_results:
            search_results.append(SearchResult(
                file_record=file_record,
                relevance_score=100.0,
                match_type="extension",
                highlighted_name=file_record.name
            ))
        
        return search_results
    
    def search_by_size(self, min_size: int = 0, max_size: Optional[int] = None,
                      max_results: Optional[int] = None) -> List[SearchResult]:
        """按文件大小搜索"""
        config = self.config_manager.get_search_config()
        max_results = max_results or config.max_results
        
        # 构建SQL查询
        conditions = ["is_dir = 0"]  # 只搜索文件
        params = []
        
        if min_size > 0:
            conditions.append("size >= ?")
            params.append(min_size)
        
        if max_size is not None:
            conditions.append("size <= ?")
            params.append(max_size)
        
        where_clause = " AND ".join(conditions)
        sql = f"""
            SELECT id, path, name, size, mtime, is_dir, extension, parent_path, path_hash
            FROM files 
            WHERE {where_clause}
            ORDER BY size DESC
            LIMIT ?
        """
        params.append(max_results)
        
        conn = self.db_manager._get_connection()
        cursor = conn.execute(sql, params)
        
        search_results = []
        for row in cursor:
            file_record = FileRecord(
                id=row['id'], path=row['path'], name=row['name'],
                size=row['size'], mtime=row['mtime'], is_dir=bool(row['is_dir']),
                extension=row['extension'], parent_path=row['parent_path'],
                path_hash=row['path_hash']
            )
            
            search_results.append(SearchResult(
                file_record=file_record,
                relevance_score=100.0,
                match_type="size",
                highlighted_name=file_record.name
            ))
        
        return search_results
    
    def get_recent_files(self, days: int = 7, max_results: Optional[int] = None) -> List[SearchResult]:
        """获取最近修改的文件"""
        config = self.config_manager.get_search_config()
        max_results = max_results or config.max_results
        
        cutoff_time = time.time() - (days * 24 * 3600)
        
        sql = """
            SELECT id, path, name, size, mtime, is_dir, extension, parent_path, path_hash
            FROM files 
            WHERE mtime >= ? AND is_dir = 0
            ORDER BY mtime DESC
            LIMIT ?
        """
        
        conn = self.db_manager._get_connection()
        cursor = conn.execute(sql, (cutoff_time, max_results))
        
        search_results = []
        for row in cursor:
            file_record = FileRecord(
                id=row['id'], path=row['path'], name=row['name'],
                size=row['size'], mtime=row['mtime'], is_dir=bool(row['is_dir']),
                extension=row['extension'], parent_path=row['parent_path'],
                path_hash=row['path_hash']
            )
            
            search_results.append(SearchResult(
                file_record=file_record,
                relevance_score=100.0,
                match_type="recent",
                highlighted_name=file_record.name
            ))
        
        return search_results
    
    def clear_cache(self):
        """清空所有缓存"""
        self._result_cache.clear()
        self._query_cache.clear()
        with self._regex_cache_lock:
            self._regex_cache.clear()
        print("🧹 搜索缓存已清空")
