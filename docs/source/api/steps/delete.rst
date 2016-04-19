delete step
===========

Удаление шага.

**URL**::

    /{v}/steps/delete/

**Method**::

    POST

**Параметры запроса**

============  =======  ====  ========  ===========
Parameter     Default  Type  Required  Description
============  =======  ====  ========  ===========
``event_id``           int   true      Id ивента
``step_id``            int   true      Id шага
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
* STEP_NOT_FOUND
* STEP_IS_NOT_IN_EVENT
* PERMISSION_DENIED
* INVALID_EVENT_STATUS

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "step_id": 2,
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }