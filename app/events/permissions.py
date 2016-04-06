# -*- coding: utf-8 -*-

__all__ = (
    'PERMISSION',
)


class PERMISSION(object):

    UPDATE_EVENT_DETAILS = 'update_event_details'
    READ_EVENT_DETAILS = 'read_event_details'
    DELETE_EVENT = 'delete_event'
    INVITE_EVENT_PARTICIPANT = 'invite_event_participant'
    DELETE_EVENT_PARTICIPANT = 'delete_event_participant'
    CREATE_EVENT_STEP = 'create_event_step'
    DELETE_EVENT_STEP = 'delete_event_step'
    UPDATE_EVENT_STEP = 'update_event_step'
    CREATE_STEP_ASSIGNEE = 'create_step_assignee'
    DELETE_STEP_ASSIGNEE = 'delete_step_assignee'
    UPDATE_STEP_RESOLUTION = 'update_step_resolution'

    ALL = [
        UPDATE_EVENT_DETAILS,
        READ_EVENT_DETAILS,
        DELETE_EVENT,
        INVITE_EVENT_PARTICIPANT,
        DELETE_EVENT_PARTICIPANT,
        CREATE_EVENT_STEP,
        CREATE_STEP_ASSIGNEE,
        DELETE_STEP_ASSIGNEE,
        UPDATE_STEP_RESOLUTION,
    ]

    DEFAULT_OWNER_SET = ALL

    DEFAULT_NOT_OWNER_SET = [
        UPDATE_EVENT_DETAILS,
        READ_EVENT_DETAILS,
        INVITE_EVENT_PARTICIPANT,
        CREATE_STEP_ASSIGNEE,
        DELETE_STEP_ASSIGNEE,
        UPDATE_STEP_RESOLUTION,
    ]
