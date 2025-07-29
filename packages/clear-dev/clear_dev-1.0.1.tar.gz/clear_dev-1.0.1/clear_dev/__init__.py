"""
Clear Dev - Development Cache and Directory Scanner

A powerful toolkit for scanning and cleaning development caches and directories.
Supports both command-line interface and modern GUI.

Features:
- Fast concurrent directory scanning
- Smart size filtering
- Cross-platform cache detection
- GUI and CLI interfaces
- Cleanup script generation
- Multiple output formats

Author: duolabmeng6
License: MIT
"""

__version__ = "1.0.1"
__author__ = "duolabmeng6"
__email__ = "1715109585@qq.com"
__license__ = "MIT"

from .scanner import DirectoryScanner, DirectoryScanResult

__all__ = [
    "DirectoryScanner",
    "DirectoryScanResult",
    "__version__",
    "__author__",
    "__email__",
    "__license__"
]
