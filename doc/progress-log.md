# 初始化进度记录

## 2026-03-17

### 已完成

- 确认仓库已由 `uv init` 初始化，但 `pyproject.toml` 依赖仍为空。
- 确认现有 `scripts/` 主要依赖 `python-docx`。
- 设计单进程 `LangGraph + Gradio` 原型目录。
- 建立 `doc/` 文档体系初稿。
- 建立 `src/doc_demo/` 基础骨架。
- 使用 `uv add` 安装 `python-docx`、`langgraph`、`gradio`、`pydantic`、`python-dotenv`。
- 追加安装 `langchain`，为后续 skill 和 LLM 接入做准备。
- 追加安装 `langchain-openai`，并补充 OpenAI 兼容聊天封装。
- 建立 `LangGraph` 工作流与 `Gradio` 页面入口。
- 完成 `analyzer`、`punctuation`、`formatter` 三个首批工具包装。
- 完成分析、标点修复、全文格式化的冒烟测试。
- `analyzer` 与 `punctuation` 已开始拆分为独立 `skills/` 实现层与注入适配层。
- `formatter` 已开始拆分为独立 `skills/` 实现层与注入适配层。

### 产物

- 包入口：`src/doc_demo/`
- 聊天入口代码：`src/doc_demo/chat/`
- 内置 skill 代码：`src/doc_demo/skills/`
- 启动入口：`main.py`
- 运行时输出：`output/artifacts/`
- 运行时临时目录：`output/temp/`
- 依赖锁文件：`uv.lock`

### 后续同步要求

- 每次新增依赖时更新 `doc/dependency-analysis.md`。
- 每次新增或调整 tool 时更新 `doc/tool-catalog.md`。
- 每次结构调整时更新 `doc/architecture.md`。
