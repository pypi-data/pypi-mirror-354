"""Allows easy access to payload templates."""

# Copyright (C) 2025  Stefano Cuizza

#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.


from importlib import resources
from pathlib import Path, PurePath
import shutil
from typing import Literal, TypedDict

from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

from ..modules import metadata
from ..tokenizer import Keystroke, SleepInterval


TEMPLATES_DIRECTORY: Path = Path(
    str(resources.files(metadata.package()) / 'templates')
)
ENVIRONMENT = Environment(
    loader=FileSystemLoader(TEMPLATES_DIRECTORY)
)


def btoi_filter(byte: bytes) -> int:
    """"""

    return int.from_bytes(byte)


def encode_filter(value: str, encoding: str) -> bytes:
    """"""

    return value.encode(encoding)


ENVIRONMENT.filters['btoi'] = btoi_filter
ENVIRONMENT.filters['encode'] = encode_filter


class TemplateParameters(TypedDict):
    """Parameters accepted by init template."""

    do_repeat: Literal[False] | int
    interval_mapping: list[tuple[int, SleepInterval]]
    keyboard_layout: str
    keystrokes: list[Keystroke]
    wpm: int


def add(path: Path) -> None:
    """Adds template to the package collection.

    Args:
        path:
            the template's path.
    """

    shutil.copy(path, TEMPLATES_DIRECTORY)


def enum() -> list[str]:
    """Lists all available templates."""

    available_templates = (
        PurePath(template) for template in ENVIRONMENT.list_templates()
        if not any(map(lambda s: s.startswith('_'), template.split('/')))
    )

    return [
        template_path.parent.as_posix() if template_path.stem == 'init'
        else template_path.as_posix().split('.', maxsplit=1)[0]
        for template_path in available_templates
    ]


def get(name: str) -> Template:
    """Loads template by name.

    Args:
        name:
            the name of the template.
    """

    try:
        template = ENVIRONMENT.get_template('/'.join((name, 'init')))
    except TemplateNotFound:
        return ENVIRONMENT.get_template(name)

    return template


def remove(name: str) -> None:
    """Removes template from the package's collection.

    Args:
        name:
            the name of the template to remove.
    """

    (TEMPLATES_DIRECTORY / name).unlink()
