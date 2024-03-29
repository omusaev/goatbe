cancel event
============

Отмена ивента. Ивент переходит в :doc:`статус <../other/event_statuses>` CANCELED.

Недоступно для завершённых и отменённых ивентов.

**URL**::

    /{v}/events/cancel/

**Method**::

    POST

**Параметры запроса**

============  ====  ========  ===========
Parameter     Type  Required  Description
============  ====  ========  ===========
``event_id``  int   true      Id ивента
============  ====  ========  ===========

**Структура data**

Пустой словарь.

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* INVALID_EVENT_STATUS
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