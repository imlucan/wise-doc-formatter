from __future__ import annotations

from datetime import datetime
from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = PROJECT_ROOT / "output"
ARTIFACTS_DIR = OUTPUT_DIR / "artifacts"
TEMP_DIR = OUTPUT_DIR / "temp"


def ensure_output_dirs() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)


def build_output_path(input_path: str, suffix: str) -> Path:
    ensure_output_dirs()
    source = Path(input_path)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    stem = source.stem
    extension = source.suffix or ".docx"
    return ARTIFACTS_DIR / f"{stem}-{suffix}-{timestamp}{extension}"


def build_temp_path(
    *,
    prefix: str,
    extension: str = ".tmp",
    keep_extension_dot: bool = True,
) -> Path:
    ensure_output_dirs()
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    unique_suffix = uuid4().hex[:8]
    normalized_extension = extension if keep_extension_dot or extension.startswith(".") else f".{extension}"
    return TEMP_DIR / f"{prefix}-{timestamp}-{unique_suffix}{normalized_extension}"
