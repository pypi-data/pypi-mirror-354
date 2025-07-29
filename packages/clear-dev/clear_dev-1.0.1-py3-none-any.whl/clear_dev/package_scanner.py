#!/usr/bin/env python3
"""
高性能包管理工具目录扫描器
扫描系统中各种编程语言包管理工具的缓存目录和可执行文件，统计大小
"""

import os
import sys
import json
import argparse
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import time


@dataclass
class ScanResult:
    """扫描结果数据类"""
    path: str
    size_bytes: int
    size_human: str
    file_count: int
    tool_type: str
    exists: bool
    error: Optional[str] = None


class PackageScanner:
    """包管理工具目录扫描器"""
    
    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers
        self.results: List[ScanResult] = []
        self.lock = threading.Lock()
        
    def get_package_paths(self) -> Dict[str, List[str]]:
        """获取各种包管理工具的路径"""
        home = Path.home()

        paths = {
            # Node.js 生态
            "npm": [
                str(home / ".npm"),
                str(home / ".npm-global"),
            ],
            "yarn": [
                str(home / ".yarn"),
                str(home / ".cache/yarn"),
            ],
            "pnpm": [
                str(home / "pnpm"),
                str(home / ".pnpm-store"),
                str(home / ".local/share/pnpm"),
            ],
            "node_modules": [
                "./node_modules",
                str(home / "node_modules"),
            ],

            # Python 生态
            "pip": [
                str(home / ".cache/pip"),
                str(home / "Library/Caches/pip"),  # macOS
            ],
            "uv": [
                str(home / ".cache/uv"),
                str(home / "Library/Caches/uv"),  # macOS
            ],
            "conda": [
                str(home / "miniconda3"),
                str(home / "anaconda3"),
                str(home / ".conda"),
            ],
            "python_site_packages": [
                "/usr/local/lib/python*/site-packages",
                str(home / ".local/lib/python*/site-packages"),
            ],

            # Go 生态
            "go": [
                str(home / "go/pkg"),
                os.environ.get("GOPATH", str(home / "go")) + "/pkg",
                os.environ.get("GOCACHE", str(home / "Library/Caches/go-build")),
            ],

            # Java 生态
            "maven": [
                str(home / ".m2/repository"),
            ],
            "gradle": [
                str(home / ".gradle/caches"),
                str(home / ".gradle/kotlin"),  # Kotlin缓存
            ],

            # PHP 生态
            "composer": [
                str(home / ".composer/cache"),
                str(home / ".cache/composer"),
                "./vendor",
            ],

            # Ruby 生态
            "gem": [
                str(home / ".gem"),
                "./vendor/bundle",
            ],

            # Rust 生态
            "rust_cargo": [
                str(home / ".cargo"),
                str(home / "Library/Caches/cargo"),  # macOS
                str(home / ".rustup"),
            ],

            # C/C++ 生态
            "cpp_tools": [
                str(home / "Library/Caches/clang"),  # macOS
                str(home / "Library/Caches/cmake"),  # macOS
                str(home / ".cache/clang"),
                str(home / ".cache/cmake"),
                str(home / ".conan"),
                str(home / "vcpkg"),
            ],

            # macOS 开发工具
            "xcode": [
                str(home / "Library/Developer/Xcode"),
                str(home / "Library/Caches/com.apple.dt.Xcode"),
                str(home / "Library/Developer/CoreSimulator"),
                str(home / "Library/Developer/XCTestDevices"),
            ],

            # Swift 生态
            "swift": [
                str(home / "Library/Caches/org.swift.swiftpm"),
                str(home / ".swiftpm"),
            ],

            # 移动开发
            "flutter": [
                str(home / "Library/Caches/flutter_engine"),  # macOS
                str(home / ".pub-cache"),
                str(home / "flutter"),
            ],

            "android": [
                str(home / "Library/Android"),  # macOS
                str(home / ".android"),
                str(home / "Android"),
            ],

            "react_native": [
                str(home / "Library/Caches/com.facebook.react.packager"),  # macOS
                str(home / ".cache/react-native"),
            ],

            # 容器化工具
            "docker": [
                str(home / "Library/Caches/Docker Desktop"),  # macOS
                str(home / "Library/Containers/com.docker.docker"),  # macOS
                str(home / ".docker"),
                str(home / ".local/share/docker"),
            ],

            "podman": [
                str(home / ".local/share/containers"),
                str(home / ".config/containers"),
            ],

            # 包管理器
            "homebrew": [
                str(home / "Library/Caches/Homebrew"),  # macOS
                "/opt/homebrew/var/cache",  # macOS Apple Silicon
                "/usr/local/var/cache",  # macOS Intel
            ],

            "macports": [
                "/opt/local/var/macports",  # macOS
            ],

            # 其他编程语言
            "dart": [
                str(home / ".pub-cache"),
                str(home / "Library/Caches/dart"),  # macOS
            ],

            "kotlin": [
                str(home / ".konan"),
                str(home / ".gradle/kotlin"),
            ],

            "scala": [
                str(home / ".ivy2"),
                str(home / ".sbt"),
                str(home / ".cache/coursier"),
            ],

            "haskell": [
                str(home / ".stack"),
                str(home / ".cabal"),
                str(home / ".ghc"),
            ],

            # IDE 和编辑器缓存
            "vscode": [
                str(home / "Library/Caches/com.microsoft.VSCode"),  # macOS
                str(home / ".cache/vscode"),
                str(home / ".vscode/extensions"),
            ],

            "jetbrains": [
                str(home / "Library/Caches/JetBrains"),  # macOS
                str(home / ".cache/JetBrains"),
                str(home / "Library/Application Support/JetBrains"),  # macOS
            ],

            "sublime": [
                str(home / "Library/Caches/com.sublimetext.3"),  # macOS
                str(home / "Library/Caches/com.sublimetext.4"),  # macOS
            ],

            # 构建工具
            "cmake": [
                str(home / "Library/Caches/cmake"),  # macOS
                str(home / ".cache/cmake"),
            ],

            "bazel": [
                str(home / ".cache/bazel"),
                str(home / "Library/Caches/bazel"),  # macOS
            ],

            "ninja": [
                str(home / ".ninja_log"),
            ],

            # 其他工具
            "conan": [
                str(home / ".conan"),
                str(home / ".conan2"),
            ],

            "vcpkg": [
                str(home / "vcpkg"),
                "./vcpkg",
            ],

            # 可执行文件目录
            "executables": [
                "/usr/local/bin",
                str(home / ".local/bin"),
                str(home / "bin"),
                "/opt/homebrew/bin",  # macOS Homebrew
                "/opt/local/bin",  # macOS MacPorts
            ],
        }

        # 添加环境变量中的路径
        if "PATH" in os.environ:
            for path in os.environ["PATH"].split(os.pathsep):
                if any(keyword in path.lower() for keyword in ["node", "python", "go", "java", "php", "ruby"]):
                    paths.setdefault("executables", []).append(path)
        
        return paths
    
    def calculate_directory_size(self, path: str) -> Tuple[int, int]:
        """计算目录大小和文件数量"""
        total_size = 0
        file_count = 0
        
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                return 0, 0
                
            if path_obj.is_file():
                return path_obj.stat().st_size, 1
                
            # 使用 os.scandir 提高性能
            for entry in os.scandir(path):
                try:
                    if entry.is_file(follow_symlinks=False):
                        total_size += entry.stat().st_size
                        file_count += 1
                    elif entry.is_dir(follow_symlinks=False):
                        dir_size, dir_files = self.calculate_directory_size(entry.path)
                        total_size += dir_size
                        file_count += dir_files
                except (OSError, PermissionError):
                    continue
                    
        except (OSError, PermissionError) as e:
            return 0, 0
            
        return total_size, file_count
    
    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    def scan_path(self, path: str, tool_type: str) -> ScanResult:
        """扫描单个路径"""
        try:
            path_obj = Path(path)
            exists = path_obj.exists()
            
            if not exists:
                return ScanResult(
                    path=path,
                    size_bytes=0,
                    size_human="0 B",
                    file_count=0,
                    tool_type=tool_type,
                    exists=False
                )
            
            size_bytes, file_count = self.calculate_directory_size(path)
            size_human = self.format_size(size_bytes)
            
            return ScanResult(
                path=path,
                size_bytes=size_bytes,
                size_human=size_human,
                file_count=file_count,
                tool_type=tool_type,
                exists=True
            )
            
        except Exception as e:
            return ScanResult(
                path=path,
                size_bytes=0,
                size_human="0 B",
                file_count=0,
                tool_type=tool_type,
                exists=False,
                error=str(e)
            )
    
    def scan_all(self, show_progress: bool = True) -> List[ScanResult]:
        """扫描所有路径"""
        package_paths = self.get_package_paths()
        all_tasks = []
        
        # 准备所有扫描任务
        for tool_type, paths in package_paths.items():
            for path in paths:
                all_tasks.append((path, tool_type))
        
        print(f"开始扫描 {len(all_tasks)} 个路径...")
        
        # 并发执行扫描
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {
                executor.submit(self.scan_path, path, tool_type): (path, tool_type)
                for path, tool_type in all_tasks
            }
            
            completed = 0
            for future in as_completed(future_to_task):
                result = future.result()
                
                with self.lock:
                    self.results.append(result)
                    completed += 1
                    
                if show_progress:
                    print(f"进度: {completed}/{len(all_tasks)} ({completed/len(all_tasks)*100:.1f}%)", end="\r")
        
        if show_progress:
            print()  # 换行
            
        return self.results
    
    def get_summary(self) -> Dict:
        """获取扫描结果摘要"""
        existing_results = [r for r in self.results if r.exists and r.size_bytes > 0]

        total_size = sum(r.size_bytes for r in existing_results)
        total_files = sum(r.file_count for r in existing_results)

        # 按工具类型分组
        by_tool = {}
        for result in existing_results:
            if result.tool_type not in by_tool:
                by_tool[result.tool_type] = {
                    "size_bytes": 0,
                    "file_count": 0,
                    "paths": []
                }
            by_tool[result.tool_type]["size_bytes"] += result.size_bytes
            by_tool[result.tool_type]["file_count"] += result.file_count
            by_tool[result.tool_type]["paths"].append({
                "path": result.path,
                "size_bytes": result.size_bytes,
                "size_human": result.size_human,
                "file_count": result.file_count
            })

        # 添加人类可读的大小
        for tool_data in by_tool.values():
            tool_data["size_human"] = self.format_size(tool_data["size_bytes"])

        return {
            "total_size_bytes": total_size,
            "total_size_human": self.format_size(total_size),
            "total_files": total_files,
            "scanned_paths": len(self.results),
            "existing_paths": len(existing_results),
            "by_tool": by_tool
        }

    def generate_cleanup_report(self) -> str:
        """生成清理教程报告"""
        summary = self.get_summary()
        existing_results = [r for r in self.results if r.exists and r.size_bytes > 0]

        # 清理规则定义
        cleanup_rules = {
            "docker": {
                "priority": "🚨 极高优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "docker system prune -a --volumes  # 清理所有未使用的镜像、容器、网络和卷",
                    "docker image prune -a  # 仅清理未使用的镜像",
                    "docker container prune  # 仅清理停止的容器"
                ],
                "description": "Docker容器和镜像缓存",
                "impact": "删除未使用的Docker资源，不影响正在运行的容器",
                "rebuild_time": "重新拉取镜像需要时间，取决于网络速度"
            },
            "jetbrains": {
                "priority": "🔥 高优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "# 手动清理JetBrains缓存目录",
                    "find ~/Library/Caches/JetBrains -name 'caches' -type d -exec rm -rf {} +",
                    "find ~/Library/Caches/JetBrains -name 'tmp' -type d -exec rm -rf {} +",
                    "# 或者直接删除整个缓存目录",
                    "rm -rf ~/Library/Caches/JetBrains"
                ],
                "description": "JetBrains IDE缓存和临时文件",
                "impact": "IDE首次启动会重建索引，启动速度变慢",
                "rebuild_time": "重建索引需要几分钟到几十分钟"
            },
            "uv": {
                "priority": "⚠️ 中等优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "uv cache clean  # 清理所有uv缓存",
                    "uv cache clean --package <package_name>  # 清理特定包缓存"
                ],
                "description": "Python uv包管理器缓存",
                "impact": "下次安装包时需要重新下载",
                "rebuild_time": "重新下载包的时间取决于网络速度"
            },
            "pip": {
                "priority": "⚠️ 中等优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "pip cache purge  # 清理所有pip缓存",
                    "pip cache remove <package_name>  # 清理特定包缓存"
                ],
                "description": "Python pip包缓存",
                "impact": "下次安装包时需要重新下载",
                "rebuild_time": "重新下载包的时间取决于网络速度"
            },
            "npm": {
                "priority": "⚠️ 中等优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "npm cache clean --force  # 强制清理npm缓存",
                    "npm cache verify  # 验证缓存完整性"
                ],
                "description": "Node.js npm包缓存",
                "impact": "下次安装包时需要重新下载",
                "rebuild_time": "重新下载包的时间取决于网络速度"
            },
            "rust_cargo": {
                "priority": "⚠️ 中等优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "cargo cache --autoclean  # 需要先安装cargo-cache",
                    "cargo install cargo-cache  # 安装cargo-cache工具",
                    "rm -rf ~/.cargo/registry/cache  # 手动清理注册表缓存",
                    "rm -rf ~/.cargo/git/checkouts  # 清理git检出缓存"
                ],
                "description": "Rust Cargo包缓存和工具链",
                "impact": "重新编译项目时需要重新下载依赖",
                "rebuild_time": "重新编译和下载依赖需要较长时间"
            },
            "vscode": {
                "priority": "📝 低优先级",
                "safety": "⚠️ 谨慎",
                "risk_level": "中风险",
                "commands": [
                    "rm -rf ~/Library/Caches/com.microsoft.VSCode  # 清理VS Code缓存",
                    "# 扩展目录建议手动检查后清理",
                    "ls ~/.vscode/extensions  # 查看已安装扩展"
                ],
                "description": "VS Code缓存和扩展",
                "impact": "可能需要重新配置扩展和设置",
                "rebuild_time": "重新安装扩展需要几分钟"
            },
            "go": {
                "priority": "📝 低优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "go clean -cache  # 清理构建缓存",
                    "go clean -modcache  # 清理模块缓存",
                    "go clean -testcache  # 清理测试缓存"
                ],
                "description": "Go语言构建和模块缓存",
                "impact": "重新编译项目时需要重新下载模块",
                "rebuild_time": "重新编译和下载模块需要一些时间"
            },
            "homebrew": {
                "priority": "📝 低优先级",
                "safety": "✅ 安全",
                "risk_level": "低风险",
                "commands": [
                    "brew cleanup  # 清理旧版本和缓存",
                    "brew autoremove  # 移除不需要的依赖",
                    "brew cleanup --prune=all  # 清理所有缓存"
                ],
                "description": "Homebrew包管理器缓存",
                "impact": "重新安装包时需要重新下载",
                "rebuild_time": "重新下载包的时间取决于网络速度"
            },
            "executables": {
                "priority": "ℹ️ 信息参考",
                "safety": "⚠️ 谨慎",
                "risk_level": "高风险",
                "commands": [
                    "# 可执行文件目录 - 仅供参考，请勿随意删除",
                    "# 这些是系统和开发工具的可执行文件",
                    "# 删除可能导致系统或开发环境无法正常工作"
                ],
                "description": "系统和开发工具可执行文件",
                "impact": "删除可能导致系统或开发环境无法正常工作",
                "rebuild_time": "需要重新安装相关工具和环境"
            }
        }

        # 生成报告
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("🧹 开发工具缓存清理教程报告")
        report_lines.append("=" * 80)
        report_lines.append(f"📊 扫描结果: {summary['total_size_human']} ({summary['total_files']:,} 文件)")
        report_lines.append(f"📁 扫描路径: {summary['scanned_paths']} 个")
        report_lines.append(f"✅ 发现缓存: {summary['existing_paths']} 个")
        report_lines.append("")

        # 按大小排序工具
        sorted_tools = sorted(summary["by_tool"].items(),
                            key=lambda x: x[1]["size_bytes"], reverse=True)

        # 计算可清理的总空间
        cleanable_size = 0
        high_priority_size = 0

        for tool_type, tool_data in sorted_tools:
            if tool_type in cleanup_rules:
                cleanable_size += tool_data["size_bytes"]
                if "极高优先级" in cleanup_rules[tool_type]["priority"] or "高优先级" in cleanup_rules[tool_type]["priority"]:
                    high_priority_size += tool_data["size_bytes"]

        report_lines.append(f"💾 可清理空间: {self.format_size(cleanable_size)}")
        report_lines.append(f"🚨 高优先级可清理: {self.format_size(high_priority_size)}")
        report_lines.append("")

        # 生成清理建议
        report_lines.append("📋 清理建议 (按优先级排序)")
        report_lines.append("=" * 50)

        for tool_type, tool_data in sorted_tools:
            if tool_data["size_bytes"] > 0:
                # 如果有清理规则，显示清理建议
                if tool_type in cleanup_rules:
                    rule = cleanup_rules[tool_type]
                    report_lines.append("")
                    report_lines.append(f"{rule['priority']} {rule['description']}")
                    report_lines.append(f"📦 大小: {tool_data['size_human']} ({tool_data['file_count']:,} 文件)")
                    report_lines.append(f"🛡️  安全性: {rule['safety']} ({rule['risk_level']})")
                    report_lines.append(f"📝 影响: {rule['impact']}")
                    report_lines.append(f"⏱️  重建时间: {rule['rebuild_time']}")
                    report_lines.append("🔧 清理命令:")
                    for cmd in rule['commands']:
                        report_lines.append(f"   {cmd}")
                else:
                    # 没有清理规则的工具，仅显示信息
                    report_lines.append("")
                    report_lines.append(f"📊 信息参考 {tool_type.upper()}")
                    report_lines.append(f"📦 大小: {tool_data['size_human']} ({tool_data['file_count']:,} 文件)")
                    report_lines.append("ℹ️  说明: 此类文件仅供参考，建议谨慎处理")

                # 显示具体路径和文件大小清单
                if len(tool_data['paths']) > 0:
                    report_lines.append("📁 详细路径清单:")
                    for path_info in sorted(tool_data['paths'], key=lambda x: x['size_bytes'], reverse=True):
                        if path_info['size_bytes'] > 0:
                            report_lines.append(f"   📂 {path_info['path']}")
                            report_lines.append(f"      💾 大小: {path_info['size_human']}")
                            report_lines.append(f"      📄 文件数: {path_info['file_count']:,}")

                report_lines.append("-" * 50)

        # 添加注意事项
        report_lines.append("")
        report_lines.append("⚠️  重要注意事项")
        report_lines.append("=" * 30)
        report_lines.append("1. 🔒 清理前请确保重要数据已备份")
        report_lines.append("2. 🚫 不要清理正在使用的项目目录")
        report_lines.append("3. 📋 建议按优先级顺序逐个清理")
        report_lines.append("4. 🔍 清理后可重新运行扫描查看效果")
        report_lines.append("5. 💡 定期清理可保持系统性能")
        report_lines.append("")
        report_lines.append("🔄 重新扫描命令:")
        report_lines.append("   python3 package_scanner.py")
        report_lines.append("")

        return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(description="扫描系统中包管理工具的目录大小")
    parser.add_argument("--workers", type=int, default=8, help="并发线程数")
    parser.add_argument("--output", choices=["table", "json", "cleanup"], default="cleanup", help="输出格式")
    parser.add_argument("--file", help="输出到文件", default="清理报告.md")

    args = parser.parse_args()

    scanner = PackageScanner(max_workers=args.workers)

    start_time = time.time()
    results = scanner.scan_all()
    end_time = time.time()

    summary = scanner.get_summary()

    if args.output == "cleanup":
        # 生成清理教程报告
        output_text = scanner.generate_cleanup_report()
    elif args.output == "json":
        output_data = {
            "summary": summary,
            "results": [asdict(r) for r in results if r.exists and r.size_bytes > 0],
            "scan_time_seconds": end_time - start_time
        }
        output_text = json.dumps(output_data, indent=2, ensure_ascii=False)
    else:
        # 表格输出
        output_lines = []
        output_lines.append("=" * 80)
        output_lines.append("包管理工具目录大小统计")
        output_lines.append("=" * 80)
        output_lines.append(f"总大小: {summary['total_size_human']}")
        output_lines.append(f"总文件数: {summary['total_files']:,}")
        output_lines.append(f"扫描时间: {end_time - start_time:.2f} 秒")
        output_lines.append("")

        for tool_type, tool_data in sorted(summary["by_tool"].items(),
                                         key=lambda x: x[1]["size_bytes"], reverse=True):
            output_lines.append(f"{tool_type.upper()}: {tool_data['size_human']} ({tool_data['file_count']:,} 文件)")
            for path_info in sorted(tool_data["paths"], key=lambda x: x["size_bytes"], reverse=True):
                if path_info["size_bytes"] > 0:
                    output_lines.append(f"  {path_info['path']}: {path_info['size_human']} ({path_info['file_count']:,} 文件)")
            output_lines.append("")

        output_text = "\n".join(output_lines)

    if args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"结果已保存到: {args.file}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
