create plan item
================

Создание пункта плана.

**URL**::

    /{v}/plan_items/create/

**Method**::

    POST

**Параметры запроса**

===============  ========  =========   =======================  ========  ================================
Parameter        Default   Type        Format                   Required  Description
===============  ========  =========   =======================  ========  ================================
``event_id``               int                                  true      Id ивента
``plan_items``             list                                 true      Список пунктов плана
===============  ========  =========   =======================  ========  ================================

Элемент списка ``plan_items`` имеют следующую структуру.

===============  ========  =========   =======================  ========  ================================
Parameter        Default   Type        Format                   Required  Description
===============  ========  =========   =======================  ========  ================================
``title``                  unicode     Length(min=1, max=255)   false     Заголовок
``description``  ''        unicode     Length(min=1, max=2000)  false     Описание
``start_at``               timestamp                            false     Дата начала
``finish_at``              timestamp                            false     Дата окончания
``order``                  int                                  false     Порядок
``point``                  dict                                 false     Географическая точка
===============  ========  =========   =======================  ========  ================================

Элемент ``point`` имеют следующую структуру.

===============  =====  ================================
Parameter        Type   Description
===============  =====  ================================
``lng``          float  Долгота
``lat``        	 float  Широта
===============  =====  ================================


**Структура data**

==================  ====  =================================
Parameter           Type  Description
==================  ====  =================================
``plan_items_ids``  list  Список Id созданных пунктов плана
==================  ====  =================================

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
      "event_id":1,
      "plan_items":[
         {
            "title":"Coming to Warsaw",
            "description":"First city of our trip",
            "start_at":1469049355,
            "finish_at":1469149355,
            "order":1,
            "point":{
               "lng":-74.78886216922375,
               "lat":40.32829276931833
            }
         },
         {
            "id":2,
            "title":"Coming to Berlin",
            "description":"Last city of our trip",
            "start_at":1469149355,
            "finish_at":1469249355,
            "order":2,
            "point":{
               "lng":-75.78886216922375,
               "lat":41.32829276931833
            }
         }
      ]
   }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {
            "plan_items": [1, 2],
        }
    }