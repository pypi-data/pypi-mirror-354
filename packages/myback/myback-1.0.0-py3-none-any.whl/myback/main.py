"""
主入口模块 - 启动MCP服务器
"""

from .tools import mcp


def main():
    """Main entry point for the myback command."""
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序运行出错: {e}")


if __name__ == "__main__":
    main()
