# 依赖分析

## 现有脚本依赖

当前 `scripts/` 的实际依赖非常集中：

- 标准库：`re`、`sys`、`json`、`logging`、`pathlib`、`collections`
- 第三方：`python-docx`

这意味着仓库此前更偏“本地脚本工具箱”，尚未引入应用层、编排层或界面层依赖。

## 本次新增依赖

为支持单进程 `LangGraph + Gradio` 原型，推荐安装以下依赖：

- `python-docx`
  - 保留现有脚本能力运行基础。
- `langgraph`
  - 用于定义分析和处理工作流。
- `langchain`
  - 为后续 skill、LLM 接入、prompt 组织与 tool 抽象提供统一上层接口。
- `langchain-openai`
  - 提供 OpenAI 兼容模型接入层，便于后续构建可对话的 skill 调用入口。
- `gradio`
  - 提供浏览器可用的轻量界面。
- `pydantic`
  - 预留给后续状态模型、配置校验和接口数据结构。
- `python-dotenv`
  - 为后续模型供应商密钥或运行配置做环境变量加载准备。

以上依赖已通过 `uv add` 写入项目配置，并生成 `uv.lock`。

当前项目已经安装 `langchain-openai`，并提供了一个最小聊天封装；但默认仍未把聊天入口接入现有 Gradio 页面，因此仓库当前仍以工作流编排和本地工具调用为主。

## 传递依赖说明

虽然项目没有显式添加服务化框架，但 `gradio` 会自动引入若干传递依赖，例如：

- `fastapi`
- `starlette`
- `uvicorn`
- `httpx`

这属于 UI 框架运行时依赖，不代表项目已经切换为独立后端服务架构。

## 暂不显式预装的依赖

第一版原型刻意不引入以下依赖，避免过早服务化：

- `langgraph-sdk`
- 各类模型供应商 SDK

这些依赖应在明确接入具体 LLM 或拆分前后端后再补充。

## 为后续 skill 开发准备

安装 `langchain` 后，仓库已经具备继续补充以下能力的基础：

- `prompt template` 组织
- LLM 调用适配层
- 基于 LangChain tool 约定包装现有 `scripts`
- 后续与 `LangGraph` 做更自然的节点集成

下一步真正要实现“可对话/可推理”时，仍需按模型供应商补装对应包，例如：

- `langchain-openai`
- `langchain-google-genai`
- `langchain-anthropic`

## Python 版本

当前项目基于 `.python-version` 使用 `3.13`。如后续遇到个别生态包兼容问题，可考虑回退到 `3.12`，但第一版先保持现状。

## 风险与注意事项

- `gradio` 和 `langgraph` 会显著增加锁文件和虚拟环境体积。
- 当前工作流未接入 LLM，因此 `LangGraph` 主要承担编排职责，而不是 Agent 推理职责。
- 当前新增的 OpenAI 风格聊天能力优先依赖本地 `LLM_API_KEY`，未配置密钥时不会实际发起模型调用。
- 现有 `scripts/formatter.py` 仍是大一统逻辑，后续拆分时要同步更新本文件。
