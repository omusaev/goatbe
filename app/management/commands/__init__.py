# -*- coding: utf-8 -*-

import os

__all__ = (
    'BaseCommand',
    'CommandError',
    'get_submodules',
)


class CommandError(Exception):
    pass


class BaseCommand(object):
    help = 'Command help'
    usage = None

    options = {}

    @classmethod
    def configure(cls, command_parser):
        command_parser.usage = cls.usage
        for opt, params in cls.options.iteritems():

            options = opt if isinstance(opt, tuple) else (opt, )
            command_parser.add_argument(*options, **params)

        command_parser.set_defaults(cmd=cls)

    @classmethod
    def run(cls, **kwargs):
        raise NotImplementedError()


def get_submodules():
    """
    Returns list of *.py files from current directory. `__init__.py` is omitted, file extenstions are truncated.

    :rtype: list
    """
    result = []
    for item in os.listdir(os.path.dirname(__file__)):
        if item.endswith('py') and item != '__init__.py':
            result.append(os.path.splitext(item)[0])
    return result
