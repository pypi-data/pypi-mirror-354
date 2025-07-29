#!/usr/bin/env python3
"""
DirectoryScanner GUI - PySide6图形界面
为DirectoryScanner.py提供现代化的图形用户界面
"""

import sys
import os
import json
from pathlib import Path
from typing import List, Optional
from dataclasses import asdict

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QSpinBox, QTableWidget, QTableWidgetItem,
    QFileDialog, QMessageBox, QProgressBar, QStatusBar, QGroupBox,
    QTextEdit, QSplitter, QHeaderView, QAbstractItemView
)
from PySide6.QtCore import QThread, Signal, Qt, QTimer, QSettings
from PySide6.QtGui import QFont, QIcon

# 导入原有的扫描器类
from .scanner import DirectoryScanner, DirectoryScanResult


class ScanWorker(QThread):
    """异步扫描工作线程"""
    progress_updated = Signal(int, int)  # 当前进度, 总数
    result_ready = Signal(DirectoryScanResult)  # 单个结果就绪
    scan_finished = Signal(list)  # 扫描完成，返回所有结果
    error_occurred = Signal(str)  # 错误信息
    
    def __init__(self, root_path: str, target_dirs: List[str], 
                 exclude_dirs: set, max_workers: int = 8):
        super().__init__()
        self.root_path = root_path
        self.target_dirs = target_dirs
        self.exclude_dirs = exclude_dirs
        self.max_workers = max_workers
        self.scanner = DirectoryScanner(max_workers=max_workers)
        
    def run(self):
        """执行扫描任务"""
        try:
            # 执行扫描
            results = self.scanner.scan_all_concurrent(
                self.root_path, 
                self.target_dirs, 
                self.exclude_dirs,
                show_progress=False  # GUI中不显示命令行进度
            )
            
            # 发送完成信号
            self.scan_finished.emit(results)
            
        except Exception as e:
            self.error_occurred.emit(str(e))


class ConfigPanel(QWidget):
    """左侧配置面板"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化配置面板UI"""
        layout = QVBoxLayout()
        
        # 目录选择组
        dir_group = QGroupBox("扫描目录")
        dir_layout = QVBoxLayout()
        
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("选择要扫描的根目录...")
        self.browse_btn = QPushButton("浏览...")
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_btn)
        
        dir_layout.addLayout(path_layout)
        dir_group.setLayout(dir_layout)
        
        # 目标目录组
        target_group = QGroupBox("目标目录")
        target_layout = QVBoxLayout()
        
        self.target_edit = QLineEdit("node_modules")
        self.target_edit.setPlaceholderText("要搜索的目录名称，多个用逗号分隔")
        
        target_layout.addWidget(QLabel("目录名称:"))
        target_layout.addWidget(self.target_edit)
        target_group.setLayout(target_layout)
        
        # 过滤选项组
        filter_group = QGroupBox("过滤选项")
        filter_layout = QVBoxLayout()
        
        self.min_size_edit = QLineEdit()
        self.min_size_edit.setPlaceholderText("如: 100M, 1G, 500MB")
        
        self.exclude_edit = QLineEdit(".git,.svn,.hg")
        self.exclude_edit.setPlaceholderText("排除的目录，用逗号分隔")
        
        filter_layout.addWidget(QLabel("最小大小:"))
        filter_layout.addWidget(self.min_size_edit)
        filter_layout.addWidget(QLabel("排除目录:"))
        filter_layout.addWidget(self.exclude_edit)
        filter_group.setLayout(filter_layout)
        
        # 性能设置组
        perf_group = QGroupBox("性能设置")
        perf_layout = QVBoxLayout()
        
        self.workers_spin = QSpinBox()
        self.workers_spin.setRange(1, 32)
        self.workers_spin.setValue(8)
        
        perf_layout.addWidget(QLabel("并发线程数:"))
        perf_layout.addWidget(self.workers_spin)
        perf_group.setLayout(perf_layout)
        
        # 操作按钮
        self.scan_btn = QPushButton("开始扫描")
        self.scan_btn.setStyleSheet("QPushButton { font-weight: bold; padding: 8px; }")
        
        # 添加所有组件到主布局
        layout.addWidget(dir_group)
        layout.addWidget(target_group)
        layout.addWidget(filter_group)
        layout.addWidget(perf_group)
        layout.addStretch()
        layout.addWidget(self.scan_btn)
        
        self.setLayout(layout)
        
    def get_config(self) -> dict:
        """获取当前配置"""
        return {
            'root_path': self.path_edit.text().strip(),
            'target_dirs': [d.strip() for d in self.target_edit.text().split(',') if d.strip()],
            'min_size': self.min_size_edit.text().strip(),
            'exclude_dirs': set(d.strip() for d in self.exclude_edit.text().split(',') if d.strip()),
            'max_workers': self.workers_spin.value()
        }


