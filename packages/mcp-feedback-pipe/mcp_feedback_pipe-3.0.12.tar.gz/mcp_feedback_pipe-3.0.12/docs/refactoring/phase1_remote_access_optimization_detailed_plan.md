# 详细实施计划：优化远程访问便捷性 (阶段一)

## 背景与澄清

**关于VSCode Remote SSH插件与端口转发：**

通常情况下，当使用 VSCode Remote SSH 插件并在远程服务器上启动一个监听 `localhost` 或 `127.0.0.1` 的服务时，VSCode 会自动处理端口转发。这意味着用户可以直接在本地浏览器通过 `http://localhost:<forwarded_port>` 访问服务，无需手动执行 `ssh -L` 命令。项目文档 ([`README.md:158`](README.md:158)) 也提到了这一点。

尽管如此，在 `server.py` 的日志输出中提供手动设置SSH端口转发的命令仍然是有价值的：
1.  **通用性**：确保不使用 VSCode Remote SSH 的用户也能获得清晰指引。
2.  **明确性**：帮助用户理解服务运行情况，并在自动转发失效时进行排错。
3.  **可配置性**：推荐的固定本地端口 (`recommended_local_port`) 为用户提供一致的访问点。

因此，我们将在日志中保留手动转发指引，并在项目文档中同时提及 VSCode 的自动转发特性。

## 计划目标

优化远程访问便捷性，通过引入首选固定端口和改进用户指引，简化用户在远程 SSH 环境下访问由 `collect_feedback` 和 `pick_image` 工具启动的 Web 界面的操作。

## 流程图

```mermaid
graph TD
    A[开始] --> B{步骤 1: 修改端口查找逻辑};
    B --> B1[在 `backend/utils/network_utils.py` 中修改 `find_free_port`];
    B1 --> B2[添加 `preferred_port` 参数];
    B1 --> B3[实现逻辑: 检查 preferred_port -> 可用则返回 -> 不可用则动态查找];
    B --> C{步骤 2: 调整 ServerManager};
    C --> C1[在 `backend/server_manager.py` 的 `ServerManager.start_server` 中];
    C1 --> C2[从配置获取首选端口];
    C1 --> C3[修改调用 `find_free_port` 处，传入首选端口];
    C --> D{步骤 3: 修改 server.py 日志输出};
    D --> D1[在 `server.py` 的 `collect_feedback` 和 `pick_image` 函数中];
    D1 --> D2[获取 `actual_remote_port`];
    D1 --> D3[从配置获取 `recommended_local_port`];
    D1 --> D4[修改 `print` 语句为详细指引, 包含手动转发命令];
    D --> E{步骤 4: 添加配置项};
    E --> E1[在 `backend/config.py` 中];
    E1 --> E2[在 `ServerConfig` 添加 `preferred_web_port` (默认 `8765`)];
    E1 --> E3[在 `ServerConfig` 添加 `recommended_local_forward_port` (默认 `8888`)];
    E1 --> E4[在 `ConfigManager._load_from_env` 实现从环境变量加载];
    E --> F{步骤 5: 更新文档};
    F --> F1[修改 `README.md`];
    F1 --> F2[说明新端口行为, SSH手动转发方法, 并提及VSCode自动转发];
    F --> G[结束];
```

## 详细步骤说明

### 步骤 1: 修改端口查找逻辑 (`backend/utils/network_utils.py`)

1.  **修改 `find_free_port` 函数 ([`backend/utils/network_utils.py:20`](backend/utils/network_utils.py:20))**:
    *   向函数签名中添加一个新参数 `preferred_port: Optional[int] = None`。
    *   **逻辑调整**:
        *   在函数开始处，如果 `preferred_port` 已提供且不为 `None`：
            *   调用 `_test_port_availability(preferred_port, test_timeout)` 检查该端口是否可用。
            *   如果可用，立即返回 `preferred_port`。
            *   如果不可用，记录一条警告日志（例如 `logger.warning(f"首选端口 {preferred_port} 被占用，尝试动态查找...")`），然后继续执行后续的动态端口查找逻辑。
        *   如果 `preferred_port` 未提供或（在检查后）不可用，则执行现有的动态端口查找循环。

### 步骤 2: 调整 `ServerManager` 使用新的端口逻辑 (`backend/server_manager.py`)

1.  **获取首选端口配置**:
    *   在 `ServerManager.start_server` 方法 ([`backend/server_manager.py:56`](backend/server_manager.py:56)) 的开始部分，确保可以访问到配置对象。当前代码中 `self._config` 已经是 `ServerConfig` 的实例。
    *   我们将直接使用 `self._config.preferred_web_port`