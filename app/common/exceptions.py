# -*- coding: utf-8 -*-

from falcon import status_codes

__all__ = (
    'GoatBaseException',
    'UnsupportedResourceMethodException',
    'MissingParameterException',
    'InvalidParameterFormatException',
    'FacebookLoginException',
    'AccountNotFoundException',
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


class InvalidParameterFormatException(GoatBaseException):

    error_code = 'INVALID_PARAMETER'
    message_template = 'Invalid parameter format: %s: %s'

    def __init__(self, param_name, error_msg):
        self.param_name = param_name
        self.error_msg = error_msg

    @property
    def message(self):
        return self.message_template % (self.param_name, self.error_msg)


class FacebookLoginException(GoatBaseException):

    error_code = 'FACEBOOK_LOGIN_FAILED'

    def __init__(self, message):
        self.message = message


class AccountNotFoundException(GoatBaseException):

    error_code = 'ACCOUNT_NOT_FOUND'
    message = 'Account not found'
