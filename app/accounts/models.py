# -*- coding: utf-8 -*-

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql.schema import UniqueConstraint

from db.base import Base
from db.mixins import GoatBasicModelMixin


__all__ = (
    'Account',
)


class Account(Base, GoatBasicModelMixin):

    __tablename__ = 'account'

    class STATUS:
        ACTIVE = 'ACTIVE'
        INACTIVE = 'INACTIVE'

        ALL = (
            ACTIVE,
            INACTIVE,
        )

    class AUTH_METHOD:
        FB = 'FB'
        ANONYM = 'ANONYM'

        ALL = (
            FB,
            ANONYM,
        )

    name = Column(String(255), nullable=False, default='', server_default='')
    status = Column(String(255), nullable=False, default=STATUS.ACTIVE, server_default=STATUS.ACTIVE)
    avatar_url = Column(String(255), nullable=False, default='', server_default='')
    auth_method = Column(String(255), nullable=False)
    identifier = Column(String(255), nullable=False)

    UniqueConstraint('auth_method', 'identifier', name='auth_method_identifier')
