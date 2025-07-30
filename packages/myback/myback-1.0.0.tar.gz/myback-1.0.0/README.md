# MyBack - 交互式反馈收集工具

一个基于MCP协议的图形化反馈收集工具，支持文字和图片反馈。

## 功能特性

- 🎯 **交互式反馈收集**：提供美观的GUI界面收集用户反馈
- 💬 **文字反馈**：支持多行文本输入，可以提供详细的文字反馈
- 🖼️ **图片反馈**：支持多张图片上传，可以从文件选择或剪贴板粘贴
- 📋 **剪贴板支持**：直接从剪贴板粘贴截图或复制的图片
- ⏱️ **超时控制**：可配置对话框超时时间，避免长时间等待
- 🔧 **MCP工具集成**：作为MCP工具可以被AI助手调用

## 安装方法

### 方法1：从PyPI安装（推荐）

```bash
pip install myback
```

### 方法2：从源码安装

```bash
git clone https://github.com/yourusername/myback.git
cd myback
pip install -e .
```

### 方法3：使用uv安装

```bash
# 安装uv（如果还没有安装）
pip install uv

# 使用uv安装myback
uv pip install myback

# 或者直接运行（无需安装）
uvx myback
```

## 使用方法

### 作为命令行工具

```bash
# 启动MCP服务器
myback

# 或者
myback-server
```

### 作为Python模块

```python
from myback import collect_feedback, pick_image, get_image_info

# 收集用户反馈
feedback = collect_feedback("AI完成了某项工作的汇报")

# 选择单张图片
image = pick_image()

# 获取图片信息
info = get_image_info("/path/to/image.png")
```

### 在MCP客户端中使用

将myback配置为MCP服务器，然后在支持MCP的AI客户端中使用：

```json
{
  "mcpServers": {
    "myback": {
      "command": "myback",
      "args": []
    }
  }
}
```

## 可用工具

### collect_feedback

收集用户反馈的交互式工具。

**参数：**
- `work_summary` (str): AI完成的工作内容汇报
- `timeout_seconds` (int): 对话框超时时间（秒），默认300秒

**返回：**
- 包含用户反馈内容的列表，可能包含文本和图片

### pick_image

弹出图片选择对话框。

**返回：**
- 用户选择的图片数据

### get_image_info

获取指定路径图片的信息。

**参数：**
- `image_path` (str): 图片文件路径

**返回：**
- 图片信息字符串（尺寸、格式等）

## 环境变量

- `MCP_DIALOG_TIMEOUT`: 设置对话框默认超时时间（秒），默认为300秒

## 系统要求

- Python 3.8+
- tkinter（通常随Python一起安装）
- Windows系统需要pywin32（用于剪贴板支持）

## 开发

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 代码格式化

```bash
black myback/
```

### 类型检查

```bash
mypy myback/
```

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持文字和图片反馈收集
- 支持剪贴板图片粘贴
- 提供MCP工具接口
