#!/usr/bin/env python3
"""
Clear Dev GUI - Graphical User Interface Entry Point

Entry point for the GUI version of Clear Dev.
"""

import sys

def main():
    """Main GUI entry point"""
    try:
        # 检查PySide6是否可用
        try:
            from PySide6.QtWidgets import QApplication
            from .gui_app import MainWindow
        except ImportError:
            print("❌ PySide6 未安装，请安装GUI依赖:")
            print("   pip install clear-dev[gui]")
            print("   或")
            print("   pip install PySide6")
            sys.exit(1)
        
        # 启动GUI应用
        app = QApplication(sys.argv)
        app.setApplicationName("Clear Dev")
        app.setOrganizationName("Clear Dev")
        
        window = MainWindow()
        window.show()
        
        sys.exit(app.exec())
        
    except KeyboardInterrupt:
        print("\n⚠️  应用已关闭")
        sys.exit(0)
    except Exception as e:
        print(f"❌ GUI启动失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
