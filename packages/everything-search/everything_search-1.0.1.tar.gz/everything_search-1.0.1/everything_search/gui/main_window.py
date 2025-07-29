#!/usr/bin/env python3
"""
主窗口类
整合搜索和设置页面
"""

import sys
from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QMenuBar, QStatusBar, QMessageBox, QApplication
)
from PySide6.QtCore import Qt, QTimer, QSettings
from PySide6.QtGui import QAction, QKeySequence, QIcon

from .search_tab import SearchTab
from .settings_tab import SettingsTab


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()

        # 初始化设置
        self.settings = QSettings("EverythingSearch", "MainWindow")

        self._setup_ui()
        self._setup_menu()
        self._setup_status_bar()
        self._connect_signals()

        # 恢复窗口状态
        self._restore_window_state()

        # 检查是否需要自动开启索引
        self._check_auto_start_index()
    
    def _setup_ui(self):
        """设置界面"""
        self.setWindowTitle("Everything Search - 高性能文件搜索工具 QQ:1715109585")
        self.setMinimumSize(600, 420)
        # 不在这里设置默认大小，将在_restore_window_state中处理
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建布局
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建选项卡
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        
        # 创建搜索页面
        self.search_tab = SearchTab()
        self.tab_widget.addTab(self.search_tab, "🔍 搜索")
        
        # 创建设置页面
        self.settings_tab = SettingsTab()
        self.tab_widget.addTab(self.settings_tab, "⚙️ 设置")
        
        layout.addWidget(self.tab_widget)
    
    def _setup_menu(self):
        """设置菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        # 退出动作
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.setStatusTip("退出应用程序")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        # 关于
        about_action = QAction("关于(&A)", self)
        about_action.setStatusTip("关于Everything Search")
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _setup_status_bar(self):
        """设置状态栏"""
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("准备就绪")
        
        # 定时更新状态
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self._update_status)
        self.status_timer.start(5000)  # 每5秒更新一次
    
    def _connect_signals(self):
        """连接信号"""
        # 选项卡切换信号
        self.tab_widget.currentChanged.connect(self._on_tab_changed)

        # 连接搜索页面的状态信号到状态栏
        self.search_tab.status_message.connect(self.status_bar.showMessage)
    
    def _focus_search(self):
        """聚焦搜索框"""
        self.tab_widget.setCurrentIndex(0)  # 切换到搜索页面
        self.search_tab.focus_search_input()
    
    def _start_indexing(self):
        """开始索引"""
        self.tab_widget.setCurrentIndex(1)  # 切换到设置页面
        if not self.settings_tab.is_indexing:
            self.settings_tab._start_indexing()
    
    def _rebuild_index(self):
        """重建索引"""
        self.tab_widget.setCurrentIndex(1)  # 切换到设置页面
        self.settings_tab._rebuild_index()
    
    def _on_tab_changed(self, index: int):
        """选项卡切换"""
        if index == 0:
            self.status_bar.showMessage("搜索页面")
        elif index == 1:
            self.status_bar.showMessage("设置页面")
    
    def _update_status(self):
        """更新状态栏"""
        current_tab = self.tab_widget.currentIndex()
        if current_tab == 0:
            # 搜索页面状态
            pass
        elif current_tab == 1:
            # 设置页面状态
            pass
    
    def _check_auto_start_index(self):
        """检查是否需要自动开启索引"""
        try:
            # 延迟检查，等待界面完全加载
            QTimer.singleShot(1000, self._perform_auto_start_check)
        except Exception as e:
            print(f"自动开启索引检查失败: {e}")

    def _perform_auto_start_check(self):
        """执行自动开启索引检查"""
        try:
            # 检查设置页面的自动开启选项
            if hasattr(self.settings_tab, 'auto_start_checkbox') and self.settings_tab.auto_start_checkbox.isChecked():
                # 检查是否已有索引在运行
                if not (hasattr(self.settings_tab, 'index_worker') and
                       self.settings_tab.index_worker and
                       self.settings_tab.index_worker.isRunning()):

                    # 自动开启索引
                    self.settings_tab.index_log.append("🚀 自动启动索引模式...")

                    # 直接调用开始索引，跳过确认对话框
                    self.settings_tab._start_indexing(auto_start=True)
        except Exception as e:
            print(f"自动开启索引失败: {e}")

    def _save_window_state(self):
        """保存窗口状态"""
        try:
            self.settings.setValue("geometry", self.saveGeometry())
            self.settings.setValue("windowState", self.saveState())
            self.settings.setValue("size", self.size())
            self.settings.setValue("position", self.pos())
        except Exception as e:
            print(f"保存窗口状态失败: {e}")

    def _restore_window_state(self):
        """恢复窗口状态"""
        try:
            # 恢复几何信息
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)

            # 恢复窗口状态
            window_state = self.settings.value("windowState")
            if window_state:
                self.restoreState(window_state)

            # 如果没有保存的几何信息，使用默认大小和位置
            if not geometry:
                # 获取屏幕尺寸并居中显示
                screen = QApplication.primaryScreen().geometry()
                default_width = 800
                default_height = 600
                x = (screen.width() - default_width) // 2
                y = (screen.height() - default_height) // 2
                self.setGeometry(x, y, default_width, default_height)

        except Exception as e:
            print(f"恢复窗口状态失败: {e}")
            # 使用默认大小
            self.resize(800, 600)



    def _show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>Everything Search</h2>
        <p><b>版本:</b> 1.0.0</p>
        <p><b>描述:</b> 高性能文件搜索工具 QQ:1715109585</p>
        <p>类似于Windows Everything的macOS解决方案，使用Python开发。</p>
        <p><b>特性:</b></p>
        <ul>
        <li>快速文件索引</li>
        <li>实时搜索</li>
        <li>多种搜索模式</li>
        <li>文件监控</li>
        <li>自动索引启动</li>
        </ul>
        <p><b>开发团队:</b> Everything Search Team</p>
        """

        QMessageBox.about(self, "关于 Everything Search", about_text)
    
    def closeEvent(self, event):
        """关闭事件"""
        # 保存窗口状态
        self._save_window_state()

        # 停止所有工作线程
        if hasattr(self.search_tab, 'search_worker') and self.search_tab.search_worker:
            if self.search_tab.search_worker.isRunning():
                self.search_tab.search_worker.terminate()
                self.search_tab.search_worker.wait()

        if hasattr(self.settings_tab, 'index_worker') and self.settings_tab.index_worker:
            if self.settings_tab.index_worker.isRunning():
                self.settings_tab.index_worker.stop()
                self.settings_tab.index_worker.wait()

        if hasattr(self.settings_tab, 'config_worker') and self.settings_tab.config_worker:
            if self.settings_tab.config_worker.isRunning():
                self.settings_tab.config_worker.terminate()
                self.settings_tab.config_worker.wait()

        event.accept()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    
    # 设置应用程序信息
    app.setApplicationName("Everything Search")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Everything Search Team")
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 启动应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
