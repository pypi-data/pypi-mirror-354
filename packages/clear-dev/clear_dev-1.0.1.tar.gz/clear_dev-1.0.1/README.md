# 开发工具缓存清理工具集

这是一套专门用于扫描和清理开发工具缓存的Python脚本工具集，帮助开发者释放磁盘空间并优化系统性能。

## 📦 工具列表

### 1. 包扫描器 - macOS/Linux 通用扫描器
**适用系统**: macOS, Linux
**功能**: 全面扫描40+种开发工具的缓存目录

```bash
# 使用已安装的包
package-scanner

# 或从源码运行
python3 -m clear_dev.package_scanner

# 保存报告到文件
package-scanner --file cleanup_report.md

# 表格格式输出
package-scanner --output table

# JSON格式输出
package-scanner --output json --file results.json
```

**支持的工具**:
- **容器化**: Docker, Podman
- **IDE**: JetBrains, VS Code, Sublime Text
- **编程语言**: Python (pip/uv/conda), Node.js (npm/yarn/pnpm), Go, Rust, Java (Maven/Gradle), PHP (Composer), Ruby (gem)
- **macOS特有**: Xcode, Swift Package Manager, Homebrew
- **构建工具**: CMake, Bazel, Ninja
- **其他**: C/C++工具, Dart, Kotlin, Scala, Haskell

### 2. Windows 专用扫描器
**适用系统**: Windows
**功能**: 专为Windows系统优化的开发工具缓存扫描器

```bash
# 使用已安装的包
windows-cleaner

# 或从源码运行
python clear_window_dev.py

# 保存报告
windows-cleaner --file windows_cleanup.md
```

**Windows特有功能**:
- 使用Windows环境变量 (%APPDATA%, %LOCALAPPDATA%, %USERPROFILE%)
- 支持Windows特有工具: Visual Studio, NuGet, Chocolatey, Scoop, WSL
- 提供PowerShell和批处理清理命令
- 自动检测操作系统兼容性

### 3. 目录扫描器 - 精简目录扫描器
**适用系统**: 跨平台
**功能**: 快速扫描指定名称的目录，只显示路径和大小

### 4. GUI界面版本 🆕
**适用系统**: 跨平台（需要PySide6）
**功能**: 基于PySide6的现代化图形界面，提供直观的目录扫描体验

```bash
# 方式1: 使用已安装的包（推荐）
clear-dev-gui

# 方式2: 使用启动脚本
./start_gui.sh

# 方式3: 使用Python启动脚本
python run_gui.py

# 方式4: 从源码直接运行
python -m clear_dev.gui
```

**GUI特色功能**:
- **🖥️ 现代界面**: 直观的图形用户界面，操作简单
- **⚡ 异步扫描**: 后台扫描，界面不卡顿
- **📊 实时显示**: 扫描进度和结果实时更新
- **🔍 智能过滤**: 支持按大小过滤扫描结果
- **📋 表格管理**: 可排序的结果表格，支持多选操作
- **💾 一键导出**: 导出扫描结果到文本文件
- **🧹 脚本生成**: 一键生成清理脚本（Shell/批处理）
- **⚙️ 配置保存**: 自动保存用户设置和窗口状态
- **🎯 批量操作**: 支持批量选择和处理目录

**界面布局**:
- **左侧配置面板**: 目录选择、扫描参数、过滤选项
- **右侧结果区域**: 统计信息、结果表格、操作按钮
- **底部状态栏**: 扫描进度、状态信息

```bash
# 扫描 node_modules 目录（默认）
clear-dev

# 扫描单个目录
clear-dev --target-dir build

# 同时扫描多个目录
clear-dev --target-dir build dist node_modules
clear-dev --target-dir build dist target

# 扫描指定路径下的目录
clear-dev --target-dir node_modules /path/to/projects

# 保存结果到文件
clear-dev --target-dir build dist --file scan_results.txt

# 生成清理脚本（按大小排序，包含文件大小注释）
clear-dev --target-dir build dist --gen-script cleanup.sh
clear-dev --target-dir node_modules --gen-script cleanup.bat

# 排除特定目录
clear-dev --target-dir build --exclude .git .svn
```

**特色功能**:
- **简洁输出**: 只显示目录路径和大小，无多余信息
- **真正并发扫描**: 一次遍历同时查找所有目标目录类型
- **多目录扫描**: 支持同时扫描多个不同名称的目录
- **任意目录搜索**: 支持搜索任何指定名称的目录
- **高性能算法**: 优化的文件系统遍历，避免重复扫描
- **递归查找**: 深度搜索指定目录
- **类型标识**: 多目录扫描时显示每个目录的类型
- **智能清理脚本**: 自动生成按大小排序的清理脚本，包含安全确认
- **跨平台脚本**: 支持生成bash(.sh)和批处理(.bat)脚本
- **文件输出**: 支持将结果保存到文件

**支持的目录类型**:
- 任何用户指定的目录名称（如：`node_modules`, `build`, `dist`, `target`, `.git`, `.cache`等）

## 🎯 主要特性

### 高性能扫描
- **并发处理**: 使用多线程并发扫描，大幅提升速度
- **智能跳过**: 自动跳过符号链接和无权限目录
- **进度显示**: 实时显示扫描进度

### 智能分析
- **优先级排序**: 按大小和清理安全性自动排序
- **风险评估**: 每个清理建议都标明安全等级
- **重复检测**: 识别重复安装的包和工具

### 多种输出格式
- **cleanup**: 详细的清理教程报告（默认）
- **table**: 简洁的表格统计
- **json**: 结构化数据，便于程序处理

