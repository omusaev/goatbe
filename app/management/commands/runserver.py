# -*- coding: utf-8 -*-

import sys

from werkzeug.serving import run_simple

from management.commands import BaseCommand


class Command(BaseCommand):
    help = 'Run development server'

    options = {
        'bind_to': {
            'help': 'Port or address:port',
            'default': '0.0.0.0:8000',
            'nargs': '?',
        },
        '--no-reload': {
            'help': 'Do not autoreload when code changes',
            'action': 'store_false',
            'dest': 'user_reloader',
        }
    }

    @classmethod
    def run(cls, bind_to, user_reloader, **kwargs):
        from app import application

        if ':' in bind_to:
            host, port = bind_to.split(':')
        else:
            host = '127.0.0.1'
            port = bind_to

        port = int(port)

        sys.stdout.write('Dev server started at %s:%s\n' % (host, port))

        run_simple(host, port, application, use_reloader=user_reloader)
