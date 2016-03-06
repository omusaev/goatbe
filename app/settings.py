# -*- coding: utf-8 -*-

import os

DATABASE = {
    'DIALECT': 'postgresql',
    'DRIVER': 'psycopg2',
    'USERNAME': 'goat',
    'PASSWORD': '[GEjcV9Fy9HK.[zz',
    'DATABASE': 'goat',
    'HOST': 'localhost',
    'PORT': '5432'
}

DB_CONNECTION_URL = '%(DIALECT)s+%(DRIVER)s://%(USERNAME)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(DATABASE)s' % DATABASE

INSTALLED_RESOURCES = [
    'resources.Ping',
]

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

try:
    from settings_local import *
except ImportError:
    pass


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine(DB_CONNECTION_URL)

Base = declarative_base()
Base.metadata.bind = engine

DBSession = scoped_session(sessionmaker(bind=engine))
