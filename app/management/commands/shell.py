# -*- coding: utf-8 -*-

from management.commands import BaseCommand


class Command(BaseCommand):
    help = 'Run shell.'

    options = {
    }

    @classmethod
    def run(cls):
        from IPython import start_ipython
        start_ipython(argv=[])
