# -*- coding: utf-8 -*-

from __future__ import absolute_import

from redis import Redis
from rq import Queue
from rq.decorators import job

import settings

__all__ = (
    'queue',
    'task',
)

queue = Queue(connection=Redis(**settings.RQ_CONNECTION))
task = job(queue=queue)
