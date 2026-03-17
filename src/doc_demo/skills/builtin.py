from __future__ import annotations

from langchain_core.tools import BaseTool, StructuredTool

from skills.analyzer_routing import analyze_document_for_skill
from skills.formatter_apply import format_document_with_preset_for_skill
from skills.punctuation_fix import fix_document_punctuation_for_skill


def _analyze_document_skill(input_path: str) -> str:
    return analyze_document_for_skill(input_path)


def _fix_punctuation_skill(input_path: str) -> str:
    return fix_document_punctuation_for_skill(input_path)


def _format_document_skill(input_path: str, preset_name: str = "official") -> str:
    return format_document_with_preset_for_skill(input_path, preset_name=preset_name)


def build_document_analysis_skill() -> BaseTool:
    return StructuredTool.from_function(
        func=_analyze_document_skill,
        name="inspect_document_for_routing",
        description=(
            "分析 DOCX 文档中的标点、序号、段落和字体问题，"
            "返回摘要、问题计数、样例、推荐工具和下一步路由建议。"
        ),
    )


def build_document_punctuation_skill() -> BaseTool:
    return StructuredTool.from_function(
        func=_fix_punctuation_skill,
        name="fix_document_punctuation",
        description="修复 DOCX 文档中的中文标点问题，返回 success 和 output_path。",
    )


def build_document_formatter_skill() -> BaseTool:
    return StructuredTool.from_function(
        func=_format_document_skill,
        name="format_document_with_preset",
        description="按指定预设格式化 DOCX 文档，返回 success、output_path、preset_name 和 message。",
    )


def get_builtin_document_skills() -> list[BaseTool]:
    return [
        build_document_analysis_skill(),
        build_document_punctuation_skill(),
        build_document_formatter_skill(),
    ]
