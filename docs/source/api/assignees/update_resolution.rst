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

==================  =======  ====  ========  ================================================
Parameter           Default  Type  Required  Description
==================  =======  ====  ========  ================================================
``participant_id``           int   true      Id участника
``resolution``               str   true      :doc:`Резолюция <../other/assignee_resolutions>`
==================  =======  ====  ========  ================================================

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

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "step_id": 2,
        "resolutions": [
            {
                "participant_id": 12,
                "resolution": "RESOLVED"
            },
            {
                "participant_id": 13,
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