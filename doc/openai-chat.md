# OpenAI 风格 LLM Chat 与 Skill 注入

## 目标

当前项目已补充一个最小可用的 OpenAI 风格兼容聊天封装，用于后续 skill 开发与工具调用实验。

## 代码位置

- 聊天服务：`src/doc_demo/chat/openai_chat.py`
- 内置 skill：`src/doc_demo/skills/builtin.py`

## 当前能力

`OpenAIChatService` 与别名 `LLMChatService` 支持：

- 优先通过 `LLM_API_KEY` 初始化模型调用
- 可选读取 `LLM_MODEL`
- 可选读取 `LLM_BASE_URL`，兼容 OpenAI 风格接口
- 在一次聊天中动态注入 skill
- 自动处理模型返回的 tool call，并将 tool 结果回填给模型

为避免旧配置失效，代码目前仍兼容读取旧的 `OPENAI_*` 变量，但新配置统一推荐使用 `LLM_*` 前缀。

## Skill 注入方式

当前封装兼容 `LangChain BaseTool`，因此可以：

- 直接注入现成的 `BaseTool`
- 用 `StructuredTool.from_function(...)` 包装自己的 skill
- 使用内置文档 skill：`get_builtin_document_skills()`

当前 analyzer 默认以单一 skill `inspect_document_for_routing` 暴露，专门用于决定下一步该调用哪个工具。
当前 punctuation 默认以单一 skill `fix_document_punctuation` 暴露，专门返回处理结果与输出文件路径。
当前 formatter 默认以单一 skill `format_document_with_preset` 暴露，专门返回 success、output_path、preset_name 和 message。

## 最小示例

```python
from doc_demo.chat import LLMChatService
from doc_demo.skills import get_builtin_document_skills

service = LLMChatService(skills=get_builtin_document_skills())
result = service.chat(
    "请分析这个文档的问题",
    system_prompt="你是一个文档处理助手。",
)

print(result.content)
print(result.tool_calls)
```

## 环境变量

建议本地配置：

- `LLM_API_KEY`
- `LLM_MODEL`
- `LLM_BASE_URL`

项目根目录提供了 `.env.example` 作为样例。

## 当前边界

- 目前只实现了同步 `chat` 方法
- 还没有接到 Gradio 界面
- 还没有做多轮会话持久化
- 还没有把 skill 调度纳入 LangGraph 节点

## 后续建议

1. 将 chat 能力接入单独的 Gradio 页签。
2. 将内置文档 skill 与 LangGraph 工作流打通。
3. 为自定义 skill 增加注册表或配置化加载机制。
