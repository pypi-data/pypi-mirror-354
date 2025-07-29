#!/usr/bin/env python3
"""
GUI对话框组件
包含文件夹大小计算相关的对话框
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QTextEdit, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))


class FolderSizeProgressDialog(QDialog):
    """文件夹大小计算进度对话框"""
    
    def __init__(self, folder_path: str, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.worker = None
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("计算文件夹大小")
        self.setModal(True)
        self.resize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # 文件夹路径显示
        path_label = QLabel(f"正在计算: {self.folder_path}")
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # 状态标签
        self.status_label = QLabel("准备开始...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self._cancel_calculation)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # 设置布局边距
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
    
    def _connect_signals(self):
        """连接信号"""
        pass
    
    def set_worker(self, worker):
        """设置工作线程"""
        self.worker = worker
        if worker:
            worker.progress_updated.connect(self._on_progress_updated)
            worker.size_calculated.connect(self._on_size_calculated)
            worker.error_occurred.connect(self._on_error_occurred)
            worker.finished.connect(self._on_finished)
    
    def _on_progress_updated(self, message: str, processed: int, total: int):
        """更新进度"""
        self.status_label.setText(message)
        if total > 0:
            progress = int((processed / total) * 100)
            self.progress_bar.setValue(progress)
    
    def _on_size_calculated(self, total_size: int, file_count: int, folder_count: int):
        """大小计算完成"""
        # 显示结果对话框
        result_dialog = FolderSizeResultDialog(
            self.folder_path, total_size, file_count, folder_count, self
        )
        result_dialog.exec()
        self.accept()
    
    def _on_error_occurred(self, error_msg: str):
        """处理错误"""
        QMessageBox.warning(self, "计算错误", f"计算文件夹大小时发生错误:\n{error_msg}")
        self.reject()
    
    def _on_finished(self):
        """计算完成"""
        pass
    
    def _cancel_calculation(self):
        """取消计算"""
        if self.worker:
            self.worker.stop()
        self.reject()


class FolderSizeResultDialog(QDialog):
    """文件夹大小结果显示对话框"""
    
    def __init__(self, folder_path: str, total_size: int, file_count: int, folder_count: int, parent=None):
        super().__init__(parent)
        self.folder_path = folder_path
        self.total_size = total_size
        self.file_count = file_count
        self.folder_count = folder_count
        self._setup_ui()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("文件夹大小统计")
        self.setModal(True)
        self.resize(450, 300)
        
        layout = QVBoxLayout(self)
        
        # 标题
        title_label = QLabel("📊 文件夹大小统计结果")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 文件夹路径
        path_label = QLabel(f"文件夹: {self.folder_path}")
        path_label.setWordWrap(True)
        layout.addWidget(path_label)
        
        # 统计信息
        stats_text = self._format_statistics()
        self.stats_display = QTextEdit()
        self.stats_display.setPlainText(stats_text)
        self.stats_display.setReadOnly(True)
        self.stats_display.setMaximumHeight(150)
        layout.addWidget(self.stats_display)
        
        # 按钮区域
        button_layout = QHBoxLayout()
        
        self.copy_button = QPushButton("📋 复制统计信息")
        self.copy_button.clicked.connect(self._copy_statistics)
        button_layout.addWidget(self.copy_button)
        
        self.close_button = QPushButton("关闭")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        # 设置布局边距
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
    
    def _format_statistics(self) -> str:
        """格式化统计信息"""
        size_str = self._format_size(self.total_size)
        
        stats = f"""📁 文件夹统计信息

📊 总大小:     {size_str}
📄 文件数量:   {self.file_count:,} 个
📂 文件夹数量: {self.folder_count:,} 个
📍 路径:       {self.folder_path}

💡 提示: 点击"复制统计信息"可将此信息复制到剪贴板"""
        
        return stats
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def _copy_statistics(self):
        """复制统计信息到剪贴板"""
        try:
            from PySide6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(self.stats_display.toPlainText())
            
            # 显示复制成功提示
            QMessageBox.information(self, "复制成功", "统计信息已复制到剪贴板")
        except Exception as e:
            QMessageBox.warning(self, "复制失败", f"无法复制到剪贴板:\n{str(e)}")
