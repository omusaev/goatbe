# -*- coding: utf-8 -*-

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql.schema import UniqueConstraint

from db.base import Base
from db.mixins import GoatModelMixin


__all__ = (
    'Account',
)


class Account(Base, GoatModelMixin):

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

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String(255), nullable=False, default='')
    status = Column(String(255), nullable=False, default=STATUS.ACTIVE)
    avatar_url = Column(String(255), nullable=False, default='')
    auth_method = Column(String(255), nullable=False)
    identifier = Column(String(255), nullable=False)
    attributes = Column(JSON)

    UniqueConstraint('auth_method', 'identifier', name='auth_method_identifier')
