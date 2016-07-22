# -*- coding: utf-8 -*-

import logging
import logging.config
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
ALEMBIC_EXCLUDE_TABLES = ('spatial_ref_sys', )

MIDDLEWARES = [
    'core.resources.middlewares.ResourceSetupMiddleware',
    'core.sessions.middlewares.SessionMiddleware',
    'accounts.middlewares.AccountMiddleware'
]

INSTALLED_RESOURCES = [
    'accounts.resources.AuthFacebook',
    'accounts.resources.AuthAnonym',
    'accounts.resources.ReplaceAnonym',
    'accounts.resources.Logout',

    'events.resources.EventTypes',
    'events.resources.CreateEvent',
    'events.resources.UpdateEvent',
    'events.resources.CancelEvent',
    'events.resources.RestoreEvent',
    'events.resources.DeleteEvent',
    'events.resources.LeaveEvent',
    'events.resources.EventDetails',
    'events.resources.ShortEventDetails',
    'events.resources.ShortEventDetailsBySecret',
    'events.resources.MapEventDetails',
    'events.resources.EventList',

    'events.resources.DeleteParticipant',
    'events.resources.CreateParticipant',
    'events.resources.ActivateParticipant',

    'events.resources.CreateStep',
    'events.resources.UpdateStep',
    'events.resources.StepDetails',
    'events.resources.DeleteStep',
    'events.resources.ChangeStepsOrder',

    'events.resources.UpdateAssignees',
    'events.resources.UpdateAssigneesResolution',

    'events.resources.CreatePlace',
    'events.resources.UpdatePlace',
    'events.resources.DeletePlace',
    'events.resources.PlaceDetails',
    'events.resources.ChangePlacesOrder',
    'events.resources.MapPlaces',

    'common.resources.ClientSettings',
]

SESSION_TTL = 60 * 60 * 24 * 14  # 2 weeks
SESSION_COOKIE_NAME = 'sessionid'

WORKERS = {
    'session_cleanup': {'sleep': 60 * 60},
}

FB_APP_ID = '1000652553335107'
FB_APP_SECRET = 'f7b5a32a886d31b3cfd6d22d55e75d4c'

CLIENT_SETTINGS = {
    'REGISTRATION_SKIP_ENABLED': True,
}

RQ_CONNECTION = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
}


try:
    from settings_local import *
except ImportError:
    pass


# Logging

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

logging.config.dictConfig(LOGGING)
