from pathlib import Path
import sys

from dotenv import load_dotenv


def main() -> None:
    project_root = Path(__file__).resolve().parent
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))
    load_dotenv(project_root / ".env", override=False)

    from doc_demo.ui.gradio_app import launch_app

    launch_app()


if __name__ == "__main__":
    main()
