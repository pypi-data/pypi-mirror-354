"""
MCP工具模块 - 定义MCP服务器工具
"""

import io
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pathlib import Path
from datetime import datetime
import os

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image as MCPImage
from mcp.types import TextContent

from .dialog import FeedbackDialog, DIALOG_TIMEOUT

# 创建MCP服务器
mcp = FastMCP(
    "交互式反馈收集器",
    dependencies=["pillow", "tkinter"]
)


@mcp.tool()
def collect_feedback(work_summary: str = "", timeout_seconds: int = DIALOG_TIMEOUT) -> list:
    """
    收集用户反馈的交互式工具。AI可以汇报完成的工作，用户可以提供文字和/或图片反馈。
    
    Args:
        work_summary: AI完成的工作内容汇报
        timeout_seconds: 对话框超时时间（秒），默认300秒（5分钟）
        
    Returns:
        包含用户反馈内容的列表，可能包含文本和图片
    """
    dialog = FeedbackDialog(work_summary, timeout_seconds)
    result = dialog.show_dialog()
    
    if result is None:
        raise Exception(f"操作超时（{timeout_seconds}秒），请重试")
        
    if not result['success']:
        raise Exception(result.get('message', '用户取消了反馈提交'))
    
    # 构建返回内容列表
    feedback_items = []
    
    # 添加文字反馈
    if result['has_text']:
        feedback_items.append(TextContent(
            type="text", 
            text=f"用户文字反馈：{result['text_feedback']}\n提交时间：{result['timestamp']}"
        ))
        
    # 添加图片反馈
    if result['has_images']:
        for image_data, source in zip(result['images'], result['image_sources']):
            feedback_items.append(MCPImage(data=image_data, format='png'))
        
    return feedback_items


@mcp.tool()
def pick_image() -> MCPImage:
    """
    弹出图片选择对话框，让用户选择图片文件或从剪贴板粘贴图片。
    用户可以选择本地图片文件，或者先截图到剪贴板然后粘贴。
    """
    def simple_image_dialog():
        root = tk.Tk()
        root.title("选择图片")
        root.geometry("400x300")
        root.resizable(False, False)
        root.eval('tk::PlaceWindow . center')
        
        selected_image = {'data': None}
        
        def select_file():
            file_path = filedialog.askopenfilename(
                title="选择图片文件",
                filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp")]
            )
            if file_path:
                try:
                    with open(file_path, 'rb') as f:
                        selected_image['data'] = f.read()
                    root.destroy()
                except Exception as e:
                    messagebox.showerror("错误", f"无法读取图片: {e}")
                    
        def paste_clipboard():
            try:
                from PIL import ImageGrab
                clipboard_content = ImageGrab.grabclipboard()

                # 处理不同类型的剪贴板内容
                img = None
                if clipboard_content is not None:
                    # 如果是列表，取第一个元素
                    if isinstance(clipboard_content, list):
                        if len(clipboard_content) > 0:
                            img = clipboard_content[0]
                        else:
                            messagebox.showwarning("警告", "剪贴板中的图片列表为空")
                            return
                    else:
                        # 直接是图片对象
                        img = clipboard_content

                if img and hasattr(img, 'save'):
                    buffer = io.BytesIO()
                    img.save(buffer, format='PNG')
                    selected_image['data'] = buffer.getvalue()
                    root.destroy()
                else:
                    messagebox.showwarning("警告", "剪贴板中没有有效的图片数据")
            except Exception as e:
                messagebox.showerror("错误", f"剪贴板操作失败: {e}")
                
        def cancel():
            root.destroy()
            
        # 界面
        tk.Label(root, text="请选择图片来源", font=("Arial", 14, "bold")).pack(pady=20)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="📁 选择图片文件", font=("Arial", 12), 
                 width=20, height=2, command=select_file).pack(pady=10)
        tk.Button(btn_frame, text="📋 从剪贴板粘贴", font=("Arial", 12), 
                 width=20, height=2, command=paste_clipboard).pack(pady=10)
        tk.Button(btn_frame, text="❌ 取消", font=("Arial", 12), 
                 width=20, height=1, command=cancel).pack(pady=10)
        
        root.mainloop()
        return selected_image['data']
    
    image_data = simple_image_dialog()
    
    if image_data is None:
        raise Exception("未选择图片或操作被取消")
        
    return MCPImage(data=image_data, format='png')


@mcp.tool()
def get_image_info(image_path: str) -> str:
    """
    获取指定路径图片的信息（尺寸、格式等）
    
    Args:
        image_path: 图片文件路径
    """
    try:
        path = Path(image_path)
        if not path.exists():
            return f"文件不存在: {image_path}"
            
        with Image.open(path) as img:
            info = {
                "文件名": path.name,
                "格式": img.format,
                "尺寸": f"{img.width} x {img.height}",
                "模式": img.mode,
                "文件大小": f"{path.stat().st_size / 1024:.1f} KB"
            }
            
        return "\n".join([f"{k}: {v}" for k, v in info.items()])
        
    except Exception as e:
        return f"获取图片信息失败: {str(e)}"


# 导出MCP服务器实例
__all__ = ['mcp', 'collect_feedback', 'pick_image', 'get_image_info']
