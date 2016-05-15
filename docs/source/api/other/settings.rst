get client settings
===================

Получение списка клиентских настроек

**URL**::

    /{v}/settings/

**Method**::

    POST


**Структура data**

Data представляет собой словарь настроек, где key является именем настройки, а value - значением.

**Существующие настройки**

* REGISTRATION_SKIP_ENABLED

**Возможные ошибки**

* INTERNAL_ERROR

**Пример запроса**

.. code-block:: javascript

    {}

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": [
            {
                "REGISTRATION_SKIP_ENABLED": true
            }
        ]
    }