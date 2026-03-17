from __future__ import annotations

from pathlib import Path
from shutil import copy2
from typing import Any

from skills.analyzer_routing import analyze_document_for_skill
from skills.document_runtime import supported_presets
from skills.formatter_apply import format_document_with_preset_for_skill
from skills.punctuation_fix import fix_document_punctuation_for_skill


class DocxFormatterPipeline:
    """Mechanical DOCX pipeline built on top of existing skill wrappers."""

    @staticmethod
    def run(
        input_path: str,
        style: str,
        output_path: str | None = None,
    ) -> dict[str, Any]:
        source = DocxFormatterPipeline._validate_input_path(input_path)
        DocxFormatterPipeline._validate_style(style)
        final_target = DocxFormatterPipeline._normalize_output_path(
            input_path=input_path,
            output_path=output_path,
        )

        analysis_result = DocxFormatterPipeline.analyze_for_routing(str(source))
        current_path = str(source)
        steps = ["完成 analyzer_routing 分析"]
        executions: list[dict[str, Any]] = [
            {
                "tool_name": "analyzer_routing",
                "ok": True,
                "output_path": None,
                "summary": analysis_result.get("summary"),
            }
        ]

        punctuation_result: dict[str, Any] | None = None
        if DocxFormatterPipeline.should_run_punctuation_fix(analysis_result):
            punctuation_result = fix_document_punctuation_for_skill(current_path)
            executions.append(
                {
                    "tool_name": "punctuation_fix",
                    "ok": punctuation_result.get("success", False),
                    "output_path": punctuation_result.get("output_path"),
                    "summary": punctuation_result.get("message"),
                }
            )
            if not punctuation_result.get("success", False):
                return DocxFormatterPipeline._build_failure_result(
                    input_path=str(source),
                    style=style,
                    output_path=None,
                    analysis_result=analysis_result,
                    steps=steps,
                    executions=executions,
                    message=str(punctuation_result.get("message", "标点修复失败。")),
                )
            current_path = str(punctuation_result["output_path"])
            steps.append("完成 punctuation_fix")

        formatter_result = format_document_with_preset_for_skill(
            current_path,
            preset_name=style,
        )
        executions.append(
            {
                "tool_name": "formatter_apply",
                "ok": formatter_result.get("success", False),
                "output_path": formatter_result.get("output_path"),
                "summary": formatter_result.get("message"),
            }
        )
        if not formatter_result.get("success", False):
            return DocxFormatterPipeline._build_failure_result(
                input_path=str(source),
                style=style,
                output_path=None,
                analysis_result=analysis_result,
                steps=steps,
                executions=executions,
                message=str(formatter_result.get("message", "全文格式化失败。")),
            )

        steps.append("完成 formatter_apply")
        generated_output = str(formatter_result["output_path"])
        resolved_output = DocxFormatterPipeline._finalize_output_path(
            generated_output=generated_output,
            output_path=final_target,
        )
        steps.append("完成最终输出落盘")

        return {
            "success": True,
            "input_path": str(source),
            "style": style,
            "output_path": resolved_output,
            "analysis": analysis_result,
            "steps": steps,
            "executions": executions,
            "message": "DOCX 格式化流水线执行完成。",
        }

    @staticmethod
    def analyze_for_routing(input_path: str) -> dict[str, Any]:
        return analyze_document_for_skill(input_path)

    @staticmethod
    def should_run_punctuation_fix(analysis_result: dict[str, Any]) -> bool:
        issue_counts = analysis_result.get("issue_counts", {})
        punctuation_count = issue_counts.get("punctuation", 0)
        return bool(punctuation_count and punctuation_count > 0)

    @staticmethod
    def _validate_input_path(input_path: str) -> Path:
        source = Path(input_path).expanduser().resolve()
        if not source.exists():
            raise FileNotFoundError(f"输入文件不存在: {input_path}")
        if source.suffix.lower() != ".docx":
            raise ValueError("当前流水线只支持 .docx 文件")
        return source

    @staticmethod
    def _validate_style(style: str) -> None:
        presets = supported_presets()
        if style not in presets:
            raise ValueError(
                "暂不支持该 style。当前仅支持: " + ", ".join(sorted(presets))
            )

    @staticmethod
    def _normalize_output_path(
        *,
        input_path: str,
        output_path: str | None,
    ) -> Path | None:
        if output_path is None:
            return None

        source = Path(input_path).expanduser().resolve()
        target = Path(output_path).expanduser().resolve()
        if target == source:
            raise ValueError("output_path 不能与 input_path 相同")
        if target.suffix.lower() != ".docx":
            raise ValueError("output_path 必须是 .docx 文件路径")
        return target

    @staticmethod
    def _finalize_output_path(
        *,
        generated_output: str,
        output_path: Path | None,
    ) -> str:
        if output_path is None:
            return generated_output

        generated = Path(generated_output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        copy2(generated, output_path)
        return str(output_path)

    @staticmethod
    def _build_failure_result(
        *,
        input_path: str,
        style: str,
        output_path: str | None,
        analysis_result: dict[str, Any] | None,
        steps: list[str],
        executions: list[dict[str, Any]],
        message: str,
    ) -> dict[str, Any]:
        return {
            "success": False,
            "input_path": input_path,
            "style": style,
            "output_path": output_path,
            "analysis": analysis_result,
            "steps": steps,
            "executions": executions,
            "message": message,
        }
