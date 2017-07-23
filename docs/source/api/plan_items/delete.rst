delete plan item
================

Удаление пунктов плана.

**URL**::

    /{v}/plan_items/delete/

**Method**::

    POST

**Параметры запроса**

================  =======  ====  ========  ===============
Parameter         Default  Type  Required  Description
================  =======  ====  ========  ===============
``event_id``               int   true      Id ивента
``plan_item_id``           int   true      Id пункта плана
================  =======  ====  ========  ===============

**Структура data**

Пустой словарь.

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* USER_IS_NOT_EVENT_PARTICIPANT
* PLAN_ITEM_NOT_FOUND
* PLAN_ITEM_IS_NOT_IN_EVENT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "plan_item_id": 2
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }