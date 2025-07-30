import json
import os
import tempfile
from pathlib import Path
from .cli import run


def write_file(content: str):
    temp_file = tempfile.NamedTemporaryFile("w")
    temp_file.write(content)
    temp_file.flush()
    return temp_file


def poml(
    markup: str | Path, context: dict | str | Path | None = None, stylesheet: dict | str | Path | None = None,
    chat: bool = True
) -> list | dict | str:
    temp_input_file = temp_context_file = temp_stylesheet_file = None
    try:
        if isinstance(markup, Path):
            if not markup.exists():
                raise FileNotFoundError(f"File not found: {markup}")
        else:
            if os.path.exists(markup):
                markup = Path(markup)
            else:
                temp_input_file = write_file(markup)
                markup = Path(temp_input_file.name)
        with tempfile.NamedTemporaryFile("r") as output_file:
            args = ["-f", str(markup), "-o", output_file.name]
            if isinstance(context, dict):
                temp_context_file = write_file(json.dumps(context))
                args.extend(["--context-file", temp_context_file.name])
            elif context:
                if os.path.exists(context):
                    args.extend(["--context-file", str(context)])
                else:
                    raise FileNotFoundError(f"File not found: {context}")

            if isinstance(stylesheet, dict):
                temp_stylesheet_file = write_file(json.dumps(stylesheet))
                args.extend(["--stylesheet-file", temp_stylesheet_file.name])
            elif stylesheet:
                if os.path.exists(stylesheet):
                    args.extend(["--stylesheet-file", str(stylesheet)])
                else:
                    raise FileNotFoundError(f"File not found: {stylesheet}")
            
            if chat:
                args.extend(["--chat", "true"])
            else:
                args.extend(["--chat", "false"])

            run(*args)
            output = output_file.read()
            return json.loads(output)
    finally:
        if temp_input_file:
            temp_input_file.close()
        if temp_context_file:
            temp_context_file.close()
        if temp_stylesheet_file:
            temp_stylesheet_file.close()
