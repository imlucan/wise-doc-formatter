from __future__ import annotations

from typing import Any

from skills import formatter_engine
from skills.document_runtime import run_formatter, validate_input_path


def format_document_with_preset_for_skill(
    input_path: str,
    preset_name: str = "official",
) -> dict[str, Any]:
    """Single black-box formatter entry for file-based skill execution."""
    try:
        validate_input_path(input_path)
        supported_presets = sorted(formatter_engine.PRESETS.keys())
        if preset_name not in formatter_engine.PRESETS:
            return {
                "success": False,
                "input_path": input_path,
                "output_path": None,
                "preset_name": preset_name,
                "message": (
                    "暂不支持该预设。当前仅支持: "
                    + ", ".join(supported_presets)
                ),
            }

        output_path = run_formatter(input_path, preset_name=preset_name)
        return {
            "success": True,
            "input_path": input_path,
            "output_path": output_path,
            "preset_name": preset_name,
            "message": "全文格式化已完成。",
        }
    except Exception as exc:
        return {
            "success": False,
            "input_path": input_path,
            "output_path": None,
            "preset_name": preset_name,
            "message": f"全文格式化失败: {exc}",
        }
