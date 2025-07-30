"""
MCP反馈通道服务器模块
提供主入口点函数
"""

import sys
import os

def main():
    """主入口点函数"""
    # 尝试多种导入方式来确保兼容性
    try:
        # 方式1：从根目录server.py导入
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from server import main as server_main
        return server_main()
    except ImportError:
        try:
            # 方式2：从当前包的上级目录导入
            parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            sys.path.insert(0, parent_dir)
            from server import main as server_main
            return server_main()
        except ImportError:
            try:
                # 方式3：从安装路径导入
                import pkg_resources
                package_dir = pkg_resources.resource_filename('mcp_feedback_pipe', '')
                parent_dir = os.path.dirname(package_dir)
                sys.path.insert(0, parent_dir)
                from server import main as server_main
                return server_main()
            except ImportError:
                # 方式4：直接从backend包开始构建服务器
                from backend.config import get_server_config
                from backend.app import create_feedback_app
                from backend.server_manager import ServerManager
                import argparse
                
                parser = argparse.ArgumentParser(description="MCP反馈通道服务器")
                parser.add_argument("--port", type=int, default=0, help="服务器端口")
                parser.add_argument("--host", default="127.0.0.1", help="服务器主机")
                parser.add_argument("--debug", action="store_true", help="调试模式")
                
                args = parser.parse_args()
                
                # 启动服务器
                config = get_server_config()
                app = create_feedback_app()
                
                manager = ServerManager(
                    session_id="main",
                    app=app,
                    host=args.host,
                    port=args.port,
                    work_summary="MCP反馈通道服务器",
                    timeout_seconds=0,
                    suggest=[]
                )
                
                print(f"🚀 MCP反馈通道服务器启动中...")
                manager.start()
                
                try:
                    manager.wait_for_completion()
                except KeyboardInterrupt:
                    print("\n👋 服务器正在关闭...")
                    manager.cleanup()

# 重新导出main函数
__all__ = ['main'] 