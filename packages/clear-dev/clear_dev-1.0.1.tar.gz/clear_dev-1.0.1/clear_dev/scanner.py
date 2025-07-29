#!/usr/bin/env python3
"""
通用目录扫描器
扫描指定目录下所有指定名称的文件夹，统计大小
"""

import os
import argparse
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Tuple, Set
import time


@dataclass
class DirectoryScanResult:
    """目录扫描结果数据类"""
    path: str
    size_bytes: int
    size_human: str
    exists: bool


class DirectoryScanner:
    """通用目录扫描器"""

    def __init__(self, max_workers: int = 8):
        self.max_workers = max_workers
        self.results: List[DirectoryScanResult] = []
        self.lock = threading.Lock()

    def format_size(self, size_bytes: int) -> str:
        """格式化文件大小"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"

    @staticmethod
    def parse_size_string(size_str: str) -> int:
        """解析大小字符串，如 '100M', '1.5G' 等，返回字节数"""
        if not size_str:
            return 0

        size_str = size_str.strip().upper()

        # 单位映射
        units = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4,
            'K': 1024,  # 简写
            'M': 1024 ** 2,  # 简写
            'G': 1024 ** 3,  # 简写
            'T': 1024 ** 4   # 简写
        }

        # 提取数字和单位
        import re
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGT]?B?)$', size_str)
        if not match:
            raise ValueError(f"无效的大小格式: {size_str}. 支持格式如: 100M, 1.5G, 500MB")

        number = float(match.group(1))
        unit = match.group(2) or 'B'

        if unit not in units:
            raise ValueError(f"不支持的单位: {unit}. 支持的单位: {', '.join(units.keys())}")

        return int(number * units[unit])

    def filter_results_by_size(self, results: List[DirectoryScanResult], min_size_bytes: int) -> List[DirectoryScanResult]:
        """根据最小大小过滤结果"""
        if min_size_bytes <= 0:
            return results

        return [r for r in results if r.exists and r.size_bytes >= min_size_bytes]

    def find_multiple_target_directories(self, root_path: str, target_dir_names: List[str], exclude_dirs: Set[str] = None) -> List[Tuple[str, str, int, str]]:
        """一次遍历查找所有指定名称的目录"""
        if exclude_dirs is None:
            exclude_dirs = {'.git', '.svn', '.hg'}

        # 从排除列表中移除要搜索的目录
        target_set = set(target_dir_names)
        exclude_dirs = exclude_dirs - target_set

        target_dirs = []

        try:
            root_path_obj = Path(root_path)
            if not root_path_obj.exists():
                return target_dirs

            for root, dirs, _ in os.walk(root_path):
                # 移除排除的目录，避免递归进入
                dirs[:] = [d for d in dirs if d not in exclude_dirs]

                # 检查当前目录下是否有任何目标目录
                found_targets = []
                for target_name in target_dir_names:
                    target_path = os.path.join(root, target_name)
                    if os.path.exists(target_path) and os.path.isdir(target_path):
                        # 计算深度（相对于根路径）
                        depth = len(Path(root).relative_to(root_path_obj).parts)
                        target_dirs.append((target_path, root, depth, target_name))
                        found_targets.append(target_name)

                # 移除已找到的目标目录，避免递归进入
                for target_name in found_targets:
                    if target_name in dirs:
                        dirs.remove(target_name)

        except (OSError, PermissionError) as e:
            print(f"⚠️  无法访问目录 {root_path}: {e}")

        return target_dirs
    
    def calculate_directory_size(self, path: str) -> int:
        """计算目录大小"""
        total_size = 0

        try:
            for root, _, files in os.walk(path):
                try:
                    for file in files:
                        try:
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path)
                            total_size += file_size
                        except (OSError, PermissionError, FileNotFoundError):
                            continue
                except (OSError, PermissionError):
                    continue

        except (OSError, PermissionError):
            return 0

        return total_size
    
    def scan_directory(self, path: str, target_type: str = None) -> DirectoryScanResult:
        """扫描单个目录"""
        try:
            path_obj = Path(path)
            exists = path_obj.exists()

            if not exists:
                result = DirectoryScanResult(
                    path=path,
                    size_bytes=0,
                    size_human="0 B",
                    exists=False
                )
                if target_type:
                    result.target_type = target_type
                return result

            size_bytes = self.calculate_directory_size(path)
            size_human = self.format_size(size_bytes)

            result = DirectoryScanResult(
                path=path,
                size_bytes=size_bytes,
                size_human=size_human,
                exists=True
            )
            if target_type:
                result.target_type = target_type
            return result

        except Exception:
            result = DirectoryScanResult(
                path=path,
                size_bytes=0,
                size_human="0 B",
                exists=False
            )
            if target_type:
                result.target_type = target_type
            return result
    
    def scan_all_concurrent(self, root_path: str, target_dir_names: List[str], exclude_dirs: Set[str] = None, show_progress: bool = True) -> List[DirectoryScanResult]:
        """并发扫描指定目录下的所有指定名称的目录"""
        target_names_str = ", ".join(target_dir_names)
        print(f"🔍 正在查找 {root_path} 下的所有目标目录: {target_names_str}")

        # 一次遍历查找所有目标目录
        target_dirs = self.find_multiple_target_directories(root_path, target_dir_names, exclude_dirs)

        if not target_dirs:
            print(f"❌ 未找到任何目标目录: {target_names_str}")
            return []

        # 按目录类型分组统计
        type_counts = {}
        for _, _, _, target_type in target_dirs:
            type_counts[target_type] = type_counts.get(target_type, 0) + 1

        print(f"📁 找到目录: {', '.join([f'{t}({c})' for t, c in type_counts.items()])} 共{len(target_dirs)}个")
        print("📊 开始并发计算大小...")

        # 并发扫描所有目标目录
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_task = {
                executor.submit(self.scan_directory, target_path, target_type): (target_path, target_type)
                for target_path, _, _, target_type in target_dirs
            }

            completed = 0
            for future in as_completed(future_to_task):
                result = future.result()

                with self.lock:
                    self.results.append(result)
                    completed += 1

                if show_progress:
                    print(f"进度: {completed}/{len(target_dirs)} ({completed/len(target_dirs)*100:.1f}%)", end="\r")

        if show_progress:
            print()  # 换行

        return self.results
    
    def get_summary(self):
        """获取扫描结果摘要"""
        existing_results = [r for r in self.results if r.exists and r.size_bytes > 0]
        total_size = sum(r.size_bytes for r in existing_results)

        return {
            "total_size_bytes": total_size,
            "total_size_human": self.format_size(total_size),
            "total_directories": len(existing_results)
        }

    def generate_cleanup_script(self, results: List[DirectoryScanResult], script_path: str, target_dirs: List[str], script_mode: str = "auto") -> str:
        """生成清理脚本"""
        import platform

        # 过滤有效结果并按大小排序（从大到小）
        valid_results = [r for r in results if r.exists and r.size_bytes > 0]
        sorted_results = sorted(valid_results, key=lambda x: x.size_bytes, reverse=True)

        # 判断脚本类型
        is_windows = script_path.lower().endswith(('.bat', '.cmd')) or platform.system() == 'Windows'

        script_lines = []

        # 手动选择模式：生成简洁的列表格式
        if script_mode == "manual":
            return self._generate_manual_script(sorted_results, script_path, target_dirs, is_windows)

        if is_windows:
            # Windows批处理脚本
            script_lines.append("@echo off")
            script_lines.append("REM 自动生成的目录清理脚本")
            script_lines.append(f"REM 扫描目标: {', '.join(target_dirs)}")
            script_lines.append(f"REM 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            script_lines.append(f"REM 总大小: {self.format_size(sum(r.size_bytes for r in sorted_results))}")
            script_lines.append(f"REM 目录数量: {len(sorted_results)}")
            script_lines.append("")
            script_lines.append("echo 警告: 此脚本将删除以下目录，请确认后继续！")
            script_lines.append("echo.")

            for i, result in enumerate(sorted_results, 1):
                target_type = getattr(result, 'target_type', '未知')
                script_lines.append(f"echo {i:2d}. [{target_type}] {result.path} - {result.size_human}")

            script_lines.append("")
            script_lines.append("set /p confirm=确认删除以上目录？(y/N): ")
            script_lines.append("if /i not \"%confirm%\"==\"y\" goto :end")
            script_lines.append("")
            script_lines.append("echo 开始清理...")
            script_lines.append("")

            for i, result in enumerate(sorted_results, 1):
                target_type = getattr(result, 'target_type', '未知')
                # 转换路径为Windows格式
                win_path = result.path.replace('/', '\\')
                script_lines.append(f"REM {i:2d}. [{target_type}] {result.size_human}")
                script_lines.append(f"if exist \"{win_path}\" (")
                script_lines.append(f"    echo 删除: {win_path}")
                script_lines.append(f"    rmdir /s /q \"{win_path}\"")
                script_lines.append(f"    if errorlevel 1 echo 错误: 无法删除 {win_path}")
                script_lines.append(")")
                script_lines.append("")

            script_lines.append("echo 清理完成！")
            script_lines.append(":end")
            script_lines.append("pause")

        else:
            # Unix/Linux/macOS bash脚本
            script_lines.append("#!/bin/bash")
            script_lines.append("# 自动生成的目录清理脚本")
            script_lines.append(f"# 扫描目标: {', '.join(target_dirs)}")
            script_lines.append(f"# 生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            script_lines.append(f"# 总大小: {self.format_size(sum(r.size_bytes for r in sorted_results))}")
            script_lines.append(f"# 目录数量: {len(sorted_results)}")
            script_lines.append("")
            script_lines.append("echo '警告: 此脚本将删除以下目录，请确认后继续！'")
            script_lines.append("echo")

            for i, result in enumerate(sorted_results, 1):
                target_type = getattr(result, 'target_type', '未知')
                script_lines.append(f"echo '{i:2d}. [{target_type}] {result.path} - {result.size_human}'")

            script_lines.append("")
            script_lines.append("read -p '确认删除以上目录？(y/N): ' confirm")
            script_lines.append("if [[ ! \"$confirm\" =~ ^[Yy]$ ]]; then")
            script_lines.append("    echo '已取消清理'")
            script_lines.append("    exit 0")
            script_lines.append("fi")
            script_lines.append("")
            script_lines.append("echo '开始清理...'")
            script_lines.append("")

            for i, result in enumerate(sorted_results, 1):
                target_type = getattr(result, 'target_type', '未知')
                script_lines.append(f"# {i:2d}. [{target_type}] {result.size_human}")
                script_lines.append(f"if [ -d \"{result.path}\" ]; then")
                script_lines.append(f"    echo '删除: {result.path}'")
                script_lines.append(f"    rm -rf \"{result.path}\"")
                script_lines.append(f"    if [ $? -eq 0 ]; then")
                script_lines.append(f"        echo '✅ 成功删除: {result.path}'")
                script_lines.append(f"    else")
                script_lines.append(f"        echo '❌ 删除失败: {result.path}'")
                script_lines.append(f"    fi")
                script_lines.append("else")
                script_lines.append(f"    echo '⚠️  目录不存在: {result.path}'")
                script_lines.append("fi")
                script_lines.append("")

            script_lines.append("echo '清理完成！'")
            script_lines.append("")
            script_lines.append("# 重新扫描查看效果")
            script_lines.append(f"# python3 scan_node_modules.py --target-dir {' '.join(target_dirs)}")

        return "\n".join(script_lines)

def main():
    parser = argparse.ArgumentParser(description="扫描目录下所有指定名称的文件夹并统计大小")
    parser.add_argument("path", nargs="?", default=".", help="要扫描的根目录路径 (默认: 当前目录)")
    parser.add_argument("--target-dir", nargs="*", default=["node_modules"], help="要搜索的目录名称，支持多个 (默认: node_modules)")
    parser.add_argument("--workers", type=int, default=8, help="并发线程数")
    parser.add_argument("--file", help="输出到文件")
    parser.add_argument("--exclude", nargs="*", default=[], help="排除的目录名称")
    parser.add_argument("--gen-script", help="生成清理脚本文件名 (如: cleanup.sh 或 cleanup.bat)")
    parser.add_argument("--min-size", help="最小显示大小，过滤小于此大小的目录 (如: 100M, 1G, 500MB)")
    parser.add_argument("--script-mode", choices=["auto", "manual"], default="auto", help="脚本模式: auto=自动删除所有目录, manual=生成列表供手动选择 (默认: auto)")

    args = parser.parse_args()

    # 解析最小大小参数
    min_size_bytes = 0
    if args.min_size:
        try:
            min_size_bytes = DirectoryScanner.parse_size_string(args.min_size)
        except ValueError as e:
            print(f"❌ 参数错误: {e}")
            return

    # 准备排除目录集合
    exclude_dirs = set(args.exclude) if args.exclude else set()
    exclude_dirs.update({'.git', '.svn', '.hg'})  # 默认排除版本控制目录

    scanner = DirectoryScanner(max_workers=args.workers)

    start_time = time.time()

    # 使用并发扫描
    target_dirs = args.target_dir if isinstance(args.target_dir, list) else [args.target_dir]
    scanner = DirectoryScanner(max_workers=args.workers)
    all_results = scanner.scan_all_concurrent(args.path, target_dirs, exclude_dirs)

    end_time = time.time()

    if not all_results:
        print(f"❌ 未找到任何目标目录: {', '.join(target_dirs)}")
        return

    # 计算总体统计（过滤前）
    existing_results = [r for r in all_results if r.exists and r.size_bytes > 0]
    total_size = sum(r.size_bytes for r in existing_results)
    total_count = len(existing_results)

    # 应用大小过滤
    filtered_results = scanner.filter_results_by_size(existing_results, min_size_bytes)
    filtered_size = sum(r.size_bytes for r in filtered_results)
    filtered_count = len(filtered_results)

    # 简单输出：只显示目录和大小
    output_lines = []
    output_lines.append("=" * 60)
    if len(target_dirs) == 1:
        output_lines.append(f"{target_dirs[0]} 目录扫描结果")
    else:
        output_lines.append(f"多目录并发扫描结果: {', '.join(target_dirs)}")
    output_lines.append("=" * 60)

    # 显示过滤信息
    if min_size_bytes > 0:
        output_lines.append(f"过滤条件: 大小 >= {scanner.format_size(min_size_bytes)}")
        output_lines.append(f"过滤前: {scanner.format_size(total_size)} ({total_count} 个目录)")
        output_lines.append(f"过滤后: {scanner.format_size(filtered_size)} ({filtered_count} 个目录)")
        if filtered_count < total_count:
            hidden_count = total_count - filtered_count
            hidden_size = total_size - filtered_size
            output_lines.append(f"已隐藏: {scanner.format_size(hidden_size)} ({hidden_count} 个小目录)")
    else:
        output_lines.append(f"总大小: {scanner.format_size(total_size)}")
        output_lines.append(f"目录数: {total_count}")

    output_lines.append(f"扫描时间: {end_time - start_time:.2f} 秒")
    output_lines.append("")

    # 按大小排序显示，并标注目录类型（使用过滤后的结果）
    display_results = filtered_results if min_size_bytes > 0 else existing_results
    sorted_results = sorted(display_results, key=lambda x: x.size_bytes, reverse=True)

    for i, result in enumerate(sorted_results, 1):
        target_type = getattr(result, 'target_type', '未知')
        output_lines.append(f"{i:2d}. {target_type} | {result.path} | {result.size_human}")

    output_text = "\n".join(output_lines)

    # 生成清理脚本
    if args.gen_script:
        # 使用过滤后的结果生成清理脚本
        script_results = filtered_results if min_size_bytes > 0 else all_results
        script_content = scanner.generate_cleanup_script(script_results, args.gen_script, target_dirs)

        try:
            with open(args.gen_script, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # 为Unix脚本添加执行权限
            if not args.gen_script.lower().endswith(('.bat', '.cmd')):
                import stat
                current_permissions = os.stat(args.gen_script).st_mode
                os.chmod(args.gen_script, current_permissions | stat.S_IEXEC)

            print(f"🎯 清理脚本已生成: {args.gen_script}")
            script_valid_count = len([r for r in script_results if r.exists and r.size_bytes > 0])
            script_total_size = sum(r.size_bytes for r in script_results if r.exists and r.size_bytes > 0)
            print(f"📊 包含 {script_valid_count} 个目录")
            print(f"💾 可释放空间: {scanner.format_size(script_total_size)}")
            if min_size_bytes > 0:
                print(f"🔍 已应用大小过滤: >= {scanner.format_size(min_size_bytes)}")
            print("")
            print("⚠️  使用前请注意:")
            print("1. 🔒 运行前请备份重要数据")
            print("2. 📋 仔细检查要删除的目录列表")
            print("3. 🚀 脚本包含确认提示，安全可控")
            print("")
            if args.gen_script.lower().endswith(('.bat', '.cmd')):
                print(f"🖱️  Windows用户双击运行: {args.gen_script}")
            else:
                print(f"⌨️  运行命令: ./{args.gen_script}")

        except Exception as e:
            print(f"❌ 生成脚本失败: {e}")

    # 输出扫描结果
    if args.file:
        with open(args.file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"📄 扫描结果已保存到: {args.file}")
    else:
        print(output_text)


if __name__ == "__main__":
    main()
