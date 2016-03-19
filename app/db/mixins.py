# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Column, DateTime


__all__ = (
    'GoatModelMixin',
)


class GoatModelMixin:
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
