delete event
============

Удаление ивента.

**URL**::

    /{v}/events/delete/

**Method**::

    POST

**Параметры запроса**

===============  =======  ========  ================
Parameter        Type     Required  Description
===============  =======  ========  ================
``event_id``     int      true      Id ивента
===============  =======  ========  ================

**Структура data**

Пустой словарь.

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* USER_IS_NOT_EVENT_PARTICIPANT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }