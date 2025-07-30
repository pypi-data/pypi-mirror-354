# 📁 MCP反馈通道项目结构

## 📋 整体结构

```
mcp-feedback-pipe/
├── .venv/                          # 虚拟环境 (新)
├── docs/                           # 文档目录 (新)
│   ├── README.md                   # 文档索引
│   ├── SSH_SETUP.md               # SSH配置指南 (新)
│   ├── DEPLOYMENT_GUIDE.md        # 部署指南
│   └── TEST_REPORT.md             # 测试报告
├── scripts/                        # 脚本目录 (新)
│   └── start_server.py            # 启动脚本
├── src/                           # 源代码目录
│   └── mcp_feedback_pipe/
│       ├── static/                # 静态资源
│       │   ├── css/
│       │   └── js/
│       ├── templates/             # HTML模板
│       ├── __init__.py           # 包初始化 (24行)
│       ├── app.py                # Flask Web应用 (114行)
│       ├── feedback_handler.py   # 反馈数据处理 (62行)
│       ├── server.py             # MCP服务器主程序 (120行)
│       ├── server_manager.py     # 服务器管理 (82行)
│       └── utils.py              # 工具函数 (95行)
├── tests/                         # 测试目录 (新结构)
│   ├── e2e/                      # 端到端测试
│   │   ├── __init__.py
│   │   └── test_user_workflow.py
│   ├── integration/              # 集成测试
│   │   ├── __init__.py
│   │   ├── deploy_test.py        # 部署测试 (新位置)
│   │   ├── test_web_interface.py
│   │   └── test_web_version.py   # Web版本测试 (新位置)
│   ├── unit/                     # 单元测试
│   │   ├── __init__.py
│   │   ├── test_feedback_handler.py
│   │   ├── test_server_manager.py
│   │   └── test_utils.py
│   ├── __init__.py
│   ├── conftest.py               # pytest配置 (更新)
│   ├── run_tests.py
│   ├── test_requirements.txt
│   └── test_validation.py
├── ARCHITECTURE.md               # 架构文档
├── LICENSE                       # 开源许可证
├── MANIFEST.in                   # 打包清单 (更新)
├── PROJECT_STRUCTURE.md          # 项目结构说明 (新)
├── README.md                     # 项目说明
├── RELEASE_NOTES.md              # 发布说明 (更新)
├── claude_config_example.json    # Claude配置示例
├── pyproject.toml               # 项目配置
├── pytest.ini                  # pytest配置
└── requirements.txt             # 依赖列表
```

## 🔧 关键变更

### ✅ 新增结构
- **`.venv/`**: 新的虚拟环境位置（替代 `venv/`）
- **`docs/`**: 专门的文档目录
- **`scripts/`**: 启动和部署脚本
- **`tests/`**: 重新组织的测试结构

### 📝 文档组织
```
docs/
├── user_guide/
│   ├── MCP_SETUP.md              # MCP配置完整指南
│   ├── DEPLOYMENT_GUIDE.md       # 部署方案对比
│   ├── SSH_SETUP.md             # SSH环境配置
│   ├── ARCHITECTURE.md          # 系统架构设计
│   ├── SUGGEST_PARAMETER_GUIDE.md # suggest参数使用指南 ✨新增
│   ├── PROJECT_STRUCTURE.md     # 项目结构说明
│   └── frontend_upgrade.md      # 前端升级说明
└── README.md                    # 文档索引和快速导航
```

### 🧪 测试结构
```
tests/
├── unit/              # 单元测试 (32个测试)
├── integration/       # 集成测试 (11个测试)
├── e2e/              # 端到端测试
└── conftest.py       # 共享测试配置
```

### 📦 源代码组织
```
src/mcp_feedback_pipe/
├── server.py          # MCP工具定义 (120行)
├── app.py            # Flask Web应用 (114行)
├── server_manager.py # 服务器管理 (82行)
├── feedback_handler.py # 反馈处理 (62行)
├── utils.py          # 工具函数 (95行)
├── static/           # 前端资源
└── templates/        # HTML模板
```

## 🎯 使用指南

### 开发环境启动
```bash
# 1. 激活虚拟环境
source .venv/bin/activate

# 2. 启动服务
python scripts/start_server.py

# 3. 运行测试
python tests/integration/deploy_test.py
```

### SSH远程开发 (Windows → Linux)
```bash
# 1. 建立SSH隧道 (在Windows上)
ssh -L 5000:localhost:5000 username@your-server-ip

# 2. 启动服务 (在Linux服务器上)
python scripts/start_server.py

# 3. 访问Web界面 (在Windows浏览器)
http://localhost:5000
```

### 运行测试套件
```bash
# 运行所有测试
pytest tests/ -v

# 运行特定类型测试
pytest tests/unit/ -v         # 单元测试
pytest tests/integration/ -v  # 集成测试
pytest tests/e2e/ -v         # 端到端测试
```

## 📊 项目指标

### 代码组织
- **总模块数**: 8个专门模块
- **最大文件行数**: 120行 (符合<250行要求)
- **测试覆盖率**: 65%
- **测试用例数**: 43个

### 架构特点
- ✅ **关注点分离**: 每个模块职责单一
- ✅ **前后端分离**: HTML/CSS/JS独立
- ✅ **SSH兼容**: 完美支持远程开发
- ✅ **模块化**: 松耦合、高内聚

### 文件大小控制
| 文件 | 行数 | 状态 |
|------|------|------|
| `server.py` | 120 | ✅ |
| `app.py` | 114 | ✅ |
| `server_manager.py` | 82 | ✅ |
| `utils.py` | 95 | ✅ |
| `feedback_handler.py` | 62 | ✅ |

## 🔄 版本演进

### v2.0.0 → v3.0.0 重构
- **架构变更**: GUI → Web
- **环境适配**: SSH远程开发支持
- **代码组织**: 单文件 → 模块化
- **测试完善**: 43个测试用例
- **文档丰富**: 专门的文档目录

---

**更新时间**: 2025-05-31  
**项目版本**: v3.0.1  
**架构类型**: 模块化Web应用 