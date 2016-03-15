# -*- coding: utf-8 -*-

import datetime
import uuid

from sqlalchemy import Column, String, DateTime, PickleType

from db.base import Base
from db.helpers import db_session

import settings as app_settings

__all__ = (
    'Session',
    'SessionManager',
)


class Session(Base):

    __tablename__ = 'session'

    id = Column(String(32), primary_key=True)
    data = Column(PickleType, default={})

    expire_at = Column(DateTime,
                       default=datetime.datetime.now() + datetime.timedelta(seconds=app_settings.SESSION_TTL),
                       onupdate=datetime.datetime.now() + datetime.timedelta(seconds=app_settings.SESSION_TTL)
                       )

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)

    def __contains__(self, key):
        return key in self.data

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def get(self, key, default=None):
        return self.data.get(key, default)

    def pop(self, key, default=None):
        return self.data.pop(key, default)

    def update(self, dict_):
        self.data.update(dict_)


class SessionManager(object):

    @staticmethod
    def generate_session_id():
        return uuid.uuid4().hex

    @classmethod
    def create_session(cls):
        session = Session(
            id=cls.generate_session_id(),
            data={}
        )

        return session

    @staticmethod
    def get_session(session_id):
        with db_session() as db:
            session = db.query(Session).get(session_id)

        return session if session else None

    @staticmethod
    def get_or_create_session(session_id=None):
        if not session_id:
            return SessionManager.create_session()

        session = SessionManager.get_session(session_id)

        if not session:
            session = SessionManager.create_session()

        return session

    @staticmethod
    def save_session(session):
        with db_session() as db:
            db.merge(session)

    @staticmethod
    def delete_session(session):
        with db_session() as db:
            db.delete(session)

    @staticmethod
    def clear_expired():
        with db_session() as db:
            db.query(Session).filter(Session.expire_at < datetime.datetime.now()).delete()
