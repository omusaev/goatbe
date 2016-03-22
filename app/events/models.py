# -*- coding: utf-8 -*-

import sqlalchemy as sa
from sqlalchemy import Column, BigInteger, String, DateTime, Text, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import JSON

from accounts.models import Account
from db.base import Base
from db.mixins import GoatModelMixin, GoatBasicModelMixin


__all__ = (
    'Event',
    'Step',
    'Participant',
    'Assignee',
)


class Event(Base, GoatBasicModelMixin):

    __tablename__ = 'event'

    class STATUS:
        PREPARATION = 'PREPARATION'
        READY = 'READY'
        IN_PROGRESS = 'IN_PROGRESS'
        FINISHED = 'FINISHED'

        ALL = (
            PREPARATION,
            READY,
            IN_PROGRESS,
            FINISHED,
        )

    class TYPE:
        HIKING = 'HIKING'
        JOURNEY = 'JOURNEY'

        ALL = (
            HIKING,
            JOURNEY,
        )

    title = Column(String(255), nullable=False, default='', server_default='')
    destination = Column(String(255), nullable=False, default='', server_default='')
    description = Column(Text(), nullable=False, default='', server_default='')
    status = Column(String(32), nullable=False, default=STATUS.PREPARATION, server_default=STATUS.PREPARATION)
    type = Column(String(64), nullable=False)
    start_at = Column(DateTime, nullable=False)
    finish_at = Column(DateTime, nullable=False)


class Step(Base, GoatBasicModelMixin):

    __tablename__ = 'step'

    class Type:
        COMMON = 'COMMON'
        BACKPACK = 'BACKPACK'
        CUSTOM = 'CUSTOM'

        ALL = (
            COMMON,
            BACKPACK,
            CUSTOM,
        )

    title = Column(String(255), nullable=False, default='', server_default='')
    description = Column(Text(), nullable=False, default='', server_default='')
    type = Column(String(255), nullable=False, default=Type.COMMON, server_default=Type.COMMON)
    event_id = Column(
        BigInteger,
        ForeignKey(
            Event.id,
            use_alter=True,
            name='step_event_id',
            ondelete='CASCADE'
        ),
        nullable=False
    )


class Participant(Base, GoatModelMixin):

    __tablename__ = 'participant'

    class STATUS:
        ACTIVE = 'ACTIVE'
        INACTIVE = 'INACTIVE'

        ALL = (
            ACTIVE,
            INACTIVE,
        )

    account_id = Column(
        BigInteger,
        ForeignKey(
            Account.id,
            use_alter=True,
            name='participant_account_id',
            ondelete='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    event_id = Column(
        BigInteger,
        ForeignKey(
            Event.id,
            use_alter=True,
            name='participant_event_id',
            ondelete='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    status = Column(String(255), nullable=False, default=STATUS.ACTIVE, server_default=STATUS.ACTIVE)
    permissions = Column(JSON)
    is_owner = Column(Boolean, nullable=False, default=False, server_default=sa.sql.expression.false())


class Assignee(Base, GoatModelMixin):

    __tablename__ = 'assignee'

    class RESOLUTION:
        OPEN = 'OPEN'
        RESOLVED = 'RESOLVED'
        SKIPPED = 'SKIPPED'

        ALL = (
            OPEN,
            RESOLVED,
            SKIPPED,
        )

    account_id = Column(
        BigInteger,
        ForeignKey(
            Account.id,
            use_alter=True,
            name='assignee_account_id',
            ondelete='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    step_id = Column(
        BigInteger,
        ForeignKey(
            Step.id,
            use_alter=True,
            name='assignee_step_id',
            ondelete='CASCADE'
        ),
        primary_key=True,
        nullable=False
    )
    resolution = Column(String(255), nullable=False, default=RESOLUTION.OPEN, server_default=RESOLUTION.OPEN)
