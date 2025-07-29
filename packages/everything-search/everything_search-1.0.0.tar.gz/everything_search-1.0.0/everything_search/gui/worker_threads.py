#!/usr/bin/env python3
"""
GUI工作线程
处理耗时操作避免界面冻结
"""

import os
import sys
import time
import subprocess
import threading
import queue
from pathlib import Path
from typing import List, Optional
from PySide6.QtCore import QThread, Signal, QObject

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.config_manager import ConfigManager
from core.database import DatabaseManager
from core.search_engine import SearchEngine, SearchResult
from core.file_indexer import FileIndexer, IndexProgress
from core import get_default_db_path


class IndexWorker(QThread):
    """索引工作线程"""

    # 信号定义
    progress_updated = Signal(str, int, int)  # 消息, 已处理文件数, 总文件数
    status_updated = Signal(str)  # 状态消息
    finished = Signal(bool, str)  # 是否成功, 消息
    error_occurred = Signal(str)  # 错误消息

    def __init__(self, action: str = "start"):
        super().__init__()
        self.action = action  # start, delete, rebuild
        self.should_stop = False
        self.process = None
        
    def run(self):
        """执行索引操作"""
        try:
            if self.action == "start":
                self._start_indexing()
            elif self.action == "delete":
                self._delete_index()
            elif self.action == "rebuild":
                self._rebuild_index()
        except Exception as e:
            self.error_occurred.emit(f"索引操作失败: {str(e)}")
            self.finished.emit(False, str(e))
    
    def _start_indexing(self):
        """开始索引"""
        self.status_updated.emit("正在启动索引...")

        try:
            # 调用CLI命令 - 这会持续运行并监听文件变化
            cmd = ["uv", "run", "cli/index_cli.py", "start"]

            # 设置环境变量禁用Python缓冲
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['PYTHONIOENCODING'] = 'utf-8'

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,  # 无缓冲
                universal_newlines=True,
                env=env,
                cwd=Path(__file__).parent.parent  # 确保在正确的目录运行
            )

            self.status_updated.emit("索引服务已启动，正在持续监控文件变化...")

            # 持续监控进程状态
            self.status_updated.emit("索引服务正在运行，监控文件变化中...")

            while True:
                if self.should_stop:
                    self.process.terminate()
                    self.status_updated.emit("正在停止索引服务...")
                    break

                # 检查进程是否结束
                if self.process.poll() is not None:
                    break

                # 简化的输出读取机制
                try:
                    # 使用非阻塞读取
                    import select

                    # 使用select进行非阻塞读取
                    if hasattr(select, 'select'):
                        ready, _, _ = select.select([self.process.stdout], [], [], 0.1)
                        if ready:
                            line = self.process.stdout.readline()
                            if line:
                                line = line.strip()
                                if line:
                                    self.status_updated.emit(line)
                                    # 解析进度信息
                                    if "已处理:" in line:
                                        try:
                                            parts = line.split("已处理:")
                                            if len(parts) > 1:
                                                file_count = parts[1].split("文件")[0].strip().replace(",", "")
                                                self.progress_updated.emit(line, int(file_count), 0)
                                        except:
                                            pass
                    else:
                        # Windows fallback: 使用简单的readline
                        try:
                            line = self.process.stdout.readline()
                            if line:
                                line = line.strip()
                                if line:
                                    self.status_updated.emit(line)
                                    # 解析进度信息
                                    if "已处理:" in line:
                                        try:
                                            parts = line.split("已处理:")
                                            if len(parts) > 1:
                                                file_count = parts[1].split("文件")[0].strip().replace(",", "")
                                                self.progress_updated.emit(line, int(file_count), 0)
                                        except:
                                            pass
                        except:
                            pass

                except Exception as e:
                    pass

                # 短暂休眠避免CPU占用过高
                time.sleep(0.1)

            # 检查返回码
            return_code = self.process.poll()
            if return_code == 0 or self.should_stop:
                self.finished.emit(True, "索引服务已停止")
            else:
                stderr = self.process.stderr.read()
                self.finished.emit(False, f"索引服务异常退出: {stderr}")

        except Exception as e:
            self.error_occurred.emit(f"启动索引失败: {str(e)}")
            self.finished.emit(False, str(e))
    
    def _delete_index(self):
        """删除索引"""
        self.status_updated.emit("正在删除索引...")

        try:
            # 删除数据库文件
            db_path = get_default_db_path()
            if db_path.exists():
                db_path.unlink()
                self.status_updated.emit("索引数据库已删除")

                # 同时删除相关的 WAL 和 SHM 文件
                for suffix in ['-wal', '-shm']:
                    related_file = db_path.parent / f'{db_path.name}{suffix}'
                    if related_file.exists():
                        related_file.unlink()
            else:
                self.status_updated.emit("未找到索引数据库")

            self.finished.emit(True, "索引删除完成")

        except Exception as e:
            self.error_occurred.emit(f"删除索引失败: {str(e)}")
            self.finished.emit(False, str(e))

    def _rebuild_index(self):
        """重建索引"""
        self.status_updated.emit("正在重建索引...")

        try:
            # 第一步：删除数据库文件
            db_path = get_default_db_path()
            if db_path.exists():
                db_path.unlink()
                self.status_updated.emit("已删除旧索引数据库")

                # 同时删除相关的 WAL 和 SHM 文件
                for suffix in ['-wal', '-shm']:
                    related_file = db_path.parent / f'{db_path.name}{suffix}'
                    if related_file.exists():
                        related_file.unlink()

            # 第二步：调用初始化命令重建索引
            self.status_updated.emit("正在重新建立索引...")
            cmd = ["uv", "run", "cli/index_cli.py", "init"]

            # 设置环境变量禁用Python缓冲
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            env['PYTHONIOENCODING'] = 'utf-8'

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0,  # 无缓冲
                universal_newlines=True,
                env=env,
                cwd=Path(__file__).parent.parent  # 确保在正确的目录运行
            )

            # 监控进程输出
            while True:
                if self.should_stop:
                    self.process.terminate()
                    self.status_updated.emit("重建索引已取消")
                    break

                # 检查进程是否结束
                if self.process.poll() is not None:
                    break

                # 读取输出
                try:
                    line = self.process.stdout.readline()
                    if line:
                        line = line.strip()
                        self.status_updated.emit(line)
                        # 解析进度信息
                        if "已处理:" in line:
                            try:
                                parts = line.split("已处理:")
                                if len(parts) > 1:
                                    file_count = parts[1].split("文件")[0].strip().replace(",", "")
                                    self.progress_updated.emit(line, int(file_count), 0)
                            except:
                                pass
                except:
                    pass

                # 短暂休眠避免CPU占用过高
                time.sleep(0.1)

            # 检查返回码
            return_code = self.process.poll()
            if return_code == 0:
                self.finished.emit(True, "索引重建完成")
            else:
                stderr = self.process.stderr.read()
                self.finished.emit(False, f"索引重建失败: {stderr}")

        except Exception as e:
            self.error_occurred.emit(f"重建索引失败: {str(e)}")
            self.finished.emit(False, str(e))
    
    def stop(self):
        """停止操作"""
        self.should_stop = True
        if self.process and self.process.poll() is None:
            self.process.terminate()
            # 等待进程结束
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
        self.status_updated.emit("正在停止索引操作...")


