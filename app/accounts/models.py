# -*- coding: utf-8 -*-

import datetime
import logging

from sqlalchemy import Column, BigInteger, String, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSON

from db.base import Base
import settings as app_settings

logger = logging.getLogger(__name__)


__all__ = (
    'Account',
)


class Account(Base):

    __tablename__ = 'account'

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False, default='')
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)
    auth_method = Column(
        Enum(*app_settings.AUTH_METHODS, name='account_auth_method'),
        nullable=False,
    )
    identifier = Column(String(255), nullable=False)
    attributes = Column(JSON)
