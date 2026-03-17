from __future__ import annotations

import json
from typing import Any

import gradio as gr

from skills.document_runtime import supported_presets

from doc_demo.graph.workflow import WORKFLOW_APP


ACTION_LABELS = {
    "analyze": "仅分析",
    "fix_punctuation": "标点修复",
    "format_document": "全文格式化",
}


def _pretty_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2)


def run_workflow(file_path: str | None, action: str, preset_name: str) -> tuple[str, str, str | None]:
    if not file_path:
        raise gr.Error("请先上传 .docx 文件")

    result = WORKFLOW_APP.invoke(
        {
            "input_path": file_path,
            "action": action,
            "preset_name": preset_name,
            "steps": [],
            "executions": [],
        }
    )
    summary_lines = [result.get("summary", "处理完成。")]
    steps = result.get("steps", [])
    if steps:
        summary_lines.append("")
        summary_lines.append("执行步骤：")
        summary_lines.extend(f"- {step}" for step in steps)

    analysis = result.get("analysis", {})
    return "\n".join(summary_lines), _pretty_json(analysis), result.get("output_path")


def build_demo() -> gr.Blocks:
    presets = supported_presets()
    with gr.Blocks(title="Doc Demo Graph") as demo:
        gr.Markdown(
            """
            # Doc Demo Graph
            这是一个单进程 `LangGraph + Gradio` 原型，用于调度现有 `scripts/` 中的文档处理能力。
            """
        )
        with gr.Row():
            input_file = gr.File(label="上传 DOCX", file_types=[".docx"], type="filepath")
            output_file = gr.File(label="处理结果", interactive=False)
        with gr.Row():
            action = gr.Radio(
                choices=[(label, value) for value, label in ACTION_LABELS.items()],
                value="analyze",
                label="处理动作",
            )
            preset = gr.Dropdown(
                choices=presets,
                value=presets[0],
                label="格式化预设",
            )
        submit = gr.Button("运行工作流", variant="primary")
        summary = gr.Textbox(label="执行摘要", lines=8)
        analysis_json = gr.Code(label="分析结果 JSON", language="json")

        submit.click(
            fn=run_workflow,
            inputs=[input_file, action, preset],
            outputs=[summary, analysis_json, output_file],
        )
    return demo


def launch_app() -> None:
    demo = build_demo()
    demo.launch()
