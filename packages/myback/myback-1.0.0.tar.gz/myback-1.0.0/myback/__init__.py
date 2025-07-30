"""
myback - 交互式反馈收集工具

一个基于MCP协议的图形化反馈收集工具，支持文字和图片反馈。
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "交互式反馈收集工具 - 支持文字和图片反馈的MCP工具"

# 导入主要功能
from .main import main
from .dialog import FeedbackDialog
from .tools import collect_feedback, pick_image, get_image_info

__all__ = [
    'main',
    'FeedbackDialog', 
    'collect_feedback',
    'pick_image',
    'get_image_info',
]
