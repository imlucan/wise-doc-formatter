from __future__ import annotations

from typing import Any

from skills.document_runtime import run_punctuation_fix, validate_input_path


def fix_document_punctuation_for_skill(input_path: str) -> dict[str, Any]:
    """Single punctuation-fix entry for file-based skill execution."""
    try:
        validate_input_path(input_path)
        output_path = run_punctuation_fix(input_path)
        return {
            "success": True,
            "input_path": input_path,
            "output_path": output_path,
            "message": "标点修复已完成。",
        }
    except Exception as exc:
        return {
            "success": False,
            "input_path": input_path,
            "output_path": None,
            "message": f"标点修复失败: {exc}",
        }
