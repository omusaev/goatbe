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
)


class GoatBaseException(Exception):

    status_code = status_codes.HTTP_200
    error_code = 'INTERNAL_ERROR'
    message = ''


class UnsupportedResourceMethodException(GoatBaseException):

    error_code = 'METHOD_IS_NOT_ALLOWED'
    message = 'The request method is not allowed for this resource'


class MissingParameterException(GoatBaseException):

    error_code = 'MISSING_PARAMETER'
    message_template = 'Missing parameter: %s'

    def __init__(self, param_name):
        self.param_name = param_name

    @property
    def message(self):
        return self.message_template % self.param_name


class InvalidParameterException(GoatBaseException):

    error_code = 'INVALID_PARAMETER'

    def __init__(self, message):
        self.message = message


class FacebookLoginException(GoatBaseException):

    error_code = 'FACEBOOK_LOGIN_FAILED'

    def __init__(self, message):
        self.message = message


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


class StepIsNotInEventException(GoatBaseException):

    error_code = 'STEP_IS_NOT_IN_EVENT'
    message = 'Step is not in event'
