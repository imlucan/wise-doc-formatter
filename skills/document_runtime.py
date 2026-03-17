from __future__ import annotations

from pathlib import Path
from typing import Any

from docx import Document

from skills import analyzer_engine, formatter_engine, punctuation_engine

from doc_demo.utils.paths import build_output_path


def validate_input_path(input_path: str) -> Path:
    source = Path(input_path)
    if not source.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_path}")
    if source.suffix.lower() != ".docx":
        raise ValueError("当前原型只支持 .docx 文件")
    return source


def analyze_document(input_path: str) -> dict[str, Any]:
    doc = Document(input_path)
    return {
        "punctuation": analyzer_engine.analyze_punctuation(doc),
        "numbering": analyzer_engine.analyze_numbering(doc),
        "paragraph": analyzer_engine.analyze_paragraph_format(doc),
        "font": analyzer_engine.analyze_font(doc),
    }


def summarize_analysis(analysis: dict[str, Any]) -> str:
    counts = {
        "标点问题": len(analysis.get("punctuation", [])),
        "序号问题": len(analysis.get("numbering", [])),
        "段落问题": len(analysis.get("paragraph", [])),
        "字体问题": len(analysis.get("font", [])),
    }
    parts = [f"{name} {count} 项" for name, count in counts.items()]
    return "，".join(parts)


def run_punctuation_fix(input_path: str) -> str:
    output_path = build_output_path(input_path, "punctuation-fixed")
    punctuation_engine.process_document(input_path, str(output_path))
    return str(output_path)


def run_formatter(
    input_path: str,
    preset_name: str = "official",
) -> str:
    output_path = build_output_path(input_path, "formatted")
    formatter_engine.format_document(
        input_path,
        str(output_path),
        preset_name=preset_name,
    )
    return str(output_path)


def supported_presets() -> list[str]:
    presets = list(formatter_engine.PRESETS.keys())
    return presets