class SearchWorker(QThread):
    """搜索工作线程"""

    # 信号定义
    results_ready = Signal(list)  # 搜索结果
    search_finished = Signal(int, float)  # 结果数量, 搜索耗时
    error_occurred = Signal(str)  # 错误消息

    def __init__(self, query: str, max_results: int = 100, use_regex: bool = False):
        super().__init__()
        self.query = query
        self.max_results = max_results
        self.use_regex = use_regex

        # 初始化搜索组件
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        self.search_engine = SearchEngine(self.config_manager, self.db_manager)
    
    def run(self):
        """执行搜索"""
        try:
            start_time = time.time()

            # 执行搜索，使用use_regex参数
            results = self.search_engine.search(
                query=self.query,
                max_results=self.max_results,
                use_regex=self.use_regex
            )

            search_time = time.time() - start_time

            # 发送结果
            self.results_ready.emit(results)
            self.search_finished.emit(len(results), search_time)

        except Exception as e:
            self.error_occurred.emit(f"搜索失败: {str(e)}")
        finally:
            # 清理资源
            self.db_manager.close()
            self.config_manager.cleanup()


class ConfigWorker(QThread):
    """配置管理工作线程"""
    
    # 信号定义
    directories_loaded = Signal(list)  # 目录列表
    directory_added = Signal(str)  # 添加的目录
    directory_removed = Signal(str)  # 移除的目录
    error_occurred = Signal(str)  # 错误消息
    
    def __init__(self, action: str, directory: str = ""):
        super().__init__()
        self.action = action  # load, add, remove
        self.directory = directory
        self.config_manager = ConfigManager()
    
    def run(self):
        """执行配置操作"""
        try:
            if self.action == "load":
                self._load_directories()
            elif self.action == "add":
                self._add_directory()
            elif self.action == "remove":
                self._remove_directory()
        except Exception as e:
            self.error_occurred.emit(f"配置操作失败: {str(e)}")
        finally:
            self.config_manager.cleanup()
    
    def _load_directories(self):
        """加载目录列表"""
        config = self.config_manager.get_index_config()
        self.directories_loaded.emit(config.directories)
    
    def _add_directory(self):
        """添加目录"""
        if self.directory:
            self.config_manager.add_index_directory(self.directory)
            self.directory_added.emit(self.directory)
    
    def _remove_directory(self):
        """移除目录"""
        if self.directory:
            self.config_manager.remove_index_directory(self.directory)
            self.directory_removed.emit(self.directory)


