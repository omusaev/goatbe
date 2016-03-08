# -*- coding: utf-8 -*-

import time
import settings as app_settings

import logging
logger = logging.getLogger(__name__)

__all__ = (
    'BaseWorker',
)


class BaseWorker(object):

    name = ''

    def __init__(self):
        self._run = True
        self._sleep_time = int(app_settings.WORKERS.get(self.name, {}).get('sleep'))

    def _loop(self, logger):
        logger.info('Starting ioloop')
        while self._run:
            self.handle()
            self.rest_a_bit()

    def run(self):
        logger.info('Starting %s worker' % __name__)
        self._loop(logger)

    def rest_a_bit(self):
        time.sleep(self._sleep_time)

    def stop(self):
        self._run = False
        logger.info('Stopping %s worker' % __name__)

    def handle(self):
        raise NotImplementedError
