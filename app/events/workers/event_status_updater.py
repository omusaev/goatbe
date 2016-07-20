# -*- coding: utf-8 -*-

from core.workers import BaseWorker
from events.models import EventManager

import logging
logger = logging.getLogger(__name__)


class Worker(BaseWorker):

    name = 'event_status_updater'

    def handle(self):
        EventManager.update_started()
        EventManager.update_finished()
