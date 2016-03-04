# -*- coding: utf-8 -*-

import datetime

from sqlalchemy import Column, Integer, String, Date, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session

import settings as app_settings

__all__ = (
    'DBSession',
    'Base'
)


engine = create_engine(app_settings.DB_CONNECTION_URL)

Base = declarative_base()
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
