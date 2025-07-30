"""Argument parser for the `sclogon` preset."""

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


from argparse import (
    ArgumentParser, Namespace,
)
from collections.abc import Sequence
import logging
from pathlib import PureWindowsPath
from random import choices, randint
from string import ascii_letters, digits
from typing import Optional, override

from arduck.parsers.presets import PresetArgumentParser, types

logger = logging.getLogger(__name__)


def _construct() -> ArgumentParser:
    """Returns an instance of the module's argument parser.

    Invoked by the `argparse` directive in the docs.
    For more information, see https://sphinx-argparse.readthedocs.io/en/stable.
    """

    return ScLogonArgumentParser()


class ScLogonArgumentParser(PresetArgumentParser):
    """ArgumentParser for the `sclogon` preset."""

    @override
    def __init__(self):
        super().__init__(
            prog='sclogon',
            description='schedule task to run on logon with Task Scheduler',
            prefix_chars='-',
        )

    def _extend_arguments(self) -> None:
        default_task_name: str = ''.join(choices(ascii_letters + digits, k=randint(8, 16)))

        self.add_argument(
            'program',
            action='store',
            help='program to execute at log on',
            type=PureWindowsPath,
        )

        self.add_argument(
            '-n', '--name',
            action='store',
            default=default_task_name,
            help='task name',
            type=types.sc_task_name,
        )

        self.add_argument(
            '-d', '--description',
            action='store',
            help='task description',
            type=str,
        )

        self.add_argument(
            '-a', '--args',
            action='store',
            help='program arguments',
            nargs='*',
            type=str,
        )

    def _extend_subparsers(self) -> None:
        pass

    @override
    def parse_args(
            self,
            args: Optional[Sequence[str]] = None,
            namespace: Optional[Namespace] = None
    ) -> Namespace:

        namespace = super().parse_args(args=args, namespace=namespace)

        return namespace
