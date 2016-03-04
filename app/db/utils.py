# -*- coding: utf-8 -*-

import time
import unicodedata
from functools import partial

from contextlib import contextmanager

from sqlalchemy import event
from sqlalchemy.engine import Engine

from config import db_factory, config

import logging
from db import baked
from common.exceptions import WGESTBError
logger = logging.getLogger(__name__)


bakery = baked.bakery()


def clean_unormalize(data):
    form = config.get('wgestb', 'unicode_normalization_form')
    if isinstance(data, unicode):
        res = unicodedata.normalize(form, data)
    else:
        res = data
    return data.__class__(res.upper())


def _db_session_raiser(*args, **kwarg):
    raise RuntimeError('Trying to use connection outside of db session context')


@contextmanager
def master_session(autoflush=False, expire_on_commit=False):
    """
    Provide a transactional master database scope around a series of operations.

    :rtype: sqlalchemy.orm.Session
    """

    master = db_factory(master=True, autoflush=autoflush, autocommit=False, expire_on_commit=expire_on_commit)
    """:type: sqlalchemy.orm.Session"""
    try:
        yield master
        master.commit()
    except Exception, exc:
        master.rollback()
        if isinstance(exc, WGESTBError) and exc.code < 500:
            logger.info('Master database transaction failed and rollbacked '
                        'due to business logic error %s' % exc)
        else:
            logger.error('Master database transaction failed and rollbacked '
                         'due to error %s' % exc)
        raise
    except:
        master.rollback()
        logger.error('Transaction failed and rollbacked due to unknown reason')
        raise
    finally:
        master.close()
        master.connection = _db_session_raiser


@contextmanager
def slave_session():
    """
    Provide a read-only database session scope around a series of operations.

    :rtype: sqlalchemy.orm.Session
    """
    slave = db_factory(master=False, autoflush=False, autocommit=True, _enable_transaction_accounting=False)
    """:type: sqlalchemy.orm.Session"""

    try:
        yield slave
    except:
        logger.error('Slave database failed')
        raise
    finally:
        slave.close()
        slave.connection = _db_session_raiser


class QueryTracer(object):
    statements = []

    def __enter__(self):
        self.statements = []
        self.timed_statements = []
        self.failed_statements = []
        event.listen(Engine, "before_cursor_execute", self.before_cursor_execute)
        event.listen(Engine, "after_cursor_execute", self.after_cursor_execute)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        event.remove(Engine, "before_cursor_execute", self.before_cursor_execute)
        event.remove(Engine, "after_cursor_execute", self.after_cursor_execute)

    def before_cursor_execute(self, conn, cursor, statement, parameters, context, executemany):
        self.time_before = time.time()
        self.statements.append((statement, parameters))
        import threading
        self.failed_statements.append((threading.currentThread().ident, statement, parameters, time.time()))

    def after_cursor_execute(self, conn, cursor, statement, parameters, context, executemany):
        self.timed_statements.append((statement, parameters, self.time_before, time.time()))

    @property
    def num_queries(self):
        return len(self.statements)


class MetricsQueryTracer(QueryTracer):

    def __enter__(self):
        self.execution_time = 0.0
        event.listen(Engine, "before_cursor_execute", self.before_cursor_execute)
        event.listen(Engine, "after_cursor_execute", self.after_cursor_execute)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        event.remove(Engine, "before_cursor_execute", self.before_cursor_execute)
        event.remove(Engine, "after_cursor_execute", self.after_cursor_execute)

    def after_cursor_execute(self, conn, cursor, statement,
                        parameters, context, executemany):
        self.execution_time = time.time() - self.execution_time

    def before_cursor_execute(self, conn, cursor, statement, parameters, context, executemany):
        self.execution_time = time.time()


def add_value_to_enum_type(connection, type_name, old_value, new_value):
    fetch_result = connection.execute(
        """SELECT COUNT(*)
             FROM pg_catalog.pg_enum
            WHERE enumlabel = '%s';""" % type_name
    ).fetchall()

    if not fetch_result[0][0]:
        connection.execute("COMMIT;")

        values = connection.execute(
            """SELECT unnest(enum_range(NULL::%s))""" % (type_name,)
        ).fetchall()

        values = [i[0] for i in values]

        if new_value not in values:
            connection.execute(
                "ALTER TYPE %s ADD VALUE '%s' AFTER '%s';" % (
                    type_name, new_value, old_value
                )
            )
