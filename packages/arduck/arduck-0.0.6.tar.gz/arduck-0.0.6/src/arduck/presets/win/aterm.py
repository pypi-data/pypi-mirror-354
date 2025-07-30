"""Preset that opens an admin terminal window.

This preset tries to accept the UAC prompt that usually pops up when running programs that required Admin privileges.
"""

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


from ...tokenizer import RawKeystroke


def apply(raw_keystrokes: list[list[RawKeystroke]]) -> list[list[RawKeystroke]]:
    """Applies the preset to the given list of keystrokes."""

    return [['KEY_LEFT_GUI', 'x'], [500], 'a', [500], 'KEY_LEFT_ARROW', [300], '\n', [2000]] + raw_keystrokes
