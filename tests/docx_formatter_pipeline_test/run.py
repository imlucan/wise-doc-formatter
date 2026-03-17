from __future__ import annotations

import argparse
import json
import sys
from importlib import import_module
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = PROJECT_ROOT / "src"
DEFAULT_STYLE = "official"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="运行 DocxFormatterPipeline 测试示例。"
    )
    parser.add_argument("-i", "--input_path", help="输入 DOCX 文件路径")
    parser.add_argument(
        "-s",
        "--style",
        default=DEFAULT_STYLE,
        help=f"格式风格，默认值为 {DEFAULT_STYLE}",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        dest="output_path",
        default=None,
        help="输出 DOCX 文件路径；不传时默认输出到输入文件所在目录",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    docx_formatter_pipeline = import_module("tools")
    pipeline_class = docx_formatter_pipeline.DocxFormatterPipeline
    source_path = Path(args.input_path).expanduser().resolve()

    if args.output_path:
        output_path = Path(args.output_path).expanduser().resolve()
    else:
        output_path = source_path.parent / f"{source_path.stem}-pipeline-output.docx"

    result = pipeline_class.run(
        input_path=str(source_path),
        style=args.style,
        output_path=str(output_path),
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
