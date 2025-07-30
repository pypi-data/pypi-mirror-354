"""Allows easy access to payload presets."""

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


from importlib import import_module, resources
from pathlib import Path, PurePath
import shutil
from typing import Protocol

from ..modules import metadata


PRESETS_DIRECTORY: Path = Path(
    str(resources.files(metadata.package()) / 'presets')
)


class Preset(Protocol):
    """A sample preset."""

    def apply(self, raw_keystrokes: list[str]) -> list[str]: ...


def add(path: Path) -> None:
    """Adds a new preset to the package collection.

    Args:
        path:
            the preset's path.
    """

    shutil.copy(path, PRESETS_DIRECTORY)


def enum() -> list[str]:
    """Lists all available presets."""

    available_presets = (
        PurePath(root / file).relative_to(PRESETS_DIRECTORY)
        for root, _dirs, files in PRESETS_DIRECTORY.walk() for file in files
        if not any(map(lambda p: p.startswith('_'), (root / file).parts))
    )

    return [
        preset_path.parent.as_posix() if preset_path.stem == 'init'
        else preset_path.as_posix().split('.', maxsplit=1)[0]
        for preset_path in available_presets
    ]


def get(name: str) -> Preset:
    """Loads preset by name.

    Args:
        name:
            the name of the preset.
    """

    module_path: Path = PRESETS_DIRECTORY / Path('.'.join((name, 'py')))

    module_rel_path = module_path \
        .relative_to(PRESETS_DIRECTORY.parent) \
        .as_posix() \
        .rsplit('.', maxsplit=1)[0] \
        .replace('/', '.')

    return import_module('.' + module_rel_path, metadata.package())


def remove(name: str) -> None:
    """Removes preset from the package's collection.

    Args:
        name:
            the name of the preset to remove.
    """

    (PRESETS_DIRECTORY / name).unlink()
