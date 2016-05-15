# -*- coding: utf-8 -*-

import daemon

import core.sessions.workers.session_cleanup as session_cleanup

from management.commands import BaseCommand


class Command(BaseCommand):
    help = 'Run specific worker'

    workers = {
        'session_cleanup': session_cleanup.Worker
    }

    options = {
        'worker': {'help': 'Worker to run', 'choices': workers.keys()},
        ('-b', '--background'): {
            'help': 'Run in background',
            'dest': 'background',
            'action': 'store_const',
            'const': True,
            'default': False
        }
    }

    @classmethod
    def run(cls, worker=None, background=False, **kwargs):
        """
        :type worker: object
        :type background: bool
        :type kwargs: dict
        """

        if worker not in cls.workers:
            raise ValueError('Invalid worker. Should never be risen since argparse protects against invalid choices.')

        try:
            if background is False:
                worker = cls.workers[worker](**kwargs)
                worker.run()
            else:
                with daemon.DaemonContext():
                    worker = cls.workers[worker](**kwargs)
                    worker.run()
        except KeyboardInterrupt:
            worker.stop()
