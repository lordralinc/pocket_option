import re
from pathlib import Path


def make_id(name: str) -> str:
    """Generate anchor id from event name."""
    return name.lower().replace("/", "-").replace(" ", "-")


pattern = re.compile(r"^##\s+`([^`]+)`\s*$", re.MULTILINE)


def replace(match: re.Match[str]) -> str:
    event = match.group(1)
    return f'<h2 id="{make_id(event)}"><code>{event}</code></h2>'


path = Path("reverse", "on_events.md")

text = path.read_text(encoding="utf-8")
text = pattern.sub(replace, text)
path.write_text(text, encoding="utf-8")
