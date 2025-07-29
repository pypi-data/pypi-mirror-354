#!/usr/bin/env python3
"""
Everything Search - 索引管理命令行工具
支持功能：
- 初始化索引
- 自动化启动（初始化索引、增量索引、实时监控）
- 重建索引
- 实时监控
- 状态查看
- 配置管理
"""

import argparse
import sys
import time
import signal
from pathlib import Path
from typing import Optional

try:
    # 尝试相对导入
    from ..core.config_manager import ConfigManager
    from ..core.database import DatabaseManager
    from ..core.file_indexer import FileIndexer, IndexProgress
    from ..core.file_watcher import FileWatcher
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from everything_search.core.config_manager import ConfigManager
    from everything_search.core.database import DatabaseManager
    from everything_search.core.file_indexer import FileIndexer, IndexProgress
    from everything_search.core.file_watcher import FileWatcher


class IndexCLI:
    """索引管理命令行界面"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        self.file_indexer = FileIndexer(self.config_manager, self.db_manager)
        self.file_watcher: Optional[FileWatcher] = None

        # 进度跟踪
        self._last_directory = ""
        self._directory_start_time = 0
        self._directory_start_files = 0

        # 设置进度回调
        self.file_indexer.set_progress_callback(self._progress_callback)

        # 信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """信号处理器"""
        print("\n🛑 收到停止信号，正在清理...")

        if self.file_watcher and self.file_watcher.is_running():
            self.file_watcher.stop_watching()

        self.file_indexer.stop()
        self.db_manager.close()
        self.config_manager.cleanup()

        print("✅ 清理完成，程序退出")
        sys.exit(0)

    def _progress_callback(self, progress: IndexProgress):
        """索引进度回调"""
        if progress.processed_files > 0:
            elapsed = time.time() - progress.start_time
            speed = progress.processed_files / elapsed if elapsed > 0 else 0

            # 检查是否切换到新目录
            current_dir = progress.current_path
            if current_dir != self._last_directory:
                # 如果有上一个目录，显示完成信息
                if self._last_directory:
                    dir_elapsed = time.time() - self._directory_start_time
                    dir_files = progress.processed_files - self._directory_start_files
                    dir_speed = dir_files / dir_elapsed if dir_elapsed > 0 else 0
                    print(f"\n✅ 完成索引 {self._last_directory} | "
                          f"文件: {dir_files:,} | 耗时: {dir_elapsed:.2f}秒 | 速度: {dir_speed:.0f} 文件/秒")

                # 开始新目录
                print(f"\n🔄 正在索引 {current_dir}")
                self._last_directory = current_dir
                self._directory_start_time = time.time()
                self._directory_start_files = progress.processed_files

            # 检测输出环境并选择合适的输出格式
            if sys.stdout.isatty():
                # 终端环境：使用覆盖模式
                print(f"\r📊 已处理: {progress.processed_files:,} 文件 | "
                      f"速度: {speed:.0f} 文件/秒", end="", flush=True)
            else:
                # 管道环境：使用逐行输出，每100个文件输出一次
                if progress.processed_files % 100 == 0 or progress.processed_files < 100:
                    print(f"📊 已处理: {progress.processed_files:,} 文件 | "
                          f"速度: {speed:.0f} 文件/秒")
                    sys.stdout.flush()

        # 显示错误
        if progress.errors:
            for error in progress.errors[-5:]:  # 只显示最近5个错误
                print(f"\n⚠️  {error}")
                sys.stdout.flush()
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def _format_time(self, timestamp: Optional[float]) -> str:
        """格式化时间戳"""
        if timestamp is None:
            return "从未"
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    
    def cmd_init(self, args):
        """初始化索引"""
        print("🚀 开始初始化索引...")
        
        # 检查配置
        invalid_dirs = self.config_manager.validate_directories()
        if invalid_dirs:
            print("⚠️  以下目录无效，将被跳过:")
            for dir_path in invalid_dirs:
                print(f"   - {dir_path}")
        
        # 构建索引
        start_time = time.time()
        progress = self.file_indexer.build_full_index()
        elapsed_time = time.time() - start_time

        # 显示最后一个目录的完成信息
        if self._last_directory:
            dir_elapsed = time.time() - self._directory_start_time
            dir_files = progress.processed_files - self._directory_start_files
            dir_speed = dir_files / dir_elapsed if dir_elapsed > 0 else 0
            print(f"\n✅ 完成索引 {self._last_directory} | "
                  f"文件: {dir_files:,} | 耗时: {dir_elapsed:.2f}秒 | 速度: {dir_speed:.0f} 文件/秒")

        print(f"\n✅ 索引初始化完成！")
        print(f"📊 总文件数: {progress.processed_files:,}")
        print(f"⏱️  总耗时: {elapsed_time:.2f} 秒")
        
        if progress.errors:
            print(f"⚠️  遇到 {len(progress.errors)} 个错误")
    

    
    def cmd_rebuild(self, args):
        """重建索引"""
        if not args.force:
            confirm = input("⚠️  重建索引将删除所有现有数据，确认继续？(y/N): ")
            if confirm.lower() != 'y':
                print("❌ 操作已取消")
                return
        
        print("🔄 开始重建索引...")
        progress = self.file_indexer.rebuild_index()

        # 显示最后一个目录的完成信息
        if self._last_directory:
            dir_elapsed = time.time() - self._directory_start_time
            dir_files = progress.processed_files - self._directory_start_files
            dir_speed = dir_files / dir_elapsed if dir_elapsed > 0 else 0
            print(f"\n✅ 完成索引 {self._last_directory} | "
                  f"文件: {dir_files:,} | 耗时: {dir_elapsed:.2f}秒 | 速度: {dir_speed:.0f} 文件/秒")

        print(f"\n✅ 索引重建完成！")
        print(f"📊 总文件数: {progress.processed_files:,}")



    def cmd_start(self, args):
        """自动化启动：检查索引状态，自动初始化或更新，然后启动实时监控"""
        print("🚀 Everything Search 自动化启动...")

        # 显示索引文件路径信息
        db_path = Path(self.db_manager.db_path)
        config_path = Path(self.config_manager.config_path)

        print(f"💾 索引数据库: {db_path.absolute()}")
        print(f"⚙️  配置文件: {config_path.absolute()}")

        # 检查数据库是否存在
        if not db_path.exists():
            print("\n📊 未发现索引数据库，开始初始化索引...")
            self.cmd_init(args)
        else:
            db_size = db_path.stat().st_size
            print(f"📊 发现现有索引数据库 ({self._format_size(db_size)})...")

            # 显示当前状态
            status = self.file_indexer.get_index_status()
            print(f"当前索引: {status['total_files']:,} 个文件")

            # 如果索引文件数为0，使用完整初始化
            if status['total_files'] == 0:
                print("📊 索引为空，开始完整初始化...")
                self.cmd_init(args)
            else:
                # 执行增量更新
                print("🔄 开始增量更新索引...")
                progress = self.file_indexer.update_incremental_index(None, True)
                print(f"\n✅ 增量更新完成！")
                print(f"📊 更新文件数: {progress.processed_files:,}")

        print("\n🔍 启动实时监控...")
        # 启动实时监控
        self.cmd_watch(args)

    def cmd_watch(self, args):
        """启动实时监控"""
        try:
            self.file_watcher = FileWatcher(
                self.config_manager,
                self.db_manager,
                self.file_indexer
            )

            if self.file_watcher.start_watching():
                print("🔍 实时监控已启动，按 Ctrl+C 停止...")

                # 保持运行
                try:
                    while self.file_watcher.is_running():
                        time.sleep(1)
                except KeyboardInterrupt:
                    pass

                self.file_watcher.stop_watching()
            else:
                print("❌ 启动实时监控失败")

        except Exception as e:
            print(f"❌ 实时监控错误: {e}")
    
    def cmd_status(self, args):
        """显示索引状态"""
        print("📊 Everything Search 索引状态")
        print("=" * 50)

        # 索引统计
        status = self.file_indexer.get_index_status()

        print(f"总文件数:     {status['total_files']:,}")
        print(f"目录数:       {status['total_directories']:,}")
        print(f"普通文件数:   {status['total_regular_files']:,}")
        print(f"索引版本:     {status['index_version']}")
        print(f"完整索引:     {self._format_time(status['last_full_index'])}")
        print(f"增量更新:     {self._format_time(status['last_incremental_index'])}")

        # 数据库文件信息
        db_path = Path(self.db_manager.db_path)
        if db_path.exists():
            db_size = db_path.stat().st_size
            print(f"\n💾 数据库信息:")
            print(f"文件路径:     {db_path.absolute()}")
            print(f"文件大小:     {self._format_size(db_size)}")
            print(f"修改时间:     {self._format_time(db_path.stat().st_mtime)}")

        # 配置文件信息
        config_path = Path(self.config_manager.config_path)
        if config_path.exists():
            print(f"\n⚙️  配置文件:")
            print(f"文件路径:     {config_path.absolute()}")
            print(f"修改时间:     {self._format_time(config_path.stat().st_mtime)}")

        # 配置信息
        print("\n📁 监控目录:")
        config = self.config_manager.get_index_config()
        for directory in config.directories:
            exists = "✅" if Path(directory).exists() else "❌"
            print(f"   {exists} {directory}")

        # 实时监控状态
        if hasattr(self, 'file_watcher') and self.file_watcher:
            watch_status = self.file_watcher.get_status()
            print(f"\n🔍 实时监控: {'运行中' if watch_status['running'] else '已停止'}")
            print(f"监控目录数: {watch_status['watched_directories']}/{watch_status['total_directories']}")
    
    def cmd_config(self, args):
        """配置管理"""
        if args.action == "show":
            # 显示当前配置
            config = self.config_manager.get_index_config()
            search_config = self.config_manager.get_search_config()
            perf_config = self.config_manager.get_performance_config()
            
            print("⚙️  当前配置:")
            print("\n📁 索引配置:")
            print(f"   监控目录: {len(config.directories)} 个")
            for directory in config.directories:
                print(f"     - {directory}")
            print(f"   排除目录: {', '.join(config.exclude_dirs)}")
            print(f"   排除扩展名: {', '.join(config.exclude_extensions)}")
            print(f"   最大文件大小: {config.max_file_size_mb} MB")
            print(f"   跟随符号链接: {config.follow_symlinks}")
            print(f"   索引隐藏文件: {config.index_hidden_files}")
            
            print(f"\n🔍 搜索配置:")
            print(f"   大小写敏感: {search_config.case_sensitive}")
            print(f"   模糊搜索: {search_config.fuzzy_search}")
            print(f"   最大结果数: {search_config.max_results}")
            print(f"   结果缓存大小: {search_config.result_cache_size}")
            
            print(f"\n⚡ 性能配置:")
            print(f"   最大工作线程: {perf_config.max_workers}")
            print(f"   批处理大小: {perf_config.batch_size}")
            print(f"   内存限制: {perf_config.memory_limit_mb} MB")
            print(f"   索引块大小: {perf_config.index_chunk_size}")
        
        elif args.action == "add-dir":
            if args.directory:
                self.config_manager.add_index_directory(args.directory)
                print(f"✅ 已添加监控目录: {args.directory}")
            else:
                print("❌ 请指定目录路径")
        



def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Everything Search - 高性能文件索引管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s init                    # 初始化索引
  %(prog)s start                   # 开启索引服务 自动初始化索引 增量索引 实时监控索引
  %(prog)s watch                   # 启动实时监控
  %(prog)s status                  # 查看索引状态
  %(prog)s rebuild                 # 直接删除已经有的数据库文件 然后重建
  %(prog)s config show             # 显示配置
  %(prog)s config add-dir ~/Documents  # 添加监控目录
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # start 命令
    parser_start = subparsers.add_parser('start', help='自动化启动（检查索引状态，自动初始化或更新，然后启动实时监控）')

    # init 命令
    parser_init = subparsers.add_parser('init', help='初始化索引')



    # rebuild 命令
    parser_rebuild = subparsers.add_parser('rebuild', help='重建索引')
    parser_rebuild.add_argument('--force', action='store_true', help='强制重建，不询问确认')



    # watch 命令
    parser_watch = subparsers.add_parser('watch', help='启动实时监控')

    # status 命令
    parser_status = subparsers.add_parser('status', help='显示索引状态')
    
    # config 命令
    parser_config = subparsers.add_parser('config', help='配置管理')
    parser_config.add_argument('action', choices=['show', 'add-dir'],
                              help='配置操作')
    parser_config.add_argument('--directory', help='目录路径（用于 add-dir）')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 创建CLI实例并执行命令
    cli = IndexCLI()
    
    try:
        command_method = getattr(cli, f'cmd_{args.command}')
        command_method(args)
    except KeyboardInterrupt:
        print("\n🛑 操作被用户中断")
    except Exception as e:
        print(f"❌ 执行命令失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        cli.db_manager.close()
        cli.config_manager.cleanup()


if __name__ == "__main__":
    main()
