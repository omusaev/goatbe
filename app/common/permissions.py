# -*- coding: utf-8 -*-

__all__ = (
    'PERMISSION',
)


class PERMISSION(object):

    EDIT_EVENT_DETAILS = 'edit_event_details'
    READ_EVENT_DETAILS = 'read_event_details'
    DELETE_EVENT = 'delete_event'
    INVITE_EVENT_PARTICIPANT = 'invite_event_participant'
    DELETE_EVENT_PARTICIPANT = 'delete_event_participant'
    ADD_EVENT_STEP = 'add_event_step'
    EDIT_EVENT_STEP = 'edit_event_step'
    ADD_STEP_ASSIGNEE = 'add_step_assignee'
    DELETE_STEP_ASSIGNEE = 'delete_step_assignee'
    EDIT_STEP_RESOLUTION = 'edit_step_resolution'

    ALL = [
        EDIT_EVENT_DETAILS,
        READ_EVENT_DETAILS,
        DELETE_EVENT,
        INVITE_EVENT_PARTICIPANT,
        DELETE_EVENT_PARTICIPANT,
        ADD_EVENT_STEP,
        ADD_STEP_ASSIGNEE,
        DELETE_STEP_ASSIGNEE,
        EDIT_STEP_RESOLUTION,
    ]

    DEFAULT_OWNER_SET = ALL

    DEFAULT_NOT_OWNER_SET = [
        EDIT_EVENT_DETAILS,
        READ_EVENT_DETAILS,
        INVITE_EVENT_PARTICIPANT,
        ADD_STEP_ASSIGNEE,
        DELETE_STEP_ASSIGNEE,
        EDIT_STEP_RESOLUTION,
    ]
