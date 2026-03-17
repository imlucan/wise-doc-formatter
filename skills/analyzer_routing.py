from __future__ import annotations

from typing import Any

from skills.document_runtime import (
    analyze_document,
    summarize_analysis,
    validate_input_path,
)


SKILL_ANALYSIS_SAMPLE_LIMIT = 5


def analyze_document_for_skill(input_path: str) -> dict[str, Any]:
    """Single high-signal analyzer entry for LLM routing."""
    validate_input_path(input_path)
    analysis = analyze_document(input_path)
    counts = {
        "punctuation": len(analysis.get("punctuation", [])),
        "numbering": len(analysis.get("numbering", [])),
        "paragraph": len(analysis.get("paragraph", [])),
        "font": len(analysis.get("font", [])),
    }
    total_issues = sum(counts.values())

    recommended_tools: list[dict[str, str]] = []
    if counts["punctuation"] > 0:
        recommended_tools.append(
            {
                "tool_name": "fix_document_punctuation",
                "reason": "检测到标点问题，建议先进行低风险标点修复。",
            }
        )
    if counts["paragraph"] > 0 or counts["font"] > 0:
        recommended_tools.append(
            {
                "tool_name": "format_document_with_preset",
                "reason": "检测到段落或字体问题，建议执行全文格式化。",
            }
        )
    if counts["numbering"] > 0 and not recommended_tools:
        recommended_tools.append(
            {
                "tool_name": "inspect_document_for_routing",
                "reason": "检测到序号风格问题，建议先人工确认后再决定修复策略。",
            }
        )

    if total_issues == 0:
        routing_hint = "no_action_needed"
    elif counts["paragraph"] > 0 or counts["font"] > 0:
        routing_hint = "format_document"
    elif counts["punctuation"] > 0:
        routing_hint = "fix_punctuation"
    else:
        routing_hint = "review_manually"

    return {
        "input_path": input_path,
        "summary": summarize_analysis(analysis),
        "issue_counts": {
            **counts,
            "total": total_issues,
        },
        "routing_hint": routing_hint,
        "recommended_tools": recommended_tools,
        "samples": {
            "punctuation": analysis.get("punctuation", [])[:SKILL_ANALYSIS_SAMPLE_LIMIT],
            "numbering": analysis.get("numbering", [])[:SKILL_ANALYSIS_SAMPLE_LIMIT],
            "paragraph": analysis.get("paragraph", [])[:SKILL_ANALYSIS_SAMPLE_LIMIT],
            "font": analysis.get("font", [])[:SKILL_ANALYSIS_SAMPLE_LIMIT],
        },
        "raw_analysis": analysis,
    }
