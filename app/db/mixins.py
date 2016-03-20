# -*- coding: utf-8 -*-

import datetime

import sqlalchemy as sa
from sqlalchemy import Column, BigInteger, DateTime, Boolean, text
from sqlalchemy.dialects.postgresql import JSON


__all__ = (
    'GoatModelMixin',
    'GoatBasicModelMixin',
)


class GoatModelMixin:
    created_at = Column(DateTime, default=datetime.datetime.now, server_default=text("(now() at time zone 'utc')"))
    updated_at = Column(DateTime, onupdate=datetime.datetime.now, server_default=text("(now() at time zone 'utc')"))


class GoatBasicModelMixin(GoatModelMixin):
    id = Column(BigInteger, primary_key=True, nullable=False)
    attributes = Column(JSON)
    is_deleted = Column(Boolean, nullable=False, default=False, server_default=sa.sql.expression.false())
