"""Contains argument types used by preset argument parsers."""

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


from argparse import ArgumentTypeError


def sc_task_name(argument: str) -> str:
    """The name of a Windows scheduled task."""

    forbidden_characters: tuple[str, ...] = ('\\', '/', ':', '*', '?', '<', '>', '|')

    if any(c in argument for c in forbidden_characters):
        raise ArgumentTypeError(f'task name contains forbidden characters {forbidden_characters}')

    return argument