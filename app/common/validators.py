# -*- coding: utf-8 -*-

from common.exceptions import PermissionDeniedException

__all__ = (
    'BaseValidator',
    'PermissionValidator',
)


class BaseValidator(object):

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, resource, *args, **kwargs):
        raise NotImplementedError


class PermissionValidator(BaseValidator):
    '''
    Needs AccountIsEventParticipantValidator
    '''

    def __init__(self, permissions):
        self.permissions = permissions

    def run(self, resource, *args, **kwargs):
        participant = resource.data['participant']
        participant_permissions = participant.permissions

        if not set(self.permissions).issubset(set(participant_permissions)):
            raise PermissionDeniedException
