auth_facebook
=============

Аутентификация или создание аккаунта через facebook (OAuth2).

Если пользователя нет в приложении, он добавляется. Затем происходит аутентификация.

Метод возвращает новый долгосрочный токен пользователя. Этот токен нужно использовать на клиенте в дальнейшем для аутентификации или для работы с facebook api/sdk.

Если пользователь уже аутентифицирован(есть сессионная кука), метод возвращает токен этого пользователя. Чтобы залогиниться другим пользователем, необходимо сначала разлогиниться.

URL::

    /{v}/accounts/auth/facebook/

POST
----

Request parameters:

=====================  =======  ====  ========  =====================
Parameter              Default  Type  Required  Description
=====================  =======  ====  ========  =====================
``user_access_token``           str   true      FB токен пользователя
=====================  =======  ====  ========  =====================

Possible errors:

* FACEBOOK_LOGIN_FAILED
* INTERNAL_ERROR
* ACCOUNT_NOT_FOUND

Request example:

.. code-block:: javascript

    {
        "user_access_token": "36a52532g2b3c5918t48"
    }
..

Response example:

.. code-block:: javascript

    {
        "user_access_token": "36bad52532gt2gbn43c5w918tt4rw8"
    }