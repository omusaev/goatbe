# -*- coding: utf-8 -*-

from common.sessions.models import SessionManager
from common.workers.base import BaseWorker

import logging
logger = logging.getLogger(__name__)


class Worker(BaseWorker):

    name = 'session_cleanup'

    def handle(self):
        SessionManager.clear_expired()
