delete place
============

Удаление места.

**URL**::

    /{v}/places/delete/

**Method**::

    POST

**Параметры запроса**

============  =======  ====  ========  ===========
Parameter     Default  Type  Required  Description
============  =======  ====  ========  ===========
``event_id``           int   true      Id ивента
``place_id``           int   true      Id места
============  =======  ====  ========  ===========

**Структура data**

Пустой словарь.

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* USER_IS_NOT_EVENT_PARTICIPANT
* PLACE_NOT_FOUND
* PLACE_IS_NOT_IN_EVENT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "place_id": 2
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }