order places
============

Изменить порядок мест в ивенте.

**URL**::

    /{v}/places/order/

**Method**::

    POST

**Параметры запроса**

===============  =======  =======  ========  =========================
Parameter        Default  Type     Required  Description
===============  =======  =======  ========  =========================
``event_id``              int      true      Id ивента
``orders``                list     true      Список мест и их порядков
===============  =======  =======  ========  =========================

Элемент ``orders`` сожержит объекты следующей структуры.

===============  =====  ================================
Parameter        Type   Description
===============  =====  ================================
``id``           int    Id места
``order``        int    Порядок
===============  =====  ================================

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
        "orders": [
        	{
        		"id":1,
        		"order":1,
        	},
        	{
        		"id":2,
        		"order":2,
        	},
        ]
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }