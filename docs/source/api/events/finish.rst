finish event
============

Ручное завершение ивента. Ивент переходит в :doc:`статус <../other/event_statuses>` FINISHED.

Если в момент ручного завершения, дата финиша ещё не наступила, она смещается к текущей дате. Если в данной ситуации дата старта оказывается позже даты финиша, она устанавливается на вчера (за день до финиша).

Недоступно для завершённых и отменённых ивентов.

**URL**::

    /{v}/events/finish/

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