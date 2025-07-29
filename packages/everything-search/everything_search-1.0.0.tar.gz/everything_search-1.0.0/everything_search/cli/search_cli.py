#!/usr/bin/env python3
"""
Everything Search - 搜索命令行工具
支持功能：
- 快速文件搜索
- 正则表达式搜索
- 按类型、大小、时间搜索
- 结果排序和过滤
"""

import argparse
import sys
import time
import os
from pathlib import Path
from typing import List, Optional

try:
    # 尝试相对导入
    from ..core.config_manager import ConfigManager
    from ..core.database import DatabaseManager
    from ..core.search_engine import SearchEngine, SearchResult
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    from everything_search.core.config_manager import ConfigManager
    from everything_search.core.database import DatabaseManager
    from everything_search.core.search_engine import SearchEngine, SearchResult


class SearchCLI:
    """搜索命令行界面"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.db_manager = DatabaseManager()
        self.search_engine = SearchEngine(self.config_manager, self.db_manager)
    
    def _format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f}{unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f}PB"
    
    def _format_time(self, timestamp: float) -> str:
        """格式化时间戳"""
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))
    
    def _get_file_icon(self, file_record) -> str:
        """获取文件图标"""
        if file_record.is_dir:
            return "📁"
        
        ext = file_record.extension.lower()
        icon_map = {
            '.txt': '📄', '.md': '📄', '.doc': '📄', '.docx': '📄',
            '.pdf': '📕', '.epub': '📗',
            '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
            '.mp3': '🎵', '.wav': '🎵', '.flac': '🎵', '.m4a': '🎵',
            '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬', '.mov': '🎬',
            '.zip': '📦', '.rar': '📦', '.7z': '📦', '.tar': '📦', '.gz': '📦',
            '.py': '🐍', '.js': '📜', '.html': '🌐', '.css': '🎨', '.json': '📋',
            '.exe': '⚙️', '.app': '📱', '.dmg': '💿',
        }
        
        return icon_map.get(ext, '📄')
    
    def _print_results(self, results: List[SearchResult], args):
        """打印搜索结果"""
        if not results:
            print("❌ 未找到匹配的文件")
            return
        
        print(f"🔍 找到 {len(results)} 个结果:")
        print()
        
        for i, result in enumerate(results, 1):
            file_record = result.file_record
            icon = self._get_file_icon(file_record)
            
            # 基本信息
            if args.simple:
                print(f"{file_record.path}")
            else:
                # 详细信息
                size_str = self._format_size(file_record.size) if not file_record.is_dir else ""
                time_str = self._format_time(file_record.mtime)
                
                print(f"{i:3d}. {icon} {result.highlighted_name}")
                print(f"     📍 {file_record.path}")
                
                if not file_record.is_dir:
                    print(f"     📊 {size_str} | 🕒 {time_str}")
                else:
                    print(f"     🕒 {time_str}")
                
                if args.verbose:
                    print(f"     🏷️  匹配类型: {result.match_type}")
                    if file_record.extension:
                        print(f"     📎 扩展名: {file_record.extension}")
                
                print()
    
    def cmd_search(self, args):
        """执行搜索"""
        if not args.query:
            print("❌ 请提供搜索关键词")
            return
        
        # 解析文件类型
        file_types = None
        if args.type:
            file_types = args.type.split(',')

        # 执行搜索
        results = self.search_engine.search(
            query=args.query,
            file_types=file_types,
            max_results=args.limit,
            use_regex=args.regex,
            fuzzy_threshold=args.fuzzy_threshold
        )
        
        # 打印结果
        self._print_results(results, args)
    
    def cmd_extension(self, args):
        """按扩展名搜索"""
        if not args.extension:
            print("❌ 请提供文件扩展名")
            return
        
        results = self.search_engine.search_by_extension(
            extension=args.extension,
            max_results=args.limit
        )

        self._print_results(results, args)
    
    def cmd_size(self, args):
        """按文件大小搜索"""
        def parse_size(size_str: str) -> int:
            """解析大小字符串"""
            if not size_str:
                return 0
            
            size_str = size_str.upper()
            multipliers = {'B': 1, 'K': 1024, 'M': 1024**2, 'G': 1024**3, 'T': 1024**4}
            
            for suffix, multiplier in multipliers.items():
                if size_str.endswith(suffix):
                    return int(float(size_str[:-1]) * multiplier)
            
            # 默认为字节
            return int(size_str)
        
        min_size = parse_size(args.min_size) if args.min_size else 0
        max_size = parse_size(args.max_size) if args.max_size else None
        
        results = self.search_engine.search_by_size(
            min_size=min_size,
            max_size=max_size,
            max_results=args.limit
        )

        self._print_results(results, args)
    
    def cmd_recent(self, args):
        """搜索最近修改的文件"""
        results = self.search_engine.get_recent_files(
            days=args.days,
            max_results=args.limit
        )

        self._print_results(results, args)
    
    def cmd_stats(self, args):
        """显示搜索统计"""
        stats = self.db_manager.get_statistics()
        
        print("📊 Everything Search 统计信息")
        print("=" * 40)
        print(f"总文件数:     {stats['total_files']:,}")
        print(f"目录数:       {stats['total_directories']:,}")
        print(f"普通文件数:   {stats['total_regular_files']:,}")
        
        if stats['last_update']:
            print(f"最后更新:     {self._format_time(stats['last_update'])}")
        
        # 扩展名统计
        if args.extensions:
            print("\n📎 文件扩展名统计 (前20):")
            conn = self.db_manager._get_connection()
            cursor = conn.execute("""
                SELECT extension, COUNT(*) as count 
                FROM files 
                WHERE is_dir = 0 AND extension != ''
                GROUP BY extension 
                ORDER BY count DESC 
                LIMIT 20
            """)
            
            for row in cursor:
                print(f"   {row['extension']:10} {row['count']:>8,} 个文件")
    
    def cmd_open(self, args):
        """打开文件或目录"""
        if not args.query:
            print("❌ 请提供搜索关键词")
            return
        
        # 搜索文件
        results = self.search_engine.search(
            query=args.query,
            max_results=10
        )
        
        if not results:
            print("❌ 未找到匹配的文件")
            return
        
        if len(results) == 1:
            # 只有一个结果，直接打开
            file_path = results[0].file_record.path
            self._open_file(file_path)
        else:
            # 多个结果，让用户选择
            print("🔍 找到多个匹配文件:")
            for i, result in enumerate(results, 1):
                icon = self._get_file_icon(result.file_record)
                print(f"{i:2d}. {icon} {result.file_record.name}")
                print(f"     📍 {result.file_record.path}")
            
            try:
                choice = input("\n请选择要打开的文件 (1-{}): ".format(len(results)))
                index = int(choice) - 1
                
                if 0 <= index < len(results):
                    file_path = results[index].file_record.path
                    self._open_file(file_path)
                else:
                    print("❌ 无效的选择")
            except (ValueError, KeyboardInterrupt):
                print("❌ 操作已取消")
    
    def _open_file(self, file_path: str):
        """打开文件或目录"""
        try:
            if sys.platform == "darwin":  # macOS
                os.system(f'open "{file_path}"')
            elif sys.platform == "linux":  # Linux
                os.system(f'xdg-open "{file_path}"')
            elif sys.platform == "win32":  # Windows
                os.system(f'start "" "{file_path}"')
            else:
                print(f"📍 文件路径: {file_path}")
                return
            
            print(f"✅ 已打开: {file_path}")
        except Exception as e:
            print(f"❌ 打开文件失败: {e}")
            print(f"📍 文件路径: {file_path}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="Everything Search - 高性能文件搜索工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  %(prog)s search "document"           # 搜索包含 document 的文件
  %(prog)s search "*.py" --regex       # 正则表达式搜索
  %(prog)s extension py                # 搜索所有 .py 文件
  %(prog)s size --min-size 100M        # 搜索大于 100MB 的文件
  %(prog)s recent --days 7             # 搜索最近7天修改的文件
  %(prog)s open "config"               # 搜索并打开文件
        """
    )
    
    # 全局参数
    parser.add_argument('--limit', type=int, default=50, help='最大结果数 (默认: 50)')
    parser.add_argument('--simple', action='store_true', help='简单输出模式（仅显示路径）')
    parser.add_argument('--verbose', action='store_true', help='详细输出模式')
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # search 命令
    parser_search = subparsers.add_parser('search', help='搜索文件')
    parser_search.add_argument('query', help='搜索关键词')
    parser_search.add_argument('--type', help='文件类型过滤 (如: dir,file,.py,.txt)')
    parser_search.add_argument('--regex', action='store_true', help='使用正则表达式')
    parser_search.add_argument('--fuzzy-threshold', type=float, default=0.6, 
                              help='模糊搜索阈值 (0.0-1.0, 默认: 0.6)')
    
    # extension 命令
    parser_ext = subparsers.add_parser('extension', help='按扩展名搜索')
    parser_ext.add_argument('extension', help='文件扩展名 (如: py, txt, jpg)')
    
    # size 命令
    parser_size = subparsers.add_parser('size', help='按文件大小搜索')
    parser_size.add_argument('--min-size', help='最小文件大小 (如: 100M, 1G)')
    parser_size.add_argument('--max-size', help='最大文件大小 (如: 500M, 2G)')
    
    # recent 命令
    parser_recent = subparsers.add_parser('recent', help='搜索最近修改的文件')
    parser_recent.add_argument('--days', type=int, default=7, help='天数 (默认: 7)')
    
    # stats 命令
    parser_stats = subparsers.add_parser('stats', help='显示统计信息')
    parser_stats.add_argument('--extensions', action='store_true', help='显示扩展名统计')
    
    # open 命令
    parser_open = subparsers.add_parser('open', help='搜索并打开文件')
    parser_open.add_argument('query', help='搜索关键词')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 创建CLI实例并执行命令
    cli = SearchCLI()
    
    try:
        command_method = getattr(cli, f'cmd_{args.command}')
        command_method(args)
    except KeyboardInterrupt:
        print("\n🛑 搜索被用户中断")
    except Exception as e:
        print(f"❌ 执行搜索失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        cli.db_manager.close()
        cli.config_manager.cleanup()


if __name__ == "__main__":
    main()
