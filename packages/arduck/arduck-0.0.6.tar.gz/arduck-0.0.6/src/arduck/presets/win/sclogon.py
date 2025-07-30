"""Preset that schedules a program to run at logon."""

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


from argparse import ArgumentParser

from ...parsers import ScLogonArgumentParser
from ...tokenizer import RawKeystroke


PARSER: ArgumentParser = ScLogonArgumentParser()


def apply(raw_keystrokes: list[list[RawKeystroke]]) -> list[list[RawKeystroke]]:
    """Applies the preset to the given list of keystrokes."""

    parser = ScLogonArgumentParser()

    namespace = parser.parse_args(tuple(map(lambda a: ''.join(a), raw_keystrokes)))

    return [
        [('KEY_LEFT_GUI', 'r')], [500],
        list('taskschd.msc\n'), [2000],
        [('KEY_LEFT_ALT', 'a'), 'r'], [200],
        [('KEY_LEFT_ALT', 'e')], [200],
        [('KEY_LEFT_ALT', 'd')], [200],
        list(namespace.description) if namespace.description else [], [200],
        [('KEY_LEFT_ALT', 'm')], [200],
        list(namespace.name), [200],
        [('KEY_LEFT_SHIFT', 'KEY_TAB')], [200],
        ['KEY_RIGHT_ARROW'], [200],
        [('KEY_LEFT_ALT', 'n')], [200],
        ['KEY_RIGHT_ARROW'], [200],
        ['KEY_RETURN'], [200],
        ['KEY_RIGHT_ARROW'], [200],
        [('KEY_LEFT_ALT', 'n')], [200],
        [('KEY_LEFT_ALT', 'p')], [200],
        list(str(namespace.program)), [200],
        [('KEY_LEFT_ALT', 'a')], [200],
        ['KEY_RETURN'], [200],
        ['KEY_RIGHT_ARROW'], [200],
        [('KEY_LEFT_ALT', 'b', 'p')], [200],
        ['KEY_TAB'], [50],
        ['KEY_TAB'], [50],
        ['KEY_TAB'], [50],
        ['KEY_TAB'], [50],
        ['KEY_TAB'], [200],
        ['KEY_RIGHT_ARROW'], [200],
        ['KEY_TAB'], [50],
        ['KEY_TAB'], [50],
        ['KEY_TAB'], [50],
        ['KEY_TAB'], [50],
        [' '], [50],
        ['KEY_TAB'], [50],
        [' '], [200],
        ['KEY_RETURN'], [500],
        # ['KEY_TAB', ('KEY_LEFT_ALT', 'a'), 'r'],
        [500], [('KEY_LEFT_ALT', 'f'), 'x'],
    ]
