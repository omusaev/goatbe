# -*- coding: utf-8 -*-

from falcon import status_codes

__all__ = (
    'GoatBaseException',
    'UnsupportedResourceMethodException',
    'MissingParameterException',
    'InvalidParameterException',
    'FacebookLoginException',
    'AccountNotFoundException',
    'AuthenticationRequiredException',
    'AlreadyLoggedInException',
    'EventNotFoundException',
    'UserIsNotEventParticipant',
    'PermissionDeniedException',
    'StepNotFoundException',
    'StepIsNotInEventException',
    'AssigneeNotFoundException',
    'InvalidEventStatusException',
    'InvalidEventSecretException',
    'InvalidAuthMethodException',
    'InvalidAccountStateException',
    'PlaceNotFoundException',
    'PlaceIsNotInEventException',
    'EventIsNotFinishedManuallyException',
)


class GoatBaseException(Exception):

    status_code = status_codes.HTTP_200
    error_code = 'INTERNAL_ERROR'
    message = ''

    def __init__(self, message=None):
        if message is not None:
            self.message = message


class UnsupportedResourceMethodException(GoatBaseException):

    error_code = 'METHOD_IS_NOT_ALLOWED'
    message = 'The request method is not allowed for this resource'


class MissingParameterException(GoatBaseException):

    error_code = 'MISSING_PARAMETER'
    message_template = 'Missing parameter: %s'

    def __init__(self, param_name):
        self.message = self.message_template % param_name


class InvalidParameterException(GoatBaseException):

    error_code = 'INVALID_PARAMETER'
    message = 'Invalid parameter'


class FacebookLoginException(GoatBaseException):

    error_code = 'FACEBOOK_LOGIN_FAILED'
    message = 'Facebook login failed'


class AccountNotFoundException(GoatBaseException):

    error_code = 'ACCOUNT_NOT_FOUND'
    message = 'Account not found'


class AuthenticationRequiredException(GoatBaseException):

    error_code = 'AUTH_REQUIRED'
    message = 'Authentication required'


class AlreadyLoggedInException(GoatBaseException):

    error_code = 'ALREADY_LOGGED_IN'
    message = 'Already logged in'


class EventNotFoundException(GoatBaseException):

    error_code = 'EVENT_NOT_FOUND'
    message = 'Event not found'


class UserIsNotEventParticipant(GoatBaseException):

    error_code = 'USER_IS_NOT_EVENT_PARTICIPANT'
    message = 'User is not event participant'


class PermissionDeniedException(GoatBaseException):

    error_code = 'PERMISSION_DENIED'
    message = 'Permission denied'


class StepNotFoundException(GoatBaseException):

    error_code = 'STEP_NOT_FOUND'
    message = 'Step not found'


class AssigneeNotFoundException(GoatBaseException):

    error_code = 'ASSIGNEE_NOT_FOUND'
    message = 'Assignee not found'


class StepIsNotInEventException(GoatBaseException):

    error_code = 'STEP_IS_NOT_IN_EVENT'
    message = 'Step is not in event'


class InvalidEventStatusException(GoatBaseException):

    error_code = 'INVALID_EVENT_STATUS'
    message = 'Invalid event status'


class InvalidEventSecretException(GoatBaseException):

    error_code = 'INVALID_EVENT_SECRET'
    message = 'Invalid event secret'


class InvalidAuthMethodException(GoatBaseException):

    error_code = 'INVALID_AUTH_METHOD'
    message = 'Invalid auth method'


class InvalidAccountStateException(GoatBaseException):

    error_code = 'INVALID_ACCOUNT_STATE'
    message = 'Invalid account state'


class PlaceNotFoundException(GoatBaseException):

    error_code = 'PLACE_NOT_FOUND'
    message = 'Place not found'


class PlaceIsNotInEventException(GoatBaseException):

    error_code = 'PLACE_IS_NOT_IN_EVENT'
    message = 'Place is not in event'


class EventIsNotFinishedManuallyException(GoatBaseException):

    error_code = 'EVENT_IS_NOT_FINISHED_MANUALLY'
    message = 'Event is not finished manually'
