update event
============

Редактирование аттрибутов ивента.

**URL**::

    /{v}/events/update/

**Method**::

    POST

**Параметры запроса**

===============  =========  =======================  ========  ================
Parameter        Type       Format                   Required  Description
===============  =========  =======================  ========  ================
``event_id``     int                                 true      Id ивента
``title``        unicode    Length(min=1, max=255)   false     Заголовок
``description``  unicode    Length(min=1, max=2000)  false     Описание
``start_at``     timestamp                           false     Дата начала
``finish_at``    timestamp                           false     Дата окончания
===============  =========  =======================  ========  ================

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
        "event_id": 1,
        "title": "My second hiking!",
        "finish_at":1470049355
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }