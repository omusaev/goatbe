# -*- coding: utf-8 -*-

from accounts.models import Account

from common.exceptions import AuthenticationRequiredException, InvalidAuthMethodException
from common.validators import BaseValidator

__all__ = (
    'AuthRequiredValidator',
    'AuthMethodValidator',
)


class AuthRequiredValidator(BaseValidator):

    def run(self, resource, *args, **kwargs):
        if not resource.account_info:
            raise AuthenticationRequiredException


class AuthMethodValidator(BaseValidator):

    # add some parameters if you need. Now it just checks that auth method is not anonym
    def run(self, resource, *args, **kwargs):
        if resource.account_info.account.auth_method == Account.AUTH_METHOD.ANONYM:
            raise InvalidAuthMethodException
