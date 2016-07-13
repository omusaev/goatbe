# -*- coding: utf-8 -*-

import sys
import argparse
from importlib import import_module

from management.commands import BaseCommand, get_submodules, CommandError
from management.rq import task

__all__ = (
    'handle_cli',
    'task',
)

for item in get_submodules():
    try:
        import_module('management.commands.%s' % item)
    except ImportError:
        pass


def handle_cli():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers()

    for command in BaseCommand.__subclasses__():
        command_name = command.__module__.split('.').pop()
        command_parser = subparsers.add_parser(command_name, help=command.help)
        command.configure(command_parser)

    if len(sys.argv) < 2:
        parser.parse_args(['-h'])
        return

    options = parser.parse_args()
    params = options.__dict__

    cmd = params.pop('cmd')

    try:
        cmd.run(**params)
    except CommandError:
        command_name = cmd.__module__.split('.').pop()
        err = sys.exc_info()[1]
        subparsers._name_parser_map[command_name].error(str(err))
