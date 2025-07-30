# 阶段一：优化远程访问便捷性

## 1. 目标

通过引入首选固定端口和改进用户指引，显著简化用户在远程 SSH 环境下访问由 `collect_feedback` 和 `pick_image` 工具启动的 Web 界面的操作。

## 2. 核心策略

*   **引入首选固定端口**：Web 服务优先尝试在一个预定义的固定端口上运行（例如 `8765`，使其与 `@/mcp-feedback-enhanced` 的默认值一致，或使其可配置）。如果该端口被占用，则回退到动态查找空闲端口。
*   当服务启动时，向用户清晰地提供：
    *   Web 服务实际监听的远程端口号。
    *   推荐的 SSH 本地端口转发命令，建议用户将一个固定的本地端口（例如 `8888`，也可考虑让用户在客户端调用时指定或通过配置设定）转发到远程服务实际监听的端口。
    *   用户在本地浏览器中访问的固定基础 URL（例如 `http://127.0.0.1:8888/`，因为主界面是根路径 `/`）。

## 3. 具体修改步骤

### 步骤 1: 修改端口查找逻辑

*   **文件**: `backend/utils/network_utils.py` (如果此文件不存在，则在 `backend/server_manager.py` 中直接实现或创建一个新的 `network_utils.py`)。
*   **任务**: 实现或修改 `find_free_port` 函数。
    *   它应该接受一个 `preferred_port` 参数（默认值可以设为 `8765`）。
    *   考虑从配置文件或环境变量（例如 `MCP_FEEDBACK_PREFERRED_PORT`）读取这个 `preferred_port`。
    *   函数逻辑：
        1.  检查 `preferred_port` 是否可用。
        2.  如果可用，返回 `preferred_port`。
        3.  如果不可用，则像当前一样动态查找其他空闲端口并返回。

### 步骤 2: 调整 `ServerManager` 使用新的端口逻辑

*   **文件**: `backend/server_manager.py`
*   **位置**: 在 `ServerManager.start_server` 方法中，调用 `find_free_port()` 的地方。
*   **任务**: 修改为调用新的、支持首选端口的端口查找函数，并传入获取到的首选端口。

### 步骤 3: 修改 `server.py` 的日志输出

*   **文件**: `server.py`
*   **位置**: 在 `collect_feedback` 函数和 `pick_image` 函数中，打印 URL 和提示信息的地方。
*   **任务**:
    *   获取 Web 服务实际监听的端口 `actual_remote_port`。
    *   定义或获取一个推荐的本地转发端口 `recommended_local_port` (例如，硬编码为 `8888`，或从配置中读取，例如 `MCP_FEEDBACK_LOCAL_FORWARD_PORT`)。
    *   将当前的 `print` 语句替换为更详细和用户友好的指引，内容如下（以 `collect_feedback` 为例）：
        ```python
        # (获取 actual_remote_port 和 recommended_local_port 之后)
        print(f"✅ 服务已在远程服务器的 127.0.0.1:{actual_remote_port} 启动。")
        print(f"💡 要从您的本地机器访问，请设置SSH端口转发。")
        print(f"   如果您尚未配置，可以在您的本地终端运行类似以下命令：")
        print(f"   ssh -L {recommended_local_port}:127.0.0.1:{actual_remote_port} your_user@your_remote_server_ip")
        print(f"   (请将 'your_user@your_remote_server_ip' 替换为您的实际SSH登录信息)")
        print(f"➡️ 设置转发后，请在您本地的浏览器中打开: http://127.0.0.1:{recommended_local_port}/")
        print(f"⏰ 等待用户反馈... (远程服务超时: {timeout_seconds}秒)")
        ```
        对 `pick_image` 工具的提示做类似修改。

### 步骤 4: （可选但推荐）添加配置项

*   **文件**: `backend/config.py` (如果不存在则创建，或集成到现有配置管理中)。
*   **任务**: 为 `MCP_FEEDBACK_PREFERRED_PORT` (Web 服务首选端口，默认 `8765`) 和 `MCP_FEEDBACK_LOCAL_FORWARD_PORT` (建议的本地转发端口，默认 `8888`) 添加配置项，并提供从环境变量或默认值加载的逻辑。
*   在步骤1和步骤3中相应地使用这些配置值。

### 步骤 5: 更新文档

*   **位置**: 项目的 `README.md` 或专门的文档区域 (例如 `docs/usage_guide.md`)。
*   **任务**: 创建或更新文档，详细说明新的端口行为（首选固定，然后动态）以及如何在 SSH 环境下进行端口转发和访问。包括清晰的示例和故障排除提示。

## 4. 预期效果

*   用户在远程服务器上运行客户端并调用这些工具时，会得到非常明确的指令，告诉他们远程服务运行在哪个动态端口，以及如何设置 SSH 端口转发来从本地访问。
*   用户体验得到改善，减少了因不清楚如何访问远程动态端口服务而产生的困惑。
*   保留了系统原有的并发会话处理能力。