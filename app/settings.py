# -*- coding: utf-8 -*-

import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

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

ALEMBIC_CONFIG_PATH = '%s/db/migrations/alembic.ini' % PROJECT_ROOT

INSTALLED_RESOURCES = [
    'api.resources.Ping',
]

SESSION_TTL = 60 * 60 * 24 * 14  # 2 weeks
SESSION_COOKIE_NAME = 'sessionid'

WORKERS = {
    'session_cleanup': {'sleep': 60 * 60},
}

AUTH_FB = 'FB'
AUTH_ANONYM = 'ANONYM'
AUTH_METHODS = (AUTH_FB, AUTH_ANONYM)

try:
    from settings_local import *
except ImportError:
    pass
