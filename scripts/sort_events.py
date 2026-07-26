import pathlib

import yaml

ORDER = ("name", "event", "category", "doc")
SORT_FILES = (
    (pathlib.Path("generator", "emit_events.yaml"), ("category", "name")),
    (pathlib.Path("generator", "on_events.yaml"), ("category", "name")),
)


for file, keys in SORT_FILES:
    content = yaml.safe_load(file.read_text())
    content.sort(key=lambda x: tuple(x.get(it, "") for it in keys))
    content = [
        {
            **{k: item[k] for k in ORDER if k in item},
            **{k: v for k, v in item.items() if k not in ORDER},
        }
        for item in content
    ]

    text = yaml.safe_dump(
        content,
        sort_keys=False,
        allow_unicode=True,
    )
    text = text.replace("\n- ", "\n\n- ")
    if text.startswith("\n"):
        text = text[1:]

    file.write_text(text)
