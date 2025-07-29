#!/usr/bin/env python3
"""
Clear Dev CLI - Command Line Interface

Entry point for the command-line interface of Clear Dev.
"""

import sys
from .scanner import main as scanner_main

def main():
    """Main CLI entry point"""
    try:
        scanner_main()
    except KeyboardInterrupt:
        print("\n⚠️  操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
