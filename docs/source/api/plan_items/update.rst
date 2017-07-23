update plan item
================

Редактирование пункта плана.

**URL**::

    /{v}/plan_items/update/

**Method**::

    POST

**Параметры запроса**

================  ========  =========   =======================  ========  ================================
Parameter         Default   Type        Format                   Required  Description
================  ========  =========   =======================  ========  ================================
``event_id``                int                                  true      Id ивента
``plan_item_id``            int                                  true      Id пункта плана
``title``                   unicode     Length(min=1, max=255)   false     Заголовок
``description``   ''        unicode     Length(min=1, max=2000)  false     Описание
``start_at``                timestamp                            false     Дата начала
``finish_at``               timestamp                            false     Дата окончания
``order``                   int                                  false     Порядок
``point``                   dict                                 false     Географическая точка
================  ========  =========   =======================  ========  ================================

Элемент ``point`` имеют следующую структуру.

===============  =====  ================================
Parameter        Type   Description
===============  =====  ================================
``lng``          float  Долгота
``lat``        	 float  Широта
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
* PLAN_ITEM_NOT_FOUND
* PLAN_ITEM_IS_NOT_IN_EVENT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "plan_item_id": 2,
        "title": "Second city"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }