# 阶段二：实现非阻塞 MCP 工具接口

## 1. 目标

将当前阻塞式的 `collect_feedback` 和 `pick_image` MCP 工具改造为异步模式，允许 AI 客户端在发起需要用户长时间交互的任务后不被阻塞，可以继续执行其他操作，并在稍后查询交互结果。

## 2. 核心策略：异步会话启动与结果查询

将原有的单个阻塞工具调用拆分为多个非阻塞或短时阻塞的工具调用：
1.  **启动交互会话**：AI 调用一个工具来启动 Web 界面，该工具立即返回会话 ID 和访问信息。
2.  **获取交互结果**：AI 调用另一个工具，使用会话 ID 来查询用户交互的结果。此工具可以是非阻塞的（立即返回当前状态）或短时轮询等待。
3.  **取消交互会话 (可选)**：AI 调用一个工具来主动结束不再需要的交互会话。

## 3. 新的 MCP 工具接口定义

### 3.1. `start_interactive_session`

*   **描述**: 启动一个用户交互会话（反馈收集或图片选择），并立即返回会话信息。
*   **参数**:
    *   `interaction_type: str` (必需): 交互类型，例如 "feedback" 或 "image_picker"。
    *   `work_summary: str` (可选, 仅当 `interaction_type` 为 "feedback" 时相关): AI 的工作摘要。
    *   `suggest: List[str]` (可选, 仅当 `interaction_type` 为 "feedback" 时相关): 给用户的建议选项列表。
    *   `initial_timeout_seconds: int` (可选, 默认 300): Web 界面本身的超时时间（秒）。
*   **返回**: `Dict`
    *   `session_id: str`: 唯一的会话标识符。
    *   `access_url: str`: 用户在本地浏览器（配置好端口转发后）访问 Web 界面的 URL (例如, `http://127.0.0.1:RECOMMENDED_LOCAL_PORT/`)。
    *   `ssh_forward_command_suggestion: str`: 建议用户执行的 SSH 端口转发命令，包含远程服务实际监听的端口。
    *   `actual_remote_port: int`: Web 服务在远程服务器上实际监听的端口。
    *   `status: str`: "pending_user_input"。

### 3.2. `get_interactive_session_result`

*   **描述**: 获取指定交互会话的结果。
*   **参数**:
    *   `session_id: str` (必需): 由 `start_interactive_session` 返回的会话 ID。
    *   `polling_timeout_seconds: int` (可选, 默认 0): 此工具调用自身的等待/轮询超时时间（秒）。
        *   如果为 `0`，则立即返回当前结果或状态。
        *   如果大于 `0`，则在该时间内短时阻塞/轮询等待结果。
*   **返回**: `Dict`
    *   `session_id: str`: 对应的会话 ID。
    *   `status: str`: 会话状态，可能的值：
        *   `"completed"`: 用户已提交反馈/选择图片。
        *   `"pending_user_input"`: 仍在等待用户操作。
        *   `"session_timed_out"`: Web 界面已超时（根据 `initial_timeout_seconds`）。
        *   `"polling_timed_out"`: 本次 `get_interactive_session_result` 调用超时，但会话本身可能仍在进行。
        *   `"session_not_found"`: 未找到指定的会话 ID。
        *   `"error"`: 处理过程中发生错误。
    *   `data: Optional[List]` (仅当 `status` 为 `"completed"` 时存在): 包含用户反馈内容的列表（与原 `collect_feedback` 返回格式一致，可能包含文本和 MCPImage 对象）。
    *   `error_message: Optional[str]` (仅当 `status` 为 `"error"` 时存在): 错误信息。

### 3.3. `cancel_interactive_session` (可选但推荐)

*   **描述**: 主动取消一个正在进行的交互会话。
*   **参数**:
    *   `session_id: str` (必需): 要取消的会话 ID。
*   **返回**: `Dict`
    *   `session_id: str`: 被取消的会话 ID。
    *   `status: str`: 通常为 `"cancelled"` 或 `"not_found"`。

## 4. 主要代码修改点

*   **`server.py`**:
    *   实现上述三个新的 MCP 工具。
    *   移除或标记废弃旧的 `collect_feedback` 和 `pick_image` 工具。
    *   `session_id` 的生成和传递逻辑。
*   **`backend/server_manager.py`**:
    *   `start_server` 方法基本保持不变（仍由 `start_interactive_session` 间接调用），但其返回值（端口号）将被新工具使用。
    *   `wait_for_feedback` 方法的逻辑需要被分解和调整：
        *   一部分用于检查 `FeedbackHandler` 中是否有结果（供 `get_interactive_session_result` 使用）。
        *   Web 界面本身的超时逻辑（`initial_timeout_seconds`）仍需在此或 `FeedbackApp` 中处理，超时后应能标记会话状态。
    *   可能需要添加方法来通过 `session_id` 查询特定 `ServerManager` 实例的状态或其 `FeedbackHandler` 的状态。
*   **`backend/feedback_handler.py`**:
    *   `get_result()` 方法可能需要一个非阻塞的变体 `check_result()`，或者 `get_result()` 的 `timeout` 参数需要能被 `get_interactive_session_result` 精确控制。
    *   需要能与特定的 `session_id` 关联反馈结果。
*   **`backend/server_pool.py`**:
    *   `get_managed_server(session_id)` 依然用于获取与特定会话关联的 `ServerManager`。
    *   `release_managed_server(session_id, immediate=True)` 的调用时机：
        *   当 `get_interactive_session_result` 返回最终状态（`completed`, `session_timed_out`, `error` 且无法恢复）后。
        *   当 `cancel_interactive_session` 被调用时。
        *   需要有机制清理长时间处于 `pending_user_input` 但无人查询的僵尸会话。

## 5. 状态管理和资源清理

*   服务器需要维护每个 `session_id` 的状态（例如：`pending_input`, `processing_input`, `completed`, `timed_out`, `cancelled`, `error`）。
*   必须确保与每个会话关联的 Web 服务 (`FeedbackApp` 实例和其监听的端口) 在会话结束（完成、超时、取消、错误后无法恢复）时被正确关闭和清理，以释放端口和系统资源。

## 6. 对 AI 客户端的影响

*   AI 客户端需要调整其逻辑，以适应新的异步工具调用模式：
    1.  调用 `start_interactive_session`。
    2.  向用户展示访问信息。
    3.  在不阻塞主流程的情况下，定期调用 `get_interactive_session_result` 轮询结果。
    4.  根据返回的状态和数据进行后续操作。
    5.  （可选）在适当时机调用 `cancel_interactive_session`。

## 7. 预期效果

*   AI 客户端在发起需要用户交互的工具调用后，不会被长时间阻塞，可以继续执行其他任务。
*   提高了 AI 的并发处理能力和用户体验。
*   单个用户仍然可以通过不同的会话 ID 同时与多个反馈界面交互（如果 AI 客户端支持并行发起多个 `start_interactive_session` 调用）。