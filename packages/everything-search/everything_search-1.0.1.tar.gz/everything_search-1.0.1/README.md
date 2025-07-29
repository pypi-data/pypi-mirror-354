# Everything Search for macOS

🚀 高性能文件搜索工具 - 类似于Windows Everything的macOS解决方案

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)](https://www.apple.com/macos/)
![alt text](image.png)
## ✨ 特性

- 🔍 **极速搜索** - 毫秒级文件搜索响应
- 📊 **智能索引** - 增量索引和实时文件系统监控
- 🎯 **多种搜索模式** - 支持模糊搜索、正则表达式、文件类型过滤
- 🖥️ **双界面支持** - 现代化GUI界面和强大的命令行工具
- ⚡ **高性能** - 多线程并发处理，优化的数据库查询
- 🔄 **实时同步** - 文件系统变更实时更新索引

## 📦 安装

### 方式1：使用 uv tool（推荐）

```bash
# 安装
uv tool install everything-search

# 启动GUI
uv tool run everything-gui

# 使用CLI
uv tool run everything-index start
uv tool run everything-search "keyword"
```

### 方式2：使用 pip

```bash
# 安装
pip install everything-search

# 启动GUI
everything-gui

# 使用CLI
everything-index start
everything-search "keyword"
```

### 方式3：从源码安装

```bash
# 克隆仓库
git clone https://github.com/duolabmeng6/everything-for-mac.git
cd everything-for-mac

# 使用uv安装依赖
uv sync

# 运行
uv run everything-gui
```

## 🚀 快速开始

### 1. 初始化索引

首次使用需要建立文件索引：

```bash
# 自动启动（推荐）- 自动初始化索引并启动实时监控
everything-index start

# 或者手动初始化
everything-index init
```

### 2. 启动GUI界面

```bash
everything-gui
```

### 3. 命令行搜索

```bash
# 基本搜索
everything-search "document"

# 正则表达式搜索
everything-search "*.py" --regex

# 按文件类型搜索
everything-search extension py

# 按文件大小搜索
everything-search size --min-size 100M

# 搜索最近修改的文件
everything-search recent --days 7
```

## 📖 详细使用

### GUI界面

启动GUI后，您可以：

1. **搜索页面**：
   - 在搜索框中输入关键词
   - 支持实时搜索结果预览
   - 可按文件名、大小、修改时间排序
   - 右键菜单支持打开文件/文件夹

2. **设置页面**：
   - 管理索引目录
   - 配置排除规则
   - 查看索引状态
   - 启动/停止实时监控

### 命令行工具

#### 索引管理 (everything-index)

```bash
# 查看帮助
everything-index --help

# 初始化索引
everything-index init

# 自动启动（初始化+增量更新+实时监控）
everything-index start

# 重建索引
everything-index rebuild

# 启动实时监控
everything-index watch

# 查看索引状态
everything-index status

# 配置管理
everything-index config show
everything-index config add-dir ~/Documents
```

#### 文件搜索 (everything-search)

```bash
# 查看帮助
everything-search --help

# 基本搜索
everything-search search "keyword"

# 高级搜索选项
everything-search search "pattern" --regex --limit 100

# 按扩展名搜索
everything-search extension py

# 按大小搜索
everything-search size --min-size 1M --max-size 100M

# 最近文件
everything-search recent --days 30

# 搜索并打开
everything-search open "config"

# 显示统计信息
everything-search stats --extensions
```

## ⚙️ 配置

配置文件位置：`~/.everything-search/config.json`

主要配置项：

```json
{
  "index": {
    "directories": ["/Users/username/Documents", "/Users/username/Desktop"],
    "exclude_dirs": [".git", "node_modules", ".venv"],
    "exclude_extensions": [".tmp", ".log"],
    "max_file_size_mb": 1000,
    "follow_symlinks": false,
    "index_hidden_files": false
  },
  "search": {
    "case_sensitive": false,
    "fuzzy_search": true,
    "max_results": 1000
  }
}
```

## 🛠️ 开发

### 环境要求

- Python 3.8+
- macOS 10.14+
- uv (推荐) 或 pip

### 开发安装

```bash
# 克隆仓库
git clone https://github.com/duolabmeng6/everything-for-mac.git
cd everything-for-mac

# 安装开发依赖
uv sync --extra dev

# 运行测试
uv run pytest

# 代码格式化
uv run black .

# 类型检查
uv run mypy .
```

### 项目结构

```
everything-search/
├── everything_search/          # 主包
│   ├── core/                  # 核心模块
│   │   ├── config_manager.py  # 配置管理
│   │   ├── database.py        # 数据库操作
│   │   ├── file_indexer.py    # 文件索引
│   │   ├── search_engine.py   # 搜索引擎
│   │   └── file_watcher.py    # 文件监控
│   ├── cli/                   # 命令行工具
│   │   ├── index_cli.py       # 索引管理CLI
│   │   └── search_cli.py      # 搜索CLI
│   ├── gui/                   # GUI界面
│   │   ├── main_window.py     # 主窗口
│   │   ├── search_tab.py      # 搜索页面
│   │   └── settings_tab.py    # 设置页面
│   └── gui_main.py           # GUI启动脚本
├── pyproject.toml            # 项目配置
└── README.md                 # 项目说明
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- 灵感来源于Windows平台的Everything搜索工具
- 使用了优秀的开源库：PySide6、watchdog等

## 📞 联系

- 作者：duolabmeng6
- 邮箱：1715109585@qq.com
- 项目链接：https://github.com/duolabmeng6/everything-for-mac

---

⭐ 如果这个项目对您有帮助，请给个Star支持一下！
# 打赏
![alt text](swskm.jpg)