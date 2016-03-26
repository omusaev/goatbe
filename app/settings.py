# -*- coding: utf-8 -*-

import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = '%s/logs/' % PROJECT_ROOT

SITE_HOST = '162.243.219.249'
SITE_PATH = '/'
SITE_URL = '%s%s' % (SITE_HOST, SITE_PATH)

DEBUG = False

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

MIDDLEWARES = [
    'common.resources.middlewares.ResourceSetupMiddleware',
    'common.sessions.middlewares.SessionMiddleware',
    'accounts.middlewares.AccountMiddleware'
]

INSTALLED_RESOURCES = [
    'api.resources.Ping',
    'accounts.resources.AuthFacebook',
    'accounts.resources.AuthAnonym',
    'accounts.resources.Logout',

    'events.resources.EventsTypes',
    'events.resources.CreateEvent',
]

SESSION_TTL = 60 * 60 * 24 * 14  # 2 weeks
SESSION_COOKIE_NAME = 'sessionid'

WORKERS = {
    'session_cleanup': {'sleep': 60 * 60},
}

FB_APP_ID = '1000652553335107'
FB_APP_SECRET = 'f7b5a32a886d31b3cfd6d22d55e75d4c'

try:
    from settings_local import *
except ImportError:
    pass


import logging


class LevelFilter(logging.Filter):

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        return record.levelno == self.level

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },

    'filters': {
        'CriticalLevelFilter': {
            '()': LevelFilter,
            'level': logging.CRITICAL,
        },
        'ErrorLevelFilter': {
            '()': LevelFilter,
            'level': logging.ERROR,
        },
        'WarningLevelFilter': {
            '()': LevelFilter,
            'level': logging.WARNING,
        },
        'InfoLevelFilter': {
            '()': LevelFilter,
            'level': logging.INFO,
        },
        'DebugLevelFilter': {
            '()': LevelFilter,
            'level': logging.DEBUG,
        },
    },

    'handlers': {
        'critical_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.CRITICAL,
            'formatter': 'simple',
            'filename': '%serror.log' % LOG_PATH,
            'maxBytes': 10485760,
            'backupCount': 3,
            'encoding': 'utf8',
            'filters': ['CriticalLevelFilter']
        },

        'error_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.ERROR,
            'formatter': 'simple',
            'filename': '%serror.log' % LOG_PATH,
            'maxBytes': 10485760,
            'backupCount': 3,
            'encoding': 'utf8',
            'filters': ['ErrorLevelFilter']
        },

        'warning_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.WARNING,
            'formatter': 'simple',
            'filename': '%serror.log' % LOG_PATH,
            'maxBytes': 10485760,
            'backupCount': 3,
            'encoding': 'utf8',
            'filters': ['WarningLevelFilter']
        },

        'info_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.INFO,
            'formatter': 'simple',
            'filename': '%sinfo.log' % LOG_PATH,
            'maxBytes': 10485760,
            'backupCount': 3,
            'encoding': 'utf8',
            'filters': ['InfoLevelFilter']
        },

        'debug_file_handler': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': logging.DEBUG,
            'formatter': 'simple',
            'filename': '%sdebug.log' % LOG_PATH,
            'maxBytes': 10485760,
            'backupCount': 3,
            'encoding': 'utf8',
            'filters': ['DebugLevelFilter']
        }
    },

    'root': {
        'level': logging.DEBUG if DEBUG else logging.WARNING,
        'handlers': ['info_file_handler', 'error_file_handler', 'warning_file_handler', 'debug_file_handler'],
    }
}


import logging.config
logging.config.dictConfig(LOGGING)
