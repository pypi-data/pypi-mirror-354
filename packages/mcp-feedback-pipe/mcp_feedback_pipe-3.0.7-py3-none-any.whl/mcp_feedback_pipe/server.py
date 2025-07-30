"""
MCP反馈通道服务器模块
提供主入口点函数
"""

import sys
import os

# 将根目录添加到Python路径，以便导入根目录的server.py
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# 导入主服务器模块
from server import main

# 重新导出main函数
__all__ = ['main'] 