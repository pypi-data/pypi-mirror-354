#!/usr/bin/env python3
"""
Everything Search GUI启动脚本
"""

import sys
import os
from pathlib import Path

try:
    from PySide6.QtWidgets import QApplication, QMessageBox
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QIcon
except ImportError:
    print("错误: 未安装PySide6")
    print("请运行: uv add PySide6")
    sys.exit(1)

try:
    # 尝试相对导入
    from .gui.main_window import MainWindow
except ImportError:
    try:
        # 如果相对导入失败，尝试绝对导入
        from everything_search.gui.main_window import MainWindow
    except ImportError as e:
        print(f"错误: 无法导入GUI模块: {e}")
        sys.exit(1)


def check_dependencies():
    """检查依赖项"""
    try:
        # 尝试相对导入
        try:
            from .core.config_manager import ConfigManager
            from .core.database import DatabaseManager
            from .core.search_engine import SearchEngine
            from .core.file_indexer import FileIndexer
        except ImportError:
            # 如果相对导入失败，尝试绝对导入
            from everything_search.core.config_manager import ConfigManager
            from everything_search.core.database import DatabaseManager
            from everything_search.core.search_engine import SearchEngine
            from everything_search.core.file_indexer import FileIndexer
        return True
    except ImportError as e:
        QMessageBox.critical(
            None, "依赖错误",
            f"缺少必要的依赖模块:\n{e}\n\n请确保所有依赖已正确安装。"
        )
        return False


def setup_application():
    """设置应用程序"""
    app = QApplication(sys.argv)

    # 设置Fusion样式
    app.setStyle("Fusion")

    # 设置应用程序属性
    app.setApplicationName("Everything Search")
    app.setApplicationDisplayName("Everything Search")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("Everything Search Team")
    app.setOrganizationDomain("everything-search.com")

    # 设置应用程序图标（如果有的话）
    # app.setWindowIcon(QIcon("icon.png"))

    # 设置高DPI支持 (PySide6中这些属性已过时，会自动处理)
    # app.setAttribute(Qt.AA_EnableHighDpiScaling, True)  # 已过时
    # app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)     # 已过时

    return app


def main():
    """主函数"""
    # 创建应用程序
    app = setup_application()
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    try:
        # 创建主窗口
        window = MainWindow()
        
        # 显示窗口
        window.show()
        
        # 聚焦搜索框
        window._focus_search()
        
        # 运行应用程序
        return app.exec()
        
    except Exception as e:
        QMessageBox.critical(
            None, "启动错误", 
            f"应用程序启动失败:\n{str(e)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
