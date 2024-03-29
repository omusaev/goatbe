# -*- coding: utf-8 -*-

import logging
import logging.config
import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
LOG_PATH = '%s/logs/' % PROJECT_ROOT

SITE_HOST = 'CHANGE_ME'
SITE_PATH = '/'
SITE_URL = '%s%s' % (SITE_HOST, SITE_PATH)

DEBUG = False

DATABASE = {
    'DIALECT': 'postgresql',
    'DRIVER': 'psycopg2',
    'USERNAME': 'CHANGE_ME',
    'PASSWORD': 'CHANGE_ME',
    'DATABASE': 'CHANGE_ME',
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
    'accounts.resources.UpdateAccount',

    'events.resources.EventTypes',
    'events.resources.CreateEvent',
    'events.resources.UpdateEvent',
    'events.resources.CancelEvent',
    'events.resources.RestoreEvent',
    'events.resources.FinishEvent',
    'events.resources.UnfinishEvent',
    'events.resources.DeleteEvent',
    'events.resources.EventDetails',
    'events.resources.ShortEventDetails',
    'events.resources.MapEventDetails',
    'events.resources.PlanEventDetails',
    'events.resources.EventList',

    'events.resources.DeleteParticipant',
    'events.resources.CreateParticipantSelf',
    'events.resources.ActivateParticipantSelf',
    'events.resources.DeleteParticipantSelf',

    'events.resources.CreateStep',
    'events.resources.UpdateStep',
    'events.resources.StepDetails',
    'events.resources.DeleteStep',
    'events.resources.ChangeStepsOrder',

    'events.resources.UpdateAssignees',
    'events.resources.UpdateAssigneesResolution',

    'events.resources.CreatePlace',
    'events.resources.RecreatePlace',
    'events.resources.UpdatePlace',
    'events.resources.DeletePlace',
    'events.resources.PlaceDetails',
    'events.resources.ChangePlacesOrder',
    'events.resources.MapPlaces',
    
    'events.resources.CreatePlanItem',
    'events.resources.UpdatePlanItem',
    'events.resources.DeletePlanItem',
    'events.resources.PlanItemDetails',
    'events.resources.ChangePlanItemsOrder',

    'events.resources.CreateFeedback',
    'events.resources.UpdateFeedback',
    'events.resources.DeleteFeedback',
    'events.resources.FeedbackDetails',
    'events.resources.FeedbacksList',

    'common.resources.ClientSettings',
]

SESSION_TTL = 60 * 60 * 24 * 14  # 2 weeks
SESSION_COOKIE_NAME = 'sessionid'

WORKERS = {
    'session_cleanup': {'sleep': 60 * 60},
    'event_status_updater': {'sleep': 60 * 60},
    'event_participant_cleaner': {'sleep': 6 * 60 * 60},
}

FB_APP_ID = 'CHANGE_ME'
FB_APP_SECRET = 'CHANGE_ME'

CLIENT_SETTINGS = {
    'REGISTRATION_SKIP_ENABLED': True,
}

RQ_CONNECTION = {
    'host': '127.0.0.1',
    'port': 6379,
    'db': 0,
}

SENTRY_ENABLED = True
SENTRY_DSN = 'CHANGE_ME'


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
        },
        'sentry': {
            'level': logging.ERROR,
            'class': 'raven.handlers.logging.SentryHandler',
            'dsn': SENTRY_DSN,
            'filters': ['ErrorLevelFilter'],
        },
    },

    'root': {
        'level': logging.DEBUG if DEBUG else logging.WARNING,
        'handlers': ['info_file_handler', 'error_file_handler', 'warning_file_handler', 'debug_file_handler'],
    }
}

if SENTRY_ENABLED:
    LOGGING['root']['handlers'].append('sentry')

logging.config.dictConfig(LOGGING)
