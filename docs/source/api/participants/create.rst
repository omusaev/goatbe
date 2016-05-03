create participant
==================

Создание участника.

**URL**::

    /{v}/participants/create/

**Method**::

    POST

**Параметры запроса**

================  =======  ======================  ======  ========  =======================
Parameter         Default  Format                  Type    Required  Description
================  =======  ======================  ======  ========  =======================
``event_id``                                       int     true      Id ивента
``event_secret``           Length(min=32, max=32)  string  true      Секретная строка ивента
================  =======  ======================  ======  ========  =======================

**Структура data**

Пустой словарь.

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* INVALID_EVENT_SECRET

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 2,
        "event_secret": "3d34f6e82aad48c3909ea46ac2c33ccf"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }