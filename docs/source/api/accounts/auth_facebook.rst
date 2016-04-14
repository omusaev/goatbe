auth facebook
=============

Аутентификация или создание аккаунта через facebook (OAuth2).

Если пользователя нет в приложении, он добавляется. Затем происходит аутентификация.

Метод возвращает новый долгосрочный токен пользователя.
Этот токен нужно использовать на клиенте в дальнейшем для аутентификации или для работы с facebook api/sdk(если есть такая возможность).

**URL**::

    /{v}/accounts/auth/facebook/

**Method**::

    POST

**Параметры запроса**

=====================  =======  ====  ========  =====================
Parameter              Default  Type  Required  Description
=====================  =======  ====  ========  =====================
``user_access_token``           str   true      FB токен пользователя
=====================  =======  ====  ========  =====================

**Структура data**

=====================  ====  =====================
Parameter              Type  Description
=====================  ====  =====================
``user_access_token``  str   FB Токен пользователя
``account_id``         int   Id пользователя
=====================  ====  =====================

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* ACCOUNT_NOT_FOUND
* ALREADY_LOGGED_IN
* FACEBOOK_LOGIN_FAILED

**Пример запроса**

.. code-block:: javascript

    {
        "user_access_token": "CAAFzEZC9d68wBAHRZCYTB48xX8apum"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {
            "user_access_token": "KU8PZCINKjQB6730dXscqpUmplgZBq",
            "account_id": 20
        }
    }