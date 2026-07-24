from __future__ import annotations

import logging
import pathlib
import subprocess

import jinja2
import pydantic
import yaml
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)


class OnMethod(pydantic.BaseModel):
    name: str
    event: str
    return_type: str
    doc: str | None = None
    pydantic_model: str | None = None


class EmitMethodArg(pydantic.BaseModel):
    name: str
    type: str
    doc: str | None = None
    default: str | None = None


class EmitMethod(pydantic.BaseModel):
    name: str
    event: str
    doc: str | None = None
    args: EmitMethodArg | None = None


class Data(pydantic.BaseModel):
    on: list[OnMethod]
    emit: list[EmitMethod]


env = jinja2.Environment(loader=jinja2.FileSystemLoader(pathlib.Path(__file__).parent), autoescape=False)  # noqa: S701


def generate():
    data = Data.model_validate(
        {
            "on": yaml.safe_load(
                pathlib.Path(pathlib.Path(__file__).parent, "on_events.yaml").read_text(encoding="utf-8"),
            ),
            "emit": yaml.safe_load(
                pathlib.Path(pathlib.Path(__file__).parent, "emit_events.yaml").read_text(encoding="utf-8"),
            ),
        },
    )

    layout = env.get_template("layout.jinja2")
    pathlib.Path("pocket_option", "generated_client.py").write_text(layout.render(data=data))

    subprocess.run(
        [  # noqa: S607
            "poetry",
            "run",
            "ruff",
            "format",
            "pocket_option/generated_client.py",
            "--silent",
        ],
        check=True,
    )
    subprocess.run(
        [  # noqa: S607
            "poetry",
            "run",
            "ruff",
            "check",
            "pocket_option/generated_client.py",
            "--fix",
            "--unsafe-fixes",
            "--silent",
        ],
        check=True,
    )


if __name__ == "__main__":
    generate()
