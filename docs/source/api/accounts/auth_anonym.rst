auth anonym
===========

Аутентификация или создание анонимного аккаунта(скип регистрации).

Если пользователя нет в приложении, он добавляется(параметр user_access_token не передан).
Затем происходит аутентификация.

Метод возвращает токен пользователя. Этот токен нужно использовать на клиенте в дальнейшем для аутентификации.

**URL**::

    /{v}/accounts/auth/anonym/

**Method**::

    POST

**Параметры запроса**

=====================  =======  ====  ========  ==================
Parameter              Default  Type  Required  Description
=====================  =======  ====  ========  ==================
``user_access_token``           str   false     Токен пользователя
=====================  =======  ====  ========  ==================

**Структура data**

=====================  ====  ==================
Parameter              Type  Description
=====================  ====  ==================
``user_access_token``  str   Токен пользователя
``account_id``         int   Id пользователя
=====================  ====  ==================

**Возможные ошибки**

* INTERNAL_ERROR
* INVALID_PARAMETER
* ACCOUNT_NOT_FOUND
* ALREADY_LOGGED_IN

**Пример запроса**

.. code-block:: javascript

    {
        "user_access_token": "3d34f6e82aad48c3909ea46ac2c33ccf"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {
            "user_access_token": "3d34f6e82aad48c3909ea46ac2c33ccf",
            "account_id": 10
        }
    }