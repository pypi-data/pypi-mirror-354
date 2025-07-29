#!/usr/bin/env python3
"""
设置页面组件
包含索引管理和配置管理
"""

import sys
from pathlib import Path
from typing import List, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QListWidget, QListWidgetItem, QGroupBox, QMessageBox,
    QFileDialog, QTextEdit, QSplitter, QCheckBox, QLineEdit,
    QTabWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from .worker_threads import IndexWorker, ConfigWorker


class SettingsTab(QWidget):
    """设置页面"""
    
    def __init__(self):
        super().__init__()
        self.index_worker: Optional[IndexWorker] = None
        self.config_worker: Optional[ConfigWorker] = None
        self.is_indexing = False  # 跟踪索引状态

        self._setup_ui()
        self._connect_signals()
        self._load_directories()
    
    def _setup_ui(self):
        """设置界面"""
        layout = QVBoxLayout(self)

        # 创建选项卡
        self.settings_tabs = QTabWidget()

        # 创建三个选项卡
        self._create_index_management_tab()
        self._create_index_status_tab()
        self._create_config_management_tab()

        layout.addWidget(self.settings_tabs)
        layout.setContentsMargins(10, 10, 10, 10)
    
    def _create_index_management_tab(self):
        """创建索引管理选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 自动开启索引选项
        self.auto_start_checkbox = QCheckBox("启动软件时自动开启索引模式")
        self.auto_start_checkbox.setChecked(True)  # 默认开启
        layout.addWidget(self.auto_start_checkbox)

        # 按钮区域
        button_layout = QHBoxLayout()

        self.toggle_index_button = QPushButton("开始实时索引")
        self.toggle_index_button.setMinimumHeight(40)
        button_layout.addWidget(self.toggle_index_button)

        self.rebuild_index_button = QPushButton("重建索引")
        self.rebuild_index_button.setMinimumHeight(40)
        button_layout.addWidget(self.rebuild_index_button)

        layout.addLayout(button_layout)

        # 索引状态和日志显示（合并为一个大的文本框）
        self.index_log = QTextEdit()
        self.index_log.setMinimumHeight(200)
        self.index_log.setMaximumHeight(300)  # 设置最大高度以确保滚动条出现
        self.index_log.setReadOnly(True)
        # 设置滚动条策略
        self.index_log.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.index_log.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 设置自动换行
        self.index_log.setLineWrapMode(QTextEdit.WidgetWidth)
        self.index_log.append("索引状态: 准备就绪")
        layout.addWidget(self.index_log)

        self.settings_tabs.addTab(tab, "索引管理")

    def _create_index_status_tab(self):
        """创建索引状态选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 状态标题
        status_label = QLabel("索引统计信息")
        layout.addWidget(status_label)

        # 统计信息显示区域
        self.stats_text = QTextEdit("正在加载统计信息...")
        self.stats_text.setReadOnly(True)
        self.stats_text.setMinimumHeight(200)
        self.stats_text.setMaximumHeight(400)
        # 设置滚动条策略
        self.stats_text.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.stats_text.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        # 设置自动换行
        self.stats_text.setLineWrapMode(QTextEdit.WidgetWidth)
        layout.addWidget(self.stats_text)

        # 刷新按钮
        refresh_stats_button = QPushButton("刷新统计信息")
        refresh_stats_button.setMinimumHeight(35)
        refresh_stats_button.clicked.connect(self._refresh_statistics)
        layout.addWidget(refresh_stats_button)

        layout.addStretch()

        self.settings_tabs.addTab(tab, "索引状态")

        # 初始加载统计信息
        self._refresh_statistics()

    def _refresh_statistics(self):
        """刷新统计信息"""
        try:
            from pathlib import Path

            # 基本信息
            stats_text = f"""📊 Everything Search 索引状态
{'=' * 50}

"""

            # 尝试获取数据库信息
            try:
                from core.database import DatabaseManager
                from core.config_manager import ConfigManager

                config_manager = ConfigManager()
                db_manager = DatabaseManager()

                # 检查数据库文件
                db_path = Path(db_manager.db_path)
                if db_path.exists():
                    db_size = db_path.stat().st_size
                    stats_text += f"""💾 数据库信息:
文件路径:     {db_path.name}
文件大小:     {self._format_size(db_size)}
修改时间:     {self._format_time(db_path.stat().st_mtime)}

"""

                    # 尝试获取统计信息
                    try:
                        stats = db_manager.get_statistics()
                        stats_text += f"""📊 索引统计:
总文件数:     {stats['total_files']:,}
目录数:       {stats['total_directories']:,}
普通文件数:   {stats['total_regular_files']:,}
最后更新:     {self._format_time(stats['last_update'])}

"""
                    except Exception as e:
                        stats_text += f"⚠️  无法读取索引统计: {str(e)}\n\n"

                else:
                    stats_text += "⚠️  数据库文件不存在，请先建立索引\n\n"

                # 配置信息
                try:
                    config = config_manager.get_index_config()
                    stats_text += "📁 监控目录:\n"
                    for directory in config.directories:
                        exists = "✅" if Path(directory).exists() else "❌"
                        stats_text += f"   {exists} {directory}\n"
                except Exception as e:
                    stats_text += f"⚠️  无法读取配置: {str(e)}\n"

            except Exception as e:
                stats_text += f"⚠️  无法初始化数据库: {str(e)}\n"
                stats_text += "请检查数据库文件是否正常或重新建立索引"

            self.stats_text.setPlainText(stats_text)

        except Exception as e:
            self.stats_text.setPlainText(f"获取统计信息出错:\n{str(e)}")

    def _format_time(self, timestamp):
        """格式化时间"""
        if not timestamp:
            return "从未"

        try:
            import datetime
            dt = datetime.datetime.fromtimestamp(timestamp)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return "无效时间"

    def _format_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes == 0:
            return "0B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1

        return f"{size_bytes:.1f}{size_names[i]}"

    def _create_config_management_tab(self):
        """创建配置管理选项卡"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 创建内部选项卡
        config_tabs = QTabWidget()

        # 监控目录选项卡
        directories_tab = QWidget()
        directories_layout = QVBoxLayout(directories_tab)

        # 标题
        title_label = QLabel("监控目录列表:")
        directories_layout.addWidget(title_label)

        # 目录列表
        self.directory_list = QListWidget()
        self.directory_list.setMinimumHeight(150)
        directories_layout.addWidget(self.directory_list)

        # 按钮区域
        button_layout = QHBoxLayout()

        self.add_directory_button = QPushButton("添加目录")
        self.add_directory_button.setMinimumHeight(35)
        button_layout.addWidget(self.add_directory_button)

        self.remove_directory_button = QPushButton("移除目录")
        self.remove_directory_button.setMinimumHeight(35)
        self.remove_directory_button.setEnabled(False)
        button_layout.addWidget(self.remove_directory_button)

        button_layout.addStretch()

        directories_layout.addLayout(button_layout)

        config_tabs.addTab(directories_tab, "监控目录")

        # 排除设置选项卡
        exclude_tab = QWidget()
        exclude_layout = QVBoxLayout(exclude_tab)

        # 排除文件夹
        exclude_dirs_label = QLabel("排除文件夹 (每行一个):")
        exclude_layout.addWidget(exclude_dirs_label)

        self.exclude_dirs_text = QTextEdit()
        self.exclude_dirs_text.setMaximumHeight(100)
        self.exclude_dirs_text.setPlaceholderText(".git\nnode_modules\n__pycache__\n.venv")
        exclude_layout.addWidget(self.exclude_dirs_text)

        # 排除扩展名
        exclude_exts_label = QLabel("排除扩展名 (每行一个):")
        exclude_layout.addWidget(exclude_exts_label)

        self.exclude_exts_text = QTextEdit()
        self.exclude_exts_text.setMaximumHeight(100)
        self.exclude_exts_text.setPlaceholderText(".tmp\n.log\n.pyc\n.cache")
        exclude_layout.addWidget(self.exclude_exts_text)

        # 保存按钮
        save_exclude_button = QPushButton("保存排除设置")
        save_exclude_button.setMinimumHeight(35)
        save_exclude_button.clicked.connect(self._save_exclude_settings)
        exclude_layout.addWidget(save_exclude_button)

        config_tabs.addTab(exclude_tab, "排除设置")

        layout.addWidget(config_tabs)

        # 状态显示
        self.config_status_label = QLabel("配置状态: 准备就绪")
        layout.addWidget(self.config_status_label)

        self.settings_tabs.addTab(tab, "配置管理")
    
    def _connect_signals(self):
        """连接信号"""
        # 索引管理信号
        self.toggle_index_button.clicked.connect(self._toggle_indexing)
        self.rebuild_index_button.clicked.connect(self._rebuild_index)

        # 配置管理信号
        self.add_directory_button.clicked.connect(self._add_directory)
        self.remove_directory_button.clicked.connect(self._remove_directory)
        self.directory_list.itemSelectionChanged.connect(self._on_directory_selection_changed)
    
    def _toggle_indexing(self):
        """切换索引状态"""
        if self.is_indexing:
            self._stop_indexing()
        else:
            self._start_indexing()

    def _start_indexing(self, auto_start=False):
        """开始索引"""
        if self.index_worker and self.index_worker.isRunning():
            return

        # 只有手动启动时才显示确认对话框
        if not auto_start:
            reply = QMessageBox.question(
                self, "确认索引",
                "开始索引操作将持续运行，确认继续？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply != QMessageBox.Yes:
                return

        # 更新UI状态
        self.is_indexing = True
        self.toggle_index_button.setText("关闭实时索引")
        self.toggle_index_button.setEnabled(True)
        self.rebuild_index_button.setEnabled(False)

        # 只有手动启动时才清空日志
        if not auto_start:
            self.index_log.clear()

        self.index_log.append("索引状态: 正在启动...")

        # 启动索引线程
        self.index_worker = IndexWorker("start")
        self.index_worker.progress_updated.connect(self._on_index_progress)
        self.index_worker.status_updated.connect(self._on_index_status)
        self.index_worker.finished.connect(self._on_index_finished)
        self.index_worker.error_occurred.connect(self._on_index_error)
        self.index_worker.start()

    def _stop_indexing(self):
        """停止索引"""
        if self.index_worker and self.index_worker.isRunning():
            reply = QMessageBox.question(
                self, "确认停止",
                "确认停止索引操作？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )

            if reply == QMessageBox.Yes:
                self.index_worker.stop()
                self.index_log.append("正在停止索引操作...")
                # UI状态会在 _on_index_finished 中更新
    
    def _rebuild_index(self):
        """重建索引"""
        # 先停止正在运行的索引
        if self.index_worker and self.index_worker.isRunning():
            self.index_worker.stop()
            self.index_worker.wait()

        # 确认对话框
        reply = QMessageBox.warning(
            self, "确认重建",
            "重建索引将删除现有索引数据并重新建立索引，确认继续？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # 更新UI状态
        self.is_indexing = False
        self.toggle_index_button.setText("开始实时索引")
        self.toggle_index_button.setEnabled(False)
        self.rebuild_index_button.setEnabled(False)
        self.index_log.clear()
        self.index_log.append("索引状态: 正在重建...")

        # 启动重建线程
        self.index_worker = IndexWorker("rebuild")
        self.index_worker.progress_updated.connect(self._on_index_progress)
        self.index_worker.status_updated.connect(self._on_index_status)
        self.index_worker.finished.connect(self._on_index_finished)
        self.index_worker.error_occurred.connect(self._on_index_error)
        self.index_worker.start()
    
    def _add_directory(self):
        """添加目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择要监控的目录", str(Path.home())
        )
        
        if directory:
            # 检查是否已存在
            for i in range(self.directory_list.count()):
                if self.directory_list.item(i).text() == directory:
                    QMessageBox.information(self, "提示", "该目录已在监控列表中")
                    return
            
            # 添加到配置
            self.config_worker = ConfigWorker("add", directory)
            self.config_worker.directory_added.connect(self._on_directory_added)
            self.config_worker.error_occurred.connect(self._on_config_error)
            self.config_worker.start()
    
    def _remove_directory(self):
        """移除目录"""
        current_item = self.directory_list.currentItem()
        if not current_item:
            return
        
        directory = current_item.text()
        
        # 确认对话框
        reply = QMessageBox.question(
            self, "确认移除", 
            f"确认移除监控目录？\n{directory}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.config_worker = ConfigWorker("remove", directory)
            self.config_worker.directory_removed.connect(self._on_directory_removed)
            self.config_worker.error_occurred.connect(self._on_config_error)
            self.config_worker.start()
    
    def _load_directories(self):
        """加载目录列表"""
        self.config_status_label.setText("配置状态: 正在加载...")

        self.config_worker = ConfigWorker("load")
        self.config_worker.directories_loaded.connect(self._on_directories_loaded)
        self.config_worker.error_occurred.connect(self._on_config_error)
        self.config_worker.start()

        # 同时加载排除设置
        self._load_exclude_settings()

    def _save_exclude_settings(self):
        """保存排除设置"""
        try:
            from core.config_manager import ConfigManager
            config_manager = ConfigManager()

            # 获取排除文件夹
            exclude_dirs_text = self.exclude_dirs_text.toPlainText().strip()
            exclude_dirs = [line.strip() for line in exclude_dirs_text.split('\n') if line.strip()]

            # 获取排除扩展名
            exclude_exts_text = self.exclude_exts_text.toPlainText().strip()
            exclude_exts = [line.strip() for line in exclude_exts_text.split('\n') if line.strip()]

            # 更新配置
            config = config_manager.get_index_config()
            config.exclude_dirs = exclude_dirs
            config.exclude_extensions = exclude_exts

            # 保存配置
            config_manager.save_index_config(config)

            self.config_status_label.setText("配置状态: 排除设置已保存")
            QMessageBox.information(self, "保存成功", "排除设置已保存")

        except Exception as e:
            self.config_status_label.setText("配置状态: 保存失败")
            QMessageBox.warning(self, "保存失败", f"保存排除设置失败:\n{str(e)}")

    def _load_exclude_settings(self):
        """加载排除设置"""
        try:
            from core.config_manager import ConfigManager
            config_manager = ConfigManager()
            config = config_manager.get_index_config()

            # 设置排除文件夹
            exclude_dirs_text = '\n'.join(config.exclude_dirs)
            self.exclude_dirs_text.setPlainText(exclude_dirs_text)

            # 设置排除扩展名
            exclude_exts_text = '\n'.join(config.exclude_extensions)
            self.exclude_exts_text.setPlainText(exclude_exts_text)

        except Exception as e:
            print(f"加载排除设置失败: {e}")
    
    def _on_directory_selection_changed(self):
        """目录选择改变"""
        has_selection = self.directory_list.currentItem() is not None
        self.remove_directory_button.setEnabled(has_selection)
    
    # 索引相关回调
    def _on_index_progress(self, message: str, processed: int, total: int):
        """索引进度更新"""
        self.index_log.append(message)

    def _on_index_status(self, message: str):
        """索引状态更新"""
        self.index_log.append(message)
        # 自动滚动到底部
        self.index_log.verticalScrollBar().setValue(
            self.index_log.verticalScrollBar().maximum()
        )

    def _on_index_finished(self, success: bool, message: str):
        """索引完成"""
        self.is_indexing = False
        self.toggle_index_button.setText("开始实时索引")
        self.toggle_index_button.setEnabled(True)
        self.rebuild_index_button.setEnabled(True)

        if success:
            self.index_log.append(f"✅ 索引状态: 完成 - {message}")
        else:
            self.index_log.append(f"❌ 索引状态: 失败 - {message}")

    def _on_index_error(self, error_msg: str):
        """索引错误"""
        self.is_indexing = False
        self.toggle_index_button.setText("开始实时索引")
        self.toggle_index_button.setEnabled(True)
        self.rebuild_index_button.setEnabled(True)
        self.index_log.append(f"❌ 索引状态: 错误 - {error_msg}")

        QMessageBox.critical(self, "索引错误", f"索引操作失败:\n{error_msg}")
    
    # 配置相关回调
    def _on_directories_loaded(self, directories: List[str]):
        """目录列表加载完成"""
        self.directory_list.clear()
        for directory in directories:
            item = QListWidgetItem(directory)
            self.directory_list.addItem(item)
        
        self.config_status_label.setText(f"配置状态: 已加载 {len(directories)} 个目录")
    
    def _on_directory_added(self, directory: str):
        """目录添加完成"""
        item = QListWidgetItem(directory)
        self.directory_list.addItem(item)
        self.config_status_label.setText(f"配置状态: 已添加 {directory}")
    
    def _on_directory_removed(self, directory: str):
        """目录移除完成"""
        for i in range(self.directory_list.count()):
            if self.directory_list.item(i).text() == directory:
                self.directory_list.takeItem(i)
                break
        
        self.config_status_label.setText(f"配置状态: 已移除 {directory}")
    
    def _on_config_error(self, error_msg: str):
        """配置错误"""
        self.config_status_label.setText("配置状态: 错误")
        QMessageBox.warning(self, "配置错误", f"配置操作失败:\n{error_msg}")