### 安全清理
- **分级建议**: 按风险等级提供清理建议
- **详细说明**: 每个命令都有详细的影响说明
- **用户控制**: 提供建议而非自动执行

## 📊 扫描示例结果

### 典型发现的大型缓存
- **Docker**: 通常 20-60 GB
- **JetBrains IDE**: 通常 10-50 GB  
- **Python uv/pip**: 通常 5-20 GB
- **Node.js npm**: 通常 1-10 GB
- **VS Code扩展**: 通常 500MB-2GB

### 清理优先级
1. **🚨 极高优先级**: Docker容器缓存（安全清理）
2. **🔥 高优先级**: IDE缓存（安全，但需重建索引）
3. **⚠️ 中等优先级**: 包管理器缓存（需重新下载）
4. **📝 低优先级**: 构建工具缓存
5. **ℹ️ 信息参考**: 可执行文件（不建议删除）

## 🛡️ 安全注意事项

1. **备份重要数据**: 清理前请确保重要项目已备份
2. **检查运行状态**: 不要清理正在使用的项目
3. **按优先级清理**: 建议按脚本推荐的优先级顺序清理
4. **测试环境**: 在测试环境中验证清理效果
5. **定期维护**: 建议每月运行一次扫描

## 🔧 系统要求

- **Python**: 3.8+ (推荐 3.10+)
- **操作系统**: Windows, macOS, Linux
- **基础依赖**: 仅使用Python标准库
- **GUI依赖**: PySide6 (可选，仅GUI功能需要)
- **权限**: 某些目录可能需要管理员权限
- **磁盘空间**: 扫描本身不占用额外空间

## 📈 性能数据

- **扫描速度**: 通常100+个路径在10-30秒内完成
- **内存使用**: 低内存占用，适合在资源受限环境运行
- **并发优化**: 支持自定义线程数（默认8个）

## 📦 安装

### 从 PyPI 安装（推荐）
```bash
# 安装基础版本（仅命令行工具）
pip install clear-dev

# 安装完整版本（包含GUI）
pip install clear-dev[gui]

# 或安装所有功能
pip install clear-dev[all]
```

### 从源码安装
```bash
# 克隆仓库
git clone https://github.com/duolabmeng6/clear_dev.git
cd clear_dev

# 使用 uv 安装（推荐）
uv sync
uv pip install -e .

# 或使用 pip 安装
pip install -e .

# 安装GUI依赖
pip install -e .[gui]
```

### 开发环境安装
```bash
# 使用 uv
uv sync --dev
uv pip install -e .[all]

# 使用 pip
pip install -e .[all]
```

## 🚀 快速开始

### 使用已安装的包
```bash
# 命令行扫描
clear-dev

# 启动GUI界面
clear-dev-gui

# 包扫描器
package-scanner

# Windows清理工具
windows-cleaner
```

### 从源码运行
```bash
# 克隆仓库
git clone https://github.com/duolabmeng6/clear_dev.git
cd clear_dev

# 使用uv运行（推荐）
uv sync
```

2. **运行扫描**:
   ```bash
   # macOS/Linux 全面扫描
   python -m clear_dev.package_scanner

   # Windows 扫描
   python clear_window_dev.py

   # 目录扫描
   python -m clear_dev.cli /path/to/projects

   # 构建目录扫描
   python -m clear_dev.cli --target-dir build /path/to/projects
   ```

3. **查看报告**: 脚本会生成详细的清理建议报告

4. **执行清理**: 根据报告中的建议手动执行清理命令

## 💡 使用技巧

- **定期扫描**: 建议每月运行一次全面扫描
- **项目清理**: 使用精简扫描器快速查看各种项目目录大小
- **构建清理**: 定期扫描 build、dist 等构建输出目录
- **依赖管理**: 扫描 node_modules、vendor 等依赖目录
- **结果保存**: 将扫描结果保存到文件便于分析

## 🔍 常用扫描示例

```bash
# 前端项目一次性扫描多个目录
clear-dev --target-dir node_modules build dist ~/projects

# Java项目扫描
clear-dev --target-dir target ~/java-projects

# 通用构建目录批量扫描
clear-dev --target-dir build dist out bin ~/all-projects

# 依赖和构建目录同时扫描
clear-dev --target-dir node_modules vendor build

# 保存多目录扫描结果
clear-dev --target-dir node_modules build dist --file scan_results.txt

# 生成清理脚本示例
clear-dev --target-dir node_modules build dist --gen-script cleanup.sh

# 大小过滤扫描
clear-dev /Users/ll --gen-script c.sh --min-size 100M --target-dir .venv node_modules
```

## 🧹 清理脚本功能

### **自动生成清理脚本**
- **按大小排序**: 从大到小排列，优先清理占用空间最多的目录
- **文件大小注释**: 每个删除命令都包含目录大小信息
- **安全确认**: 脚本包含交互式确认，防止误删
- **跨平台支持**: 自动识别并生成对应平台的脚本格式

### **脚本特性**
- **bash脚本(.sh)**: 适用于macOS/Linux，包含详细的错误处理
- **批处理脚本(.bat)**: 适用于Windows，支持中文路径
- **执行权限**: 自动为bash脚本添加执行权限
- **安全提示**: 包含备份提醒和使用说明

### **使用示例**
```bash
# 生成并运行清理脚本
clear-dev --target-dir build dist --gen-script cleanup.sh
./cleanup.sh  # 运行脚本，会有确认提示

# Windows用户
clear-dev --target-dir node_modules --gen-script cleanup.bat
# 双击运行 cleanup.bat
```

通过这套工具，您可以轻松释放几十GB的磁盘空间，保持开发环境的整洁和高效！
