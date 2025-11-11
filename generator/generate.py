import logging
import os
import pathlib

import jinja2
import pydantic
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
    data = Data.model_validate_json(
        pathlib.Path(pathlib.Path(__file__).parent, "events.json").read_bytes(),
    )

    layout = env.get_template("layout.jinja2")
    pathlib.Path("pocket_option", "generated_client.py").write_text(layout.render(data=data))

    os.system("poetry run ruff format pocket_option/generated_client.py --silent")  # noqa: S605, S607
    os.system(
        "poetry run ruff check pocket_option/generated_client.py --fix --unsafe-fixes --silent"
    )  # noqa: S605, S607


if __name__ == "__main__":
    generate()
