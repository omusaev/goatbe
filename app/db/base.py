# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import settings as app_settings


__all__ = (
    'engine',
    'Base',
    'db_session_factory',
)

engine = create_engine(app_settings.DB_CONNECTION_URL)

Base = declarative_base()
Base.metadata.bind = engine

db_session_factory = sessionmaker(bind=engine)


def get_base_for_migrations():
    # we have to import all models here to use auto generation of migrations feature
    from core.sessions.models import Session
    from accounts.models import Account
    from events.models import Event, Step, Participant, Assignee

    return Base
