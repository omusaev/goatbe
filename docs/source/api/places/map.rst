places map
==========

Места для отображения на общей карте.

**URL**::

    /{v}/places/map/

**Method**::

    POST

**Структура data**

Ответ представляет собой список объектов следующей структуры

===============  ====  ================================
Parameter        Type  Description
===============  ====  ================================
``id``           int   Id места
``title``        str   Заголовок
``description``  str   Описание
``start_at``     int   Дата старта
``finish_at``    int   Дата финиша
``point``        dict  Географическая точка
``event_id``     int   Id ивента
===============  ====  ================================

Элемент ``point`` имеют следующую структуру.

===============  =====  ================================
Parameter        Type   Description
===============  =====  ================================
``lng``          float  Долгота
``lat``        	 float  Широта
===============  =====  ================================

**Возможные ошибки**

* INTERNAL_ERROR
* AUTH_REQUIRED

**Пример запроса**

.. code-block:: javascript

   {}

**Пример ответа**

.. code-block:: javascript

   {
      "status":"ok",
      "data":[
      	{
      		"id":1,
			"title":"Start point",
			"description":"Let's start!",
			"start_at":1469049355,
			"finish_at":1469059355,
			"point": {
				 "lng": -74.78886216922375,
				 "lat": 40.32829276931833
            },
            "event_id":1
		},
		{
      		"id":2,
			"title":"Finish point",
			"description":"Let's finish!",
			"start_at":1469049355,
			"finish_at":1469059355,
			"point": {
				 "lng": -74.78886216922375,
				 "lat": 40.32829276931833
            },
            "event_id":1
		}
      ]
   }