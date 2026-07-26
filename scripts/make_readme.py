import pathlib

import yaml

readme_paths = (pathlib.Path("README.md"), pathlib.Path("README.ru.md"))
emit_path = pathlib.Path("generator", "emit_events.yaml")

START_EMIT = "<!-- START_AVAILABLE_EMIT_EVENTS -->"
END_EMIT = "<!-- END_AVAILABLE_EMIT_EVENTS -->"
START_ON = "<!-- START_AVAILABLE_ON_EVENTS -->"
END_ON = "<!-- END_AVAILABLE_ON_EVENTS -->"


def generate_events(data: list[dict], pre_tag: str) -> str:
    lines = [
        "| Method | Event |  Category  | Description |",
        "|--------|-------|:----------:|-------------|",
    ]

    for emit in data:
        lines.append(
            f"| `{pre_tag}.{emit['name']}` | `{emit['event']}` | {emit.get('category') or '-'} | {emit.get('doc') or '-'} |"
        )

    return "\n".join(lines)


def update_readme(path: pathlib.Path, data: list[dict], tags: tuple[str, str], pre_tag: str) -> None:
    text = path.read_text(encoding="utf-8")

    generated = generate_events(data, pre_tag=pre_tag)

    start = text.index(tags[0]) + len(tags[0])
    end = text.index(tags[1])

    text = text[:start] + "\n\n" + generated + "\n\n" + text[end:]

    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    emit_data = yaml.safe_load(emit_path.read_text())
    on_data = yaml.safe_load(emit_path.read_text())
    for path in readme_paths:
        update_readme(path, emit_data, (START_EMIT, END_EMIT), pre_tag="client.emit")
        update_readme(path, on_data, (START_ON, END_ON), pre_tag="client.on")
