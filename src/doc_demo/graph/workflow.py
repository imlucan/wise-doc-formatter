from __future__ import annotations

from langgraph.graph import END, StateGraph

from doc_demo.core.state import WorkflowState
from skills.document_runtime import (
    analyze_document,
    run_formatter,
    run_punctuation_fix,
    summarize_analysis,
    validate_input_path,
)


def analyze_node(state: WorkflowState) -> WorkflowState:
    validate_input_path(state["input_path"])
    analysis = analyze_document(state["input_path"])
    steps = list(state.get("steps", []))
    steps.append("完成文档分析")
    executions = list(state.get("executions", []))
    executions.append(
        {
            "tool_name": "analyze_document",
            "ok": True,
            "summary": summarize_analysis(analysis),
            "output_path": None,
        }
    )
    return {
        "analysis": analysis,
        "steps": steps,
        "executions": executions,
        "summary": f"分析完成：{summarize_analysis(analysis)}",
    }


def punctuation_node(state: WorkflowState) -> WorkflowState:
    output_path = run_punctuation_fix(state["input_path"])
    steps = list(state.get("steps", []))
    steps.append("完成标点修复")
    executions = list(state.get("executions", []))
    executions.append(
        {
            "tool_name": "fix_punctuation",
            "ok": True,
            "summary": "已生成标点修复结果文件",
            "output_path": output_path,
        }
    )
    return {
        "output_path": output_path,
        "steps": steps,
        "executions": executions,
        "summary": f"{state.get('summary', '')}\n已完成标点修复。",
    }


def format_node(state: WorkflowState) -> WorkflowState:
    output_path = run_formatter(
        state["input_path"],
        preset_name=state.get("preset_name", "official"),
    )
    steps = list(state.get("steps", []))
    steps.append("完成全文格式化")
    executions = list(state.get("executions", []))
    executions.append(
        {
            "tool_name": "format_document",
            "ok": True,
            "summary": f"已使用预设 {state.get('preset_name', 'official')} 生成格式化结果",
            "output_path": output_path,
        }
    )
    return {
        "output_path": output_path,
        "steps": steps,
        "executions": executions,
        "summary": f"{state.get('summary', '')}\n已完成全文格式化。",
    }


def route_after_analysis(state: WorkflowState) -> str:
    action = state.get("action", "analyze")
    if action == "fix_punctuation":
        return "punctuation"
    if action == "format_document":
        return "format"
    return "finish"


def build_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("analyze", analyze_node)
    graph.add_node("punctuation", punctuation_node)
    graph.add_node("format", format_node)
    graph.set_entry_point("analyze")
    graph.add_conditional_edges(
        "analyze",
        route_after_analysis,
        {
            "punctuation": "punctuation",
            "format": "format",
            "finish": END,
        },
    )
    graph.add_edge("punctuation", END)
    graph.add_edge("format", END)
    return graph.compile()


WORKFLOW_APP = build_workflow()
