# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DB_CONNECTION_URL

__all__ = (
    'engine',
    'Base',
    'db_session_factory',
)

engine = create_engine(DB_CONNECTION_URL)

Base = declarative_base()
Base.metadata.bind = engine

db_session_factory = sessionmaker(bind=engine)
