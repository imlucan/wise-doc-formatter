from pathlib import Path

from dotenv import load_dotenv

from doc_demo.ui.gradio_app import launch_app


def main() -> None:
    load_dotenv(Path.cwd() / ".env", override=False)
    launch_app()


if __name__ == "__main__":
    main()
