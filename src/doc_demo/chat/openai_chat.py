from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_openai import ChatOpenAI


MessageLike = BaseMessage | tuple[str, str]


@dataclass(slots=True)
class ChatResult:
    content: str
    messages: list[BaseMessage]
    tool_calls: list[dict[str, Any]]


class OpenAIChatService:
    """Simple OpenAI-compatible chat wrapper with injectable skills."""

    def __init__(
        self,
        *,
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        temperature: float = 0.2,
        max_tool_rounds: int = 3,
        skills: list[BaseTool] | None = None,
    ) -> None:
        resolved_api_key = api_key or os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
        if not resolved_api_key:
            raise ValueError("缺少 LLM_API_KEY，无法初始化 OpenAIChatService")

        llm_kwargs: dict[str, Any] = {
            "model": model or os.getenv("LLM_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            "api_key": resolved_api_key,
            "temperature": temperature,
        }
        resolved_base_url = base_url or os.getenv("LLM_BASE_URL") or os.getenv("OPENAI_BASE_URL")
        if resolved_base_url:
            llm_kwargs["base_url"] = resolved_base_url

        self.llm = ChatOpenAI(**llm_kwargs)
        self.max_tool_rounds = max_tool_rounds
        self.skills = list(skills or [])

    def chat(
        self,
        user_message: str,
        *,
        system_prompt: str | None = None,
        conversation: list[MessageLike] | None = None,
        skills: list[BaseTool] | None = None,
    ) -> ChatResult:
        active_skills = [*self.skills, *(skills or [])]
        tools_by_name = {tool.name: tool for tool in active_skills}
        messages = self._normalize_messages(conversation or [])

        if system_prompt:
            messages.insert(0, SystemMessage(content=system_prompt))
        messages.append(HumanMessage(content=user_message))

        runnable = self.llm.bind_tools(active_skills) if active_skills else self.llm
        tool_calls: list[dict[str, Any]] = []

        for _ in range(self.max_tool_rounds + 1):
            response = runnable.invoke(messages)
            messages.append(response)

            if not isinstance(response, AIMessage) or not response.tool_calls:
                return ChatResult(
                    content=self._render_content(response.content),
                    messages=messages,
                    tool_calls=tool_calls,
                )

            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})
                tool = tools_by_name.get(tool_name)
                if tool is None:
                    tool_output = json.dumps(
                        {"error": f"未找到名为 {tool_name} 的 skill"},
                        ensure_ascii=False,
                    )
                else:
                    tool_output = self._coerce_tool_output(tool.invoke(tool_args))

                tool_calls.append(
                    {
                        "name": tool_name,
                        "args": tool_args,
                        "output": tool_output,
                    }
                )
                messages.append(
                    ToolMessage(
                        content=tool_output,
                        tool_call_id=tool_call["id"],
                        name=tool_name,
                    )
                )

        return ChatResult(
            content="工具调用达到上限，已停止继续执行。",
            messages=messages,
            tool_calls=tool_calls,
        )

    @staticmethod
    def _normalize_messages(conversation: list[MessageLike]) -> list[BaseMessage]:
        normalized: list[BaseMessage] = []
        for item in conversation:
            if isinstance(item, BaseMessage):
                normalized.append(item)
                continue

            role, content = item
            if role == "system":
                normalized.append(SystemMessage(content=content))
            elif role == "assistant":
                normalized.append(AIMessage(content=content))
            else:
                normalized.append(HumanMessage(content=content))
        return normalized

    @staticmethod
    def _coerce_tool_output(output: Any) -> str:
        if isinstance(output, str):
            return output
        try:
            return json.dumps(output, ensure_ascii=False, indent=2)
        except TypeError:
            return str(output)

    @staticmethod
    def _render_content(content: Any) -> str:
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts: list[str] = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(str(item.get("text", "")))
                else:
                    parts.append(str(item))
            return "\n".join(part for part in parts if part)
        return str(content)


LLMChatService = OpenAIChatService