class FolderSizeWorker(QThread):
    """文件夹大小计算工作线程"""

    # 信号定义
    progress_updated = Signal(str, int, int)  # 消息, 已处理文件数, 总文件数
    size_calculated = Signal(int, int, int)  # 总大小(字节), 文件数, 文件夹数
    error_occurred = Signal(str)  # 错误消息
    finished = Signal()  # 完成信号

    def __init__(self, folder_path: str):
        super().__init__()
        self.folder_path = folder_path
        self.should_stop = False
        self.total_size = 0
        self.file_count = 0
        self.folder_count = 0
        self.processed_count = 0

    def stop(self):
        """停止计算"""
        self.should_stop = True

    def run(self):
        """执行文件夹大小计算"""
        try:
            self.progress_updated.emit("正在扫描文件夹...", 0, 0)

            # 首先快速扫描获取总文件数
            total_items = self._count_items(self.folder_path)
            if self.should_stop:
                return

            self.progress_updated.emit(f"开始计算大小，共 {total_items} 个项目", 0, total_items)

            # 计算大小
            self._calculate_size(self.folder_path, total_items)

            if not self.should_stop:
                self.size_calculated.emit(self.total_size, self.file_count, self.folder_count)

        except Exception as e:
            self.error_occurred.emit(f"计算文件夹大小失败: {str(e)}")
        finally:
            self.finished.emit()

    def _count_items(self, folder_path: str) -> int:
        """快速计算文件夹中的项目总数"""
        count = 0
        try:
            for root, dirs, files in os.walk(folder_path):
                if self.should_stop:
                    break
                count += len(files) + len(dirs)
        except (OSError, PermissionError):
            pass
        return count

    def _calculate_size(self, folder_path: str, total_items: int):
        """递归计算文件夹大小"""
        try:
            for root, dirs, files in os.walk(folder_path):
                if self.should_stop:
                    break

                # 计算文件夹数量
                self.folder_count += len(dirs)

                # 计算文件大小
                for file_name in files:
                    if self.should_stop:
                        break

                    file_path = os.path.join(root, file_name)
                    try:
                        file_size = os.path.getsize(file_path)
                        self.total_size += file_size
                        self.file_count += 1
                    except (OSError, PermissionError):
                        # 跳过无法访问的文件
                        pass

                    self.processed_count += 1

                    # 每处理100个文件更新一次进度
                    if self.processed_count % 100 == 0:
                        self.progress_updated.emit(
                            f"正在计算... {self.processed_count}/{total_items}",
                            self.processed_count,
                            total_items
                        )

                # 更新文件夹处理进度
                for _ in dirs:
                    self.processed_count += 1
                    if self.processed_count % 100 == 0:
                        self.progress_updated.emit(
                            f"正在计算... {self.processed_count}/{total_items}",
                            self.processed_count,
                            total_items
                        )

        except (OSError, PermissionError) as e:
            self.error_occurred.emit(f"访问文件夹失败: {str(e)}")
