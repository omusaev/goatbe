# -*- coding: utf-8 -*-

import sys

from alembic import command
from alembic.config import Config

from management.commands import BaseCommand

import settings as app_settings


class Command(BaseCommand):
    """
    A migrate command for alembic. Usage

    ./app.py migrate history           shows migration history
    ./app.py migrate forward           migrates to head
    ./app.py migrate forward <rev>     migrates to revision
    ./app.py migrate backward <rev>    migrates backward to specific revision

    """
    help = 'Migrate database'

    class ACTIONS:
        FORWARD = 'forward'
        BACKWARD = 'backward'
        HISTORY = 'history'

    options = {
        'action': {
            'help': 'Action to perform',
            'choices': (
                ACTIONS.FORWARD,
                ACTIONS.BACKWARD,
                ACTIONS.HISTORY,
            )
        },
        'revision': {
            'help': 'Revision to migrate to',
            'default': None,
            'nargs': '?',
        },
    }

    @classmethod
    def run(cls, action, revision, **kwargs):
        alembic_config = Config(app_settings.ALEMBIC_CONFIG_PATH)

        if action == cls.ACTIONS.HISTORY:
            command.history(alembic_config)
        elif action == cls.ACTIONS.FORWARD:
            if revision is None:
                revision = 'head'
            command.upgrade(alembic_config, revision)
        elif action == cls.ACTIONS.BACKWARD:
            if revision is None:
                sys.stdout.write(
                    'Revision should be specified for backward migration\n'
                )
            else:
                command.downgrade(alembic_config, revision)
