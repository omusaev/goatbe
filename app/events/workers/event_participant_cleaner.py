# -*- coding: utf-8 -*-

from core.workers import BaseWorker
from events.models import EventManager

import logging
logger = logging.getLogger(__name__)


class Worker(BaseWorker):

    name = 'event_participant_cleaner'

    def handle(self):
        EventManager.clean_inactive_participants()
