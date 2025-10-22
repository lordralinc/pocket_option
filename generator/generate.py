import json
import logging
import os
import pathlib
import typing

from rich.logging import RichHandler

logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler()],
)


class OnMethod(typing.TypedDict):
    name: str
    event: str
    type: str
    custom_handler: typing.NotRequired[str]
    custom_handler_type: typing.NotRequired[str]


class EmitMethodArg(typing.TypedDict):
    name: str
    type: str
    default: typing.NotRequired[str]
    cast: typing.NotRequired[bool]


class EmitMethod(typing.TypedDict):
    name: str
    event: str
    callback: typing.NotRequired[str]
    args: typing.NotRequired[list[EmitMethodArg]]


class Data(typing.TypedDict):
    on: list[OnMethod]
    emit: list[EmitMethod]


START = """import typing
import asyncio

from pocket_option.client import BasePocketOptionClient

if typing.TYPE_CHECKING:
    from pocket_option import models
    from pocket_option.types import TypedEventListener, JsonValue

__all__ = ("PocketOptionClient",)

"""

ON_TEMPLATE = """
@typing.overload
def {name}(
    self,
    handler: None = None,
) -> "typing.Callable[[TypedEventListener[{type}]], None]": ...
@typing.overload
def {name}(
    self,
    handler: "TypedEventListener[{type}]",
) -> None: ...

def {name}(
    self,
    handler: "TypedEventListener[{type}] | None" = None,
) -> "None | typing.Callable[[TypedEventListener[{type}]], None]":
{handler}
"""


EMIT_TEMPLATE = """
async def {name}(
    {params}
) -> None:
    await self.emit({fn_content})
"""


def make_spacing(data: str | list[str], spacing: int = 4) -> str:
    if isinstance(data, str):
        content = data.split("\n")
    else:
        content = []
        for it in data:
            content.extend(it.split("\n"))
    for i in range(len(content)):
        content[i] = spacing * " " + content[i]
    return "\n".join(content)


def generate_on_method(method: OnMethod) -> str:
    if handler_path := method.get("custom_handler"):
        args = {**method, "type": method.get("custom_handler_type", method["type"])}
        handler = pathlib.Path(pathlib.Path(__file__).parent, handler_path).read_text() % args
    else:
        handler = 'return self.on("{event}", handler=handler)'.format(**method)

    return make_spacing(ON_TEMPLATE.format(**method, handler=make_spacing(handler, 4)), 4)


def generate_emit_method(method: EmitMethod) -> str:
    params = ["self"]

    for arg in method.get("args", []):
        argline = f'{arg["name"]}: "{arg["type"]}"'
        if default := arg.get("default"):
            argline += f" = {default}"
        params.append(argline)
    fn_content = ['"' + method["event"] + '"']
    if args := method.get("args", []):
        if len(args) == 1:
            if args[0].get("cast"):
                fn_content.append(f"""typing.cast("JsonValue", {args[0]["name"]})""")
            else:
                fn_content.append(args[0]["name"])
        else:
            fn_content.append("[" + ", ".join(arg["name"] for arg in args) + "]")

    if callback := method.get("callback"):
        params.append(f'callback: "EmitCallback[{callback}] | None" = None')
        fn_content.append("callback=callback")

    return make_spacing(
        EMIT_TEMPLATE.format(
            name=method["name"],
            params=", ".join(params),
            fn_content=", ".join(fn_content),
        ),
        4,
    )


def generate():
    data = typing.cast("Data", json.loads(pathlib.Path(pathlib.Path(__file__).parent, "events.json").read_bytes()))
    content = [START, "class PocketOptionClient(BasePocketOptionClient):"]
    content.extend([generate_on_method(it) for it in data["on"]])
    content.extend([generate_emit_method(it) for it in data["emit"]])
    pathlib.Path("pocket_option", "generated_client.py").write_text("\n".join(content))

    os.system("poetry run ruff format pocket_option/generated_client.py --silent")  # noqa: S605, S607
    os.system("poetry run ruff check pocket_option/generated_client.py --fix --unsafe-fixes --silent")  # noqa: S605, S607


if __name__ == "__main__":
    generate()
