#!/usr/bin/env python3
"""
搜索页面组件
包含搜索文本框和结果表格
"""

import os
import sys
import time
from pathlib import Path
from typing import List, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QMessageBox,
    QSplitter, QCheckBox, QMenu, QApplication
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QIcon

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from .worker_threads import SearchWorker, FolderSizeWorker
from .dialogs import FolderSizeProgressDialog
from core.search_engine import SearchResult


class SearchTab(QWidget):
    """搜索页面"""

    # 信号定义
    status_message = Signal(str)  # 状态消息信号

    def __init__(self):
        super().__init__()
        self.search_worker: Optional[SearchWorker] = None
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)

        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)

        # 搜索区域
        search_layout = QHBoxLayout()

        # 搜索框
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入搜索关键词...")
        search_layout.addWidget(self.search_input)

        # 正则表达式复选框
        self.regex_checkbox = QCheckBox("使用正则表达式")
        self.regex_checkbox.setToolTip("启用正则表达式搜索模式")
        search_layout.addWidget(self.regex_checkbox)

        layout.addLayout(search_layout)
        
        # 结果表格
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["文件名", "类型", "路径", "大小", "修改时间"])

        # 设置表格属性
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.results_table.setSortingEnabled(True)
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)  # 禁用编辑模式
        self.results_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results_table.customContextMenuRequested.connect(self._show_context_menu)

        # 设置固定行高
        self.results_table.verticalHeader().setDefaultSectionSize(25)  # 固定行高25像素
        self.results_table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.results_table.setWordWrap(False)  # 禁用文本换行

        # 设置列宽
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Interactive)  # 文件名
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 类型
        header.setSectionResizeMode(2, QHeaderView.Stretch)      # 路径
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 大小
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 时间

        # 设置初始列宽
        self.results_table.setColumnWidth(0, 200)
        self.results_table.setColumnWidth(1, 80)
        self.results_table.setColumnWidth(3, 100)
        self.results_table.setColumnWidth(4, 150)
        
        layout.addWidget(self.results_table)
        
        # 设置布局边距
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
    
    def _connect_signals(self):
        """连接信号"""
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._perform_search)
        # 移除双击事件，改为右键菜单操作
    
    def _on_search_text_changed(self, text: str):
        """搜索文本改变时的处理"""
        # 延迟搜索，避免频繁查询
        self.search_timer.stop()
        if text.strip():
            self.search_timer.start(300)  # 300ms延迟
        else:
            self._clear_results()
            self.status_message.emit("准备就绪")
    
    def _perform_search(self):
        """执行搜索"""
        query = self.search_input.text().strip()
        if not query:
            self._clear_results()
            self.status_message.emit("准备就绪")
            return

        # 停止之前的搜索
        if self.search_worker and self.search_worker.isRunning():
            self.search_worker.terminate()
            self.search_worker.wait()

        # 显示搜索状态
        self.status_message.emit(f"正在搜索: {query}")

        # 检查是否使用正则表达式
        use_regex = self.regex_checkbox.isChecked()

        # 启动搜索线程
        self.search_worker = SearchWorker(query, max_results=1000, use_regex=use_regex)
        self.search_worker.results_ready.connect(self._on_search_results)
        self.search_worker.search_finished.connect(self._on_search_finished)
        self.search_worker.error_occurred.connect(self._on_search_error)
        self.search_worker.start()
    
    def _on_search_results(self, results: List[SearchResult]):
        """处理搜索结果"""
        self._clear_results()

        if not results:
            self.status_message.emit("未找到匹配的文件")
            return
        
        # 填充表格
        self.results_table.setRowCount(len(results))
        
        for row, result in enumerate(results):
            file_record = result.file_record

            # 文件名
            name_item = QTableWidgetItem(file_record.name)
            if file_record.is_dir:
                name_item.setIcon(self._get_folder_icon())
            else:
                name_item.setIcon(self._get_file_icon(file_record.extension))
            self.results_table.setItem(row, 0, name_item)

            # 类型
            type_text = self._get_file_type_text(file_record)
            type_item = QTableWidgetItem(type_text)
            self.results_table.setItem(row, 1, type_item)

            # 路径
            path_item = QTableWidgetItem(file_record.path)
            path_item.setToolTip(file_record.path)
            self.results_table.setItem(row, 2, path_item)

            # 大小
            if file_record.is_dir:
                size_item = QTableWidgetItem("")
            else:
                size_str = self._format_size(file_record.size)
                size_item = QTableWidgetItem(size_str)
                size_item.setData(Qt.UserRole, file_record.size)  # 存储原始大小用于排序
            self.results_table.setItem(row, 3, size_item)

            # 修改时间
            time_str = self._format_time(file_record.mtime)
            time_item = QTableWidgetItem(time_str)
            time_item.setData(Qt.UserRole, file_record.mtime)  # 存储原始时间用于排序
            self.results_table.setItem(row, 4, time_item)
    
    def _on_search_finished(self, result_count: int, search_time: float):
        """搜索完成"""
        if result_count > 0:
            self.status_message.emit(f"找到 {result_count} 个结果 (耗时 {search_time:.3f} 秒)")
        else:
            self.status_message.emit("未找到匹配的文件")

    def _on_search_error(self, error_msg: str):
        """搜索错误"""
        self.status_message.emit("搜索失败")

        QMessageBox.warning(self, "搜索错误", f"搜索失败:\n{error_msg}")
    


    def _show_context_menu(self, position):
        """显示右键菜单"""
        item = self.results_table.itemAt(position)
        if not item:
            return

        row = item.row()
        path_item = self.results_table.item(row, 2)  # 路径在第3列（索引2）
        name_item = self.results_table.item(row, 0)  # 文件名在第1列（索引0）
        type_item = self.results_table.item(row, 1)  # 类型在第2列（索引1）

        if not path_item or not name_item or not type_item:
            return

        file_path = path_item.text()
        file_name = name_item.text()
        file_type = type_item.text()
        folder_path = str(Path(file_path).parent)

        # 判断是否为文件夹
        is_directory = (file_type == "文件夹")

        # 创建右键菜单
        menu = QMenu(self)

        # 打开文件
        open_action = menu.addAction("📂 打开")
        open_action.triggered.connect(lambda: self._open_file(file_path))

        # 打开访达
        open_finder_action = menu.addAction("📁 打开访达")
        open_finder_action.triggered.connect(lambda: self._open_in_finder(file_path))

        menu.addSeparator()

        # 如果是文件夹，添加计算大小选项
        if is_directory:
            calc_size_action = menu.addAction("📊 计算文件夹大小")
            calc_size_action.triggered.connect(lambda: self._calculate_folder_size_to_table(row, file_path))

            calc_size_detail_action = menu.addAction("📋 显示详细统计信息")
            calc_size_detail_action.triggered.connect(lambda: self._calculate_folder_size_detail(file_path))
            menu.addSeparator()

        # 复制路径
        copy_path_action = menu.addAction("📋 复制路径")
        copy_path_action.triggered.connect(lambda: self._copy_to_clipboard(file_path))

        # 复制文件夹路径
        copy_folder_action = menu.addAction("📂 复制文件夹路径")
        copy_folder_action.triggered.connect(lambda: self._copy_to_clipboard(folder_path))

        # 复制文件名
        copy_name_action = menu.addAction("📄 复制文件名")
        copy_name_action.triggered.connect(lambda: self._copy_to_clipboard(file_name))

        # 显示菜单
        menu.exec(self.results_table.mapToGlobal(position))
    
    def _open_file(self, file_path: str):
        """打开文件或目录"""
        try:
            if sys.platform == "darwin":  # macOS
                os.system(f'open "{file_path}"')
            elif sys.platform == "linux":  # Linux
                os.system(f'xdg-open "{file_path}"')
            elif sys.platform == "win32":  # Windows
                os.system(f'start "" "{file_path}"')
        except Exception as e:
            QMessageBox.warning(self, "打开失败", f"无法打开文件:\n{str(e)}")

    def _open_in_finder(self, file_path: str):
        """在访达中打开文件"""
        try:
            if sys.platform == "darwin":  # macOS
                # 使用 -R 参数在访达中选中文件
                os.system(f'open -R "{file_path}"')
            elif sys.platform == "linux":  # Linux
                # 在文件管理器中打开文件夹
                folder_path = str(Path(file_path).parent)
                os.system(f'xdg-open "{folder_path}"')
            elif sys.platform == "win32":  # Windows
                # 在资源管理器中选中文件
                os.system(f'explorer /select,"{file_path}"')
        except Exception as e:
            QMessageBox.warning(self, "打开失败", f"无法在文件管理器中打开:\n{str(e)}")

    def _copy_to_clipboard(self, text: str):
        """复制文本到剪贴板"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.status_message.emit(f"已复制: {text}")
        except Exception as e:
            QMessageBox.warning(self, "复制失败", f"无法复制到剪贴板:\n{str(e)}")
    
    def _clear_results(self):
        """清空结果"""
        self.results_table.setRowCount(0)
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def _format_time(self, timestamp: float) -> str:
        """格式化时间戳"""
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))

    def _get_file_type_text(self, file_record) -> str:
        """获取文件类型文本"""
        if file_record.is_dir:
            return "文件夹"

        # 根据扩展名判断文件类型
        ext = file_record.extension.lower()

        # 图片文件
        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg']:
            return "图片"
        # 视频文件
        elif ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm', '.m4v']:
            return "视频"
        # 音频文件
        elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a']:
            return "音频"
        # 文档文件
        elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.rtf']:
            return "文档"
        # 代码文件
        elif ext in ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.h', '.php', '.rb', '.go', '.rs']:
            return "代码"
        # 压缩文件
        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']:
            return "压缩包"
        # 可执行文件
        elif ext in ['.exe', '.app', '.deb', '.rpm', '.dmg', '.msi']:
            return "程序"
        else:
            return "文件"

    def _get_file_icon(self, extension: str) -> QIcon:
        """获取文件图标"""
        # 这里可以根据扩展名返回不同的图标
        # 暂时返回空图标
        return QIcon()
    
    def _get_folder_icon(self) -> QIcon:
        """获取文件夹图标"""
        return QIcon()
    
    def focus_search_input(self):
        """聚焦搜索框"""
        self.search_input.setFocus()
        self.search_input.selectAll()

    def _calculate_folder_size_to_table(self, row: int, folder_path: str):
        """计算文件夹大小并更新到表格"""
        try:
            # 检查路径是否存在且为文件夹
            if not Path(folder_path).exists():
                QMessageBox.warning(self, "路径错误", "指定的文件夹不存在")
                return

            if not Path(folder_path).is_dir():
                QMessageBox.warning(self, "路径错误", "指定的路径不是文件夹")
                return

            # 显示计算中状态
            size_item = self.results_table.item(row, 3)  # 大小列
            if size_item:
                size_item.setText("计算中...")
                self.status_message.emit(f"正在计算文件夹大小: {folder_path}")

            # 创建工作线程
            worker = FolderSizeWorker(folder_path)

            # 连接信号
            worker.size_calculated.connect(
                lambda total_size, file_count, folder_count: self._on_folder_size_calculated_for_table(
                    row, total_size, file_count, folder_count
                )
            )
            worker.error_occurred.connect(
                lambda error_msg: self._on_folder_size_error_for_table(row, error_msg)
            )

            # 启动工作线程
            worker.start()

            # 保存worker引用避免被垃圾回收
            if not hasattr(self, '_folder_size_workers'):
                self._folder_size_workers = []
            self._folder_size_workers.append(worker)

        except Exception as e:
            QMessageBox.warning(self, "计算错误", f"启动文件夹大小计算失败:\n{str(e)}")

    def _calculate_folder_size_detail(self, folder_path: str):
        """计算文件夹大小并显示详细统计信息"""
        try:
            # 检查路径是否存在且为文件夹
            if not Path(folder_path).exists():
                QMessageBox.warning(self, "路径错误", "指定的文件夹不存在")
                return

            if not Path(folder_path).is_dir():
                QMessageBox.warning(self, "路径错误", "指定的路径不是文件夹")
                return

            # 创建进度对话框
            progress_dialog = FolderSizeProgressDialog(folder_path, self)

            # 创建工作线程
            worker = FolderSizeWorker(folder_path)
            progress_dialog.set_worker(worker)

            # 启动工作线程
            worker.start()

            # 显示进度对话框
            progress_dialog.exec()

            # 清理工作线程
            if worker.isRunning():
                worker.stop()
                worker.wait()

        except Exception as e:
            QMessageBox.warning(self, "计算错误", f"启动文件夹大小计算失败:\n{str(e)}")

    def _on_folder_size_calculated_for_table(self, row: int, total_size: int, file_count: int, folder_count: int):
        """文件夹大小计算完成，更新表格"""
        try:
            size_item = self.results_table.item(row, 3)  # 大小列
            if size_item:
                size_str = self._format_size(total_size)
                size_item.setText(size_str)
                size_item.setData(Qt.UserRole, total_size)  # 存储原始大小用于排序
                size_item.setToolTip(f"总大小: {size_str}\n文件数: {file_count:,}\n文件夹数: {folder_count:,}")

            self.status_message.emit(f"文件夹大小计算完成: {self._format_size(total_size)}")
        except Exception as e:
            print(f"更新表格失败: {e}")

    def _on_folder_size_error_for_table(self, row: int, error_msg: str):
        """文件夹大小计算出错，更新表格"""
        try:
            size_item = self.results_table.item(row, 3)  # 大小列
            if size_item:
                size_item.setText("计算失败")
                size_item.setToolTip(f"计算失败: {error_msg}")

            self.status_message.emit(f"文件夹大小计算失败: {error_msg}")
        except Exception as e:
            print(f"更新表格失败: {e}")