class ResultsPanel(QWidget):
    """右侧结果显示面板"""
    
    def __init__(self):
        super().__init__()
        self.results = []
        self.init_ui()
        
    def init_ui(self):
        """初始化结果面板UI"""
        layout = QVBoxLayout()
        
        # 统计信息
        stats_group = QGroupBox("扫描统计")
        stats_layout = QHBoxLayout()
        
        self.total_size_label = QLabel("总大小: 0 B")
        self.total_count_label = QLabel("目录数: 0")
        self.scan_time_label = QLabel("扫描时间: 0 秒")
        
        stats_layout.addWidget(self.total_size_label)
        stats_layout.addWidget(self.total_count_label)
        stats_layout.addWidget(self.scan_time_label)
        stats_layout.addStretch()
        
        stats_group.setLayout(stats_layout)
        
        # 结果表格
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["序号", "类型", "路径", "大小"])
        
        # 设置表格属性
        header = self.results_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.results_table.setAlternatingRowColors(True)
        
        # 操作按钮
        btn_layout = QHBoxLayout()
        self.export_btn = QPushButton("导出结果")
        self.script_btn = QPushButton("生成清理脚本")
        self.clear_btn = QPushButton("清空结果")

        # 初始状态禁用按钮
        self.export_btn.setEnabled(False)
        self.script_btn.setEnabled(False)
        self.clear_btn.setEnabled(False)

        btn_layout.addWidget(self.export_btn)
        btn_layout.addWidget(self.script_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.clear_btn)

        # 添加到主布局
        layout.addWidget(stats_group)
        layout.addWidget(self.results_table)
        layout.addLayout(btn_layout)

        self.setLayout(layout)


