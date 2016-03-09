# -*- coding: utf-8 -*-

from alembic import command
from alembic.config import Config

from management.commands import BaseCommand

import settings as app_settings


class Command(BaseCommand):
    help = 'Create new migration'

    options = {
        'message': {
            'help': 'Migration message',
        },
        '--auto': {
            'help': 'Autogenerate migration',
            'dest': 'autogenerate',
            'action': 'store_const',
            'const': True,
            'default': False,
        },
    }

    @classmethod
    def run(cls, message, **options):
        alembic_config = Config(app_settings.ALEMBIC_CONFIG_PATH)
        command.revision(alembic_config, message, autogenerate=options['autogenerate'])
