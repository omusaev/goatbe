# -*- coding: utf-8 -*-

from contextlib import contextmanager

from db.base import db_session_factory

import logging
logger = logging.getLogger(__name__)


__all__ = (
    'db_session',
)

def _db_session_raiser(*args, **kwarg):
    raise RuntimeError('Trying to use connection outside of db session context')


@contextmanager
def db_session(autoflush=False, expire_on_commit=False, autocommit=False):
    """
    Provide a transactional master database scope around a series of operations.

    :rtype: sqlalchemy.orm.Session
    """

    db_session = db_session_factory(autoflush=autoflush, autocommit=autocommit, expire_on_commit=expire_on_commit)
    """:type: sqlalchemy.orm.Session"""
    try:
        yield db_session
        db_session.commit()
    except Exception, exc:
        db_session.rollback()
        logger.error('Master database transaction failed and rollbacked '
                     'due to error %s' % exc)
        raise
    except:
        db_session.rollback()
        logger.error('Transaction failed and rollbacked due to unknown reason')
        raise
    finally:
        db_session.close()
        db_session.connection = _db_session_raiser
