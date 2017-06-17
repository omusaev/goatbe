Recreate place
==============

Создание места с предварительным удалением всех уже имеющихся мест

**URL**::

    /{v}/places/recreate/

**Method**::

    POST

**Параметры запроса**

===============  ========  =========   =======================  ========  ================================
Parameter        Default   Type        Format                   Required  Description
===============  ========  =========   =======================  ========  ================================
``event_id``               int                                  true      Id ивента
``places``                 list                                 true      Список мест
===============  ========  =========   =======================  ========  ================================

Элемент списка ``places`` имеют следующую структуру.

===============  ========  =========   =======================  ========  ================================
Parameter        Default   Type        Format                   Required  Description
===============  ========  =========   =======================  ========  ================================
``title``                  unicode     Length(min=1, max=255)   false     Заголовок
``description``  ''        unicode     Length(min=1, max=2000)  false     Описание
``start_at``               timestamp                            false     Дата начала
``finish_at``              timestamp                            false     Дата окончания
``order``                  int                                  false     Порядок
``point``                  dict                                 true      Географическая точка
===============  ========  =========   =======================  ========  ================================

Элемент ``point`` имеют следующую структуру.

===============  =====  ================================
Parameter        Type   Description
===============  =====  ================================
``lng``          float  Долгота
``lat``        	 float  Широта
===============  =====  ================================


**Структура data**

===============  ====  ========================
Parameter        Type  Description
===============  ====  ========================
``places_ids``   list  Список Id созданных мест
===============  ====  ========================

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
        "places": [
            {
                "title":"Start point",
                "description":"Let's start!",
                "start_at":1469049355,
                "finish_at":1469059355
                "order":1,
                "point": {
                     "lng": -74.78886216922375,
                     "lat": 40.32829276931833,
                }
            },
            {
                "title":"End point",
                "description":"Let's finish!",
                "start_at":1469049355,
                "finish_at":1469059355
                "order":1,
                "point": {
                     "lng": -74.78886216922375,
                     "lat": 40.32829276931833,
                }
            }
        ]
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {
            "places_ids": [1, 2],
        }
    }