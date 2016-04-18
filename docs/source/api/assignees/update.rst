update assignee
===============

Редактирование списка асайни.

**URL**::

    /{v}/assignees/update/

**Method**::

    POST

**Параметры запроса**

=========================  =======  =========  ========  ==================================
Parameter                  Default  Type       Required  Description
=========================  =======  =========  ========  ==================================
``event_id``                        int        true      Id ивента
``step_id``                         int        true      Id шага
``assign_accounts_ids``    []       list(int)  false     Список id аккаунтов для ассайна
``unassign_accounts_ids``  []       list(int)  false     Список id аккаунтов для разассайна
=========================  =======  =========  ========  ==================================

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
        "assign_accounts_ids": [12, 14, 16],
        "unassign_accounts_ids": [13, 15, 17]
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }