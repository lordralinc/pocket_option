import re
from pathlib import Path


def make_id(name: str) -> str:
    return name.lower().replace("/", "-")


row_pattern = re.compile(r"^\|(?P<client>.*?)\|(?P<event>\s*`([^`]+)`\s*)\|(?P<impl>.*?)\|(?P<blink>.*?)\|$")


path = Path("reverse", "on_events.md")


lines: list[str] = []

for line in path.read_text(encoding="utf-8").splitlines():
    m = row_pattern.match(line)
    if not m:
        lines.append(line)
        continue

    event = m.group(3)

    if event == "Event name":
        lines.append(line)
        continue

    anchor = make_id(event)

    lines.append(f"|{m.group('client')}|{m.group('event')}|{m.group('impl')}| [🔗](#{anchor}) |")

path.write_text("\n".join(lines), encoding="utf-8")
