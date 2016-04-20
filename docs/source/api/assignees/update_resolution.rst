update assignee resolution
==========================

Редактирование резолюции асайни.

**URL**::

    /{v}/assignees/resolution/update/

**Method**::

    POST

**Параметры запроса**

===============  =======  ================  ========  =============================
Parameter        Default  Type              Required  Description
===============  =======  ================  ========  =============================
``event_id``              int               true      Id ивента
``step_id``               int               true      Id шага
``resolutions``           list(resolution)  true      Список резолюций по аккаунтам
===============  =======  ================  ========  =============================

Формат resolution

===============  =======  ====  ========  ===========
Parameter        Default  Type  Required  Description
===============  =======  ====  ========  ===========
``account_id``            int   true      Id аккунта
``resolution``            str   true      Резролюция
===============  =======  ====  ========  ===========

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
* ASSIGNEE_NOT_FOUND
* PERMISSION_DENIED
* INVALID_EVENT_STATUS

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "step_id": 2,
        "resolutions": [
            {
                "account_id": 12,
                "resolution": "RESOLVED"
            },
            {
                "account_id": 13,
                "resolution": "OPEN"
            }
        ]
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }