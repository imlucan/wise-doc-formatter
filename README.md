# doc-demo

基于现有 `python-docx` 脚本封装的单进程 `LangGraph + Gradio` 原型。

## 当前能力

- 文档分析
- 标点修复
- 全文格式化
- OpenAI 兼容聊天封装
- 可注入 LangChain skill
- analyzer 已提供单一高信息入口，用于后续工具路由
- skill 实现开始独立沉淀到 `skills/` 目录
- punctuation 已提供单一文件处理入口，返回 success 和 output_path
- formatter 已提供黑盒文件处理入口，返回 success、output_path、preset_name 和 message
- 文档处理实现统一归属到 `skills/`，不再放在 `tools/`
- formatter 的 `preset_name` 当前推荐由界面或上层参数显式传入

## LLM Chat 准备

复制 `.env.example` 为 `.env` 后，填入至少：

```powershell
LLM_API_KEY=your_llm_api_key
LLM_MODEL=gpt-4o-mini
```

如果你使用 OpenAI 风格的兼容网关，也可以配置：

```powershell
LLM_BASE_URL=https://your-openai-compatible-endpoint/v1
```

## 运行方式

```powershell
uv sync
uv run python .\main.py
```

或：

```powershell
uv run python -m doc_demo
```

## 文件输出约定

当前项目把文件作为 agent/skill 的主要处理对象：

- 最终或阶段性结果：`output/artifacts/`
- 处理中间临时文件：`output/temp/`

## 文档

- `doc/architecture.md`
- `doc/dependency-analysis.md`
- `doc/analyzer-skill.md`
- `doc/formatter-boundary.md`
- `doc/openai-chat.md`
- `doc/tool-catalog.md`
- `doc/skill-migration-plan.md`
- `doc/progress-log.md`