class MainWindow(QMainWindow):
    """主窗口类"""

    def __init__(self):
        super().__init__()
        self.scanner_thread = None
        self.scan_start_time = None
        self.settings = QSettings("DirectoryScanner", "GUI")
        self.init_ui()
        self.connect_signals()
        self.load_settings()

    def init_ui(self):
        """初始化主窗口UI"""
        self.setWindowTitle("Directory Scanner - 目录扫描器")
        self.setGeometry(100, 100, 1200, 800)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QHBoxLayout()

        # 创建分割器
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # 创建左右面板
        self.config_panel = ConfigPanel()
        self.results_panel = ResultsPanel()

        # 设置面板大小比例
        splitter.addWidget(self.config_panel)
        splitter.addWidget(self.results_panel)
        splitter.setSizes([300, 900])  # 左侧300px，右侧900px

        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)

        # 状态标签
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)

    def connect_signals(self):
        """连接信号和槽"""
        # 配置面板信号
        self.config_panel.browse_btn.clicked.connect(self.browse_directory)
        self.config_panel.scan_btn.clicked.connect(self.start_scan)

        # 结果面板信号
        self.results_panel.export_btn.clicked.connect(self.export_results)
        self.results_panel.script_btn.clicked.connect(self.generate_script)
        self.results_panel.clear_btn.clicked.connect(self.clear_results)

    def load_settings(self):
        """加载保存的设置"""
        # 恢复窗口几何
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

        # 恢复配置
        self.config_panel.path_edit.setText(self.settings.value("root_path", ""))
        self.config_panel.target_edit.setText(self.settings.value("target_dirs", "node_modules"))
        self.config_panel.min_size_edit.setText(self.settings.value("min_size", ""))
        self.config_panel.exclude_edit.setText(self.settings.value("exclude_dirs", ".git,.svn,.hg"))
        self.config_panel.workers_spin.setValue(int(self.settings.value("max_workers", 8)))

    def save_settings(self):
        """保存当前设置"""
        self.settings.setValue("geometry", self.saveGeometry())
        config = self.config_panel.get_config()
        self.settings.setValue("root_path", config['root_path'])
        self.settings.setValue("target_dirs", ','.join(config['target_dirs']))
        self.settings.setValue("min_size", config['min_size'])
        self.settings.setValue("exclude_dirs", ','.join(config['exclude_dirs']))
        self.settings.setValue("max_workers", config['max_workers'])

    def closeEvent(self, event):
        """窗口关闭事件"""
        self.save_settings()
        if self.scanner_thread and self.scanner_thread.isRunning():
            self.scanner_thread.terminate()
            self.scanner_thread.wait()
        event.accept()

    def browse_directory(self):
        """浏览选择目录"""
        directory = QFileDialog.getExistingDirectory(
            self, "选择要扫描的目录", self.config_panel.path_edit.text()
        )
        if directory:
            self.config_panel.path_edit.setText(directory)

    def start_scan(self):
        """开始扫描"""
        config = self.config_panel.get_config()

        # 验证配置
        if not config['root_path']:
            QMessageBox.warning(self, "配置错误", "请选择要扫描的根目录")
            return

        if not config['target_dirs']:
            QMessageBox.warning(self, "配置错误", "请输入要搜索的目标目录名称")
            return

        if not os.path.exists(config['root_path']):
            QMessageBox.warning(self, "路径错误", f"目录不存在: {config['root_path']}")
            return

        # 解析最小大小
        min_size_bytes = 0
        if config['min_size']:
            try:
                min_size_bytes = DirectoryScanner.parse_size_string(config['min_size'])
            except ValueError as e:
                QMessageBox.warning(self, "参数错误", str(e))
                return

        # 禁用扫描按钮，显示进度
        self.config_panel.scan_btn.setEnabled(False)
        self.config_panel.scan_btn.setText("扫描中...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # 不确定进度
        self.status_label.setText("正在扫描...")

        # 记录开始时间
        import time
        self.scan_start_time = time.time()

        # 创建并启动扫描线程
        self.scanner_thread = ScanWorker(
            config['root_path'],
            config['target_dirs'],
            config['exclude_dirs'],
            config['max_workers']
        )

        # 连接线程信号
        self.scanner_thread.scan_finished.connect(self.on_scan_finished)
        self.scanner_thread.error_occurred.connect(self.on_scan_error)

        # 启动线程
        self.scanner_thread.start()

    def on_scan_finished(self, results: List[DirectoryScanResult]):
        """扫描完成处理"""
        import time
        scan_time = time.time() - self.scan_start_time if self.scan_start_time else 0

        # 恢复UI状态
        self.config_panel.scan_btn.setEnabled(True)
        self.config_panel.scan_btn.setText("开始扫描")
        self.progress_bar.setVisible(False)
        self.status_label.setText("扫描完成")

        # 应用大小过滤
        config = self.config_panel.get_config()
        min_size_bytes = 0
        if config['min_size']:
            try:
                min_size_bytes = DirectoryScanner.parse_size_string(config['min_size'])
            except ValueError:
                pass

        scanner = DirectoryScanner()
        filtered_results = scanner.filter_results_by_size(results, min_size_bytes)

        # 更新结果显示
        self.update_results_display(filtered_results, scan_time)

        # 显示完成消息
        valid_count = len([r for r in filtered_results if r.exists and r.size_bytes > 0])
        QMessageBox.information(
            self, "扫描完成",
            f"扫描完成！\n找到 {valid_count} 个目录\n用时 {scan_time:.2f} 秒"
        )

    def on_scan_error(self, error_msg: str):
        """扫描错误处理"""
        # 恢复UI状态
        self.config_panel.scan_btn.setEnabled(True)
        self.config_panel.scan_btn.setText("开始扫描")
        self.progress_bar.setVisible(False)
        self.status_label.setText("扫描失败")

        # 显示错误消息
        QMessageBox.critical(self, "扫描错误", f"扫描过程中发生错误:\n{error_msg}")

    def update_results_display(self, results: List[DirectoryScanResult], scan_time: float):
        """更新结果显示"""
        # 保存结果
        self.results_panel.results = results

        # 计算统计信息
        valid_results = [r for r in results if r.exists and r.size_bytes > 0]
        total_size = sum(r.size_bytes for r in valid_results)
        total_count = len(valid_results)

        # 更新统计标签
        scanner = DirectoryScanner()
        self.results_panel.total_size_label.setText(f"总大小: {scanner.format_size(total_size)}")
        self.results_panel.total_count_label.setText(f"目录数: {total_count}")
        self.results_panel.scan_time_label.setText(f"扫描时间: {scan_time:.2f} 秒")

        # 更新表格
        self.update_results_table(valid_results)

    def update_results_table(self, results: List[DirectoryScanResult]):
        """更新结果表格"""
        # 按大小排序（从大到小）
        sorted_results = sorted(results, key=lambda x: x.size_bytes, reverse=True)

        # 设置表格行数
        self.results_panel.results_table.setRowCount(len(sorted_results))

        # 填充表格数据
        for i, result in enumerate(sorted_results):
            # 序号
            self.results_panel.results_table.setItem(i, 0, QTableWidgetItem(str(i + 1)))

            # 类型
            target_type = getattr(result, 'target_type', '未知')
            self.results_panel.results_table.setItem(i, 1, QTableWidgetItem(target_type))

            # 路径
            self.results_panel.results_table.setItem(i, 2, QTableWidgetItem(result.path))

            # 大小
            self.results_panel.results_table.setItem(i, 3, QTableWidgetItem(result.size_human))

        # 启用操作按钮
        self.results_panel.export_btn.setEnabled(len(sorted_results) > 0)
        self.results_panel.script_btn.setEnabled(len(sorted_results) > 0)
        self.results_panel.clear_btn.setEnabled(len(sorted_results) > 0)

    def export_results(self):
        """导出结果到文件"""
        if not self.results_panel.results:
            QMessageBox.information(self, "提示", "没有可导出的结果")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出扫描结果", "scan_results.txt", "文本文件 (*.txt);;所有文件 (*)"
        )

        if not file_path:
            return

        try:
            # 生成输出内容
            output_lines = []
            output_lines.append("=" * 60)
            output_lines.append("Directory Scanner 扫描结果")
            output_lines.append("=" * 60)

            # 统计信息
            valid_results = [r for r in self.results_panel.results if r.exists and r.size_bytes > 0]
            total_size = sum(r.size_bytes for r in valid_results)
            scanner = DirectoryScanner()

            output_lines.append(f"总大小: {scanner.format_size(total_size)}")
            output_lines.append(f"目录数: {len(valid_results)}")
            output_lines.append("")

            # 结果列表
            sorted_results = sorted(valid_results, key=lambda x: x.size_bytes, reverse=True)
            for i, result in enumerate(sorted_results, 1):
                target_type = getattr(result, 'target_type', '未知')
                output_lines.append(f"{i:2d}. {target_type} | {result.path} | {result.size_human}")

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(output_lines))

            QMessageBox.information(self, "导出成功", f"结果已导出到:\n{file_path}")

        except Exception as e:
            QMessageBox.critical(self, "导出失败", f"导出过程中发生错误:\n{str(e)}")

    def generate_script(self):
        """生成清理脚本"""
        if not self.results_panel.results:
            QMessageBox.information(self, "提示", "没有可生成脚本的结果")
            return

        # 选择脚本类型和保存位置
        file_path, _ = QFileDialog.getSaveFileName(
            self, "生成清理脚本", "cleanup_script.sh",
            "Shell脚本 (*.sh);;批处理文件 (*.bat);;所有文件 (*)"
        )

        if not file_path:
            return

        try:
            config = self.config_panel.get_config()
            scanner = DirectoryScanner()

            # 生成脚本内容
            script_content = scanner.generate_cleanup_script(
                self.results_panel.results,
                file_path,
                config['target_dirs'],
                script_mode="auto"
            )

            # 写入脚本文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(script_content)

            # 为Unix脚本添加执行权限
            if file_path.endswith('.sh'):
                import stat
                current_permissions = os.stat(file_path).st_mode
                os.chmod(file_path, current_permissions | stat.S_IEXEC)

            valid_count = len([r for r in self.results_panel.results if r.exists and r.size_bytes > 0])
            total_size = sum(r.size_bytes for r in self.results_panel.results if r.exists and r.size_bytes > 0)

            QMessageBox.information(
                self, "脚本生成成功",
                f"清理脚本已生成:\n{file_path}\n\n"
                f"包含 {valid_count} 个目录\n"
                f"可释放空间: {scanner.format_size(total_size)}\n\n"
                f"⚠️ 使用前请备份重要数据！"
            )

        except Exception as e:
            QMessageBox.critical(self, "生成失败", f"生成脚本时发生错误:\n{str(e)}")

    def clear_results(self):
        """清空结果"""
        reply = QMessageBox.question(
            self, "确认清空", "确定要清空所有扫描结果吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.results_panel.results = []
            self.results_panel.results_table.setRowCount(0)
            self.results_panel.total_size_label.setText("总大小: 0 B")
            self.results_panel.total_count_label.setText("目录数: 0")
            self.results_panel.scan_time_label.setText("扫描时间: 0 秒")

            # 禁用操作按钮
            self.results_panel.export_btn.setEnabled(False)
            self.results_panel.script_btn.setEnabled(False)
            self.results_panel.clear_btn.setEnabled(False)

            self.status_label.setText("已清空结果")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Directory Scanner")
    app.setOrganizationName("DirectoryScanner")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())
