delete participant
==================

Удаление участника.

**URL**::

    /{v}/participants/delete/

**Method**::

    POST

**Параметры запроса**

==============  =======  ====  ========  ===========
Parameter       Default  Type  Required  Description
==============  =======  ====  ========  ===========
``event_id``             int   true      Id ивента
``account_id``           int   true      Id шага
==============  =======  ====  ========  ===========

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
        "account_id": 2,
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }