# -*- coding: utf-8 -*-

__all__ = (
    'PERMISSION',
)


class PERMISSION(object):

    UPDATE_EVENT_DETAILS = 'update_event_details'
    READ_EVENT_DETAILS = 'read_event_details'
    READ_SHORT_EVENT_DETAILS = 'read_short_event_details'
    CANCEL_EVENT = 'cancel_event'
    RESTORE_EVENT = 'restore_event'
    FINISH_EVENT = 'finish_event'
    UNFINISH_EVENT = 'unfinish_event'
    DELETE_EVENT = 'delete_event'
    LEAVE_EVENT = 'leave_event'
    INVITE_EVENT_PARTICIPANT = 'invite_event_participant'
    DELETE_EVENT_PARTICIPANT = 'delete_event_participant'
    ACTIVATE_EVENT_PARTICIPANT = 'activate_event_participant'
    CREATE_EVENT_STEP = 'create_event_step'
    DELETE_EVENT_STEP = 'delete_event_step'
    UPDATE_EVENT_STEP = 'update_event_step'
    READ_STEP_DETAILS = 'read_step_details'
    REORDER_EVENT_STEPS = 'reorder_event_steps'
    CREATE_STEP_ASSIGNEE = 'create_step_assignee'
    DELETE_STEP_ASSIGNEE = 'delete_step_assignee'
    UPDATE_STEP_RESOLUTION = 'update_step_resolution'

    CREATE_EVENT_PLACE = 'create_event_place'
    DELETE_EVENT_PLACE = 'delete_event_place'
    UPDATE_EVENT_PLACE = 'update_event_place'
    REORDER_EVENT_PLACES = 'reorder_event_places'
    READ_PLACE_DETAILS = 'read_place_details'

    CREATE_EVENT_FEEDBACK = 'create_event_feedback'
    UPDATE_ANOTHERS_EVENT_FEEDBACK = 'update_anothers_event_feedback'
    DELETE_ANOTHERS_EVENT_FEEDBACK = 'delete_anothers_event_feedback'
    READ_EVENT_FEEDBACKS = 'read_event_feedbacks'

    ALL = [
        UPDATE_EVENT_DETAILS,
        READ_EVENT_DETAILS,
        READ_SHORT_EVENT_DETAILS,
        CANCEL_EVENT,
        RESTORE_EVENT,
        FINISH_EVENT,
        UNFINISH_EVENT,
        DELETE_EVENT,
        LEAVE_EVENT,
        INVITE_EVENT_PARTICIPANT,
        DELETE_EVENT_PARTICIPANT,
        ACTIVATE_EVENT_PARTICIPANT,
        CREATE_EVENT_STEP,
        DELETE_EVENT_STEP,
        UPDATE_EVENT_STEP,
        READ_STEP_DETAILS,
        CREATE_STEP_ASSIGNEE,
        DELETE_STEP_ASSIGNEE,
        UPDATE_STEP_RESOLUTION,
        CREATE_EVENT_PLACE,
        DELETE_EVENT_PLACE,
        UPDATE_EVENT_PLACE,
        REORDER_EVENT_PLACES,
        READ_PLACE_DETAILS,
        REORDER_EVENT_STEPS,
        CREATE_EVENT_FEEDBACK,
        DELETE_ANOTHERS_EVENT_FEEDBACK,
        READ_EVENT_FEEDBACKS,
    ]

    DEFAULT_OWNER_SET = ALL

    DEFAULT_NOT_OWNER_SET = [
        UPDATE_EVENT_DETAILS,
        LEAVE_EVENT,
        READ_EVENT_DETAILS,
        READ_SHORT_EVENT_DETAILS,
        INVITE_EVENT_PARTICIPANT,
        DELETE_EVENT_PARTICIPANT,
        ACTIVATE_EVENT_PARTICIPANT,
        CREATE_EVENT_STEP,
        DELETE_EVENT_STEP,
        UPDATE_EVENT_STEP,
        READ_STEP_DETAILS,
        CREATE_STEP_ASSIGNEE,
        DELETE_STEP_ASSIGNEE,
        UPDATE_STEP_RESOLUTION,
        READ_PLACE_DETAILS,
        CREATE_EVENT_FEEDBACK,
        READ_EVENT_FEEDBACKS,
    ]

    DEFAULT_INACTIVE_SET = [
        READ_SHORT_EVENT_DETAILS,
        LEAVE_EVENT,
        ACTIVATE_EVENT_PARTICIPANT,
    ]
