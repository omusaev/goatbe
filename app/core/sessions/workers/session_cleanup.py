# -*- coding: utf-8 -*-

from core.sessions.models import SessionManager
from core.workers import BaseWorker

import logging
logger = logging.getLogger(__name__)


class Worker(BaseWorker):

    name = 'session_cleanup'

    def handle(self):
        SessionManager.clear_expired()
