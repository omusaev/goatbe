# -*- coding: utf-8 -*-

from common.exceptions import AuthenticationRequiredException
from common.validators import BaseValidator

__all__ = (
    'AuthRequiredValidator',
)


class AuthRequiredValidator(BaseValidator):

    def run(self, resource, *args, **kwargs):
        if not resource.account_info:
            raise AuthenticationRequiredException
