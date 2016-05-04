replace anonym
==============

Перенос данных анонимного аккаунта в новый, полноценный аккаунт. Перенос возможен только в том случае, если
полноценный аккаунт не является участником ни одого ивента. После переноса итоговый аккаунт имеет id анонимного.
Авторизоваться тем же анонимным аккаунт больше нельзя

**URL**::

    /{v}/accounts/auth/anonym/replace/

**Method**::

    POST

**Параметры запроса**

=====================  =======  ====  ========  =====================
Parameter              Default  Type  Required  Description
=====================  =======  ====  ========  =====================
``user_access_token``           str   true      Токен пользователя
=====================  =======  ====  ========  =====================

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* ACCOUNT_NOT_FOUND
* INVALID_AUTH_METHOD
* INVALID_ACCOUNT_STATE

**Пример запроса**

.. code-block:: javascript

    {
        "user_access_token": "3d34f6e82aad48c3909ea46ac2c33ccf"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }