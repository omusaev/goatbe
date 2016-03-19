# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Column, DateTime, text


__all__ = (
    'GoatModelMixin',
)


class GoatModelMixin:
    created_at = Column(DateTime, default=datetime.datetime.now, server_default=text("(now() at time zone 'utc')"))
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, server_default=text("(now() at time zone 'utc')"))
