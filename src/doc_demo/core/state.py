from typing import Any, Literal, TypedDict


WorkflowAction = Literal["analyze", "fix_punctuation", "format_document"]


class ToolExecution(TypedDict):
    tool_name: str
    ok: bool
    summary: str
    output_path: str | None


class WorkflowState(TypedDict, total=False):
    input_path: str
    action: WorkflowAction
    preset_name: str
    analysis: dict[str, Any]
    output_path: str | None
    summary: str
    steps: list[str]
    executions: list[ToolExecution]
