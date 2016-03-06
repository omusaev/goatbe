# -*- coding: utf-8 -*-

from falcon import status_codes

__all__ = (
    'GoatBaseException',
    'UnsupportedResourceMethod',
    'MissingParameterException',
    'InvalidParameterFormatException',
)


class GoatBaseException(Exception):

    status_code = status_codes.HTTP_409
    message = ''


class UnsupportedResourceMethod(GoatBaseException):

    status_code = status_codes.HTTP_405
    message = 'The request method is not allowed for this resource'


class MissingParameterException(GoatBaseException):

    message_template = 'Missing parameter: %s'

    def __init__(self, param_name):
        self.param_name = param_name

    @property
    def message(self):
        return self.message_template % self.param_name


class InvalidParameterFormatException(GoatBaseException):

    message_template = 'Invalid parameter format: %s: %s'

    def __init__(self, param_name, error_msg):
        self.param_name = param_name
        self.error_msg = error_msg

    @property
    def message(self):
        return self.message_template % (self.param_name, self.error_msg)
