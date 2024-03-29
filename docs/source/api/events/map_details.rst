map event details
=================

Информация по ивенту для отображения на карте.

**URL**::

    /{v}/events/details/map/

**Method**::

    POST

**Параметры запроса**

============  =======  ====  ========  ===========
Parameter     Default  Type  Required  Description
============  =======  ====  ========  ===========
``event_id``           int   true      Id ивента
============  =======  ====  ========  ===========

**Структура data**

================  ====  ==============================================
Parameter         Type  Description
================  ====  ==============================================
``status``        str   :doc:`Статус ивента <../other/event_statuses>`
``start_at``      int   Дата старта
``description``   str   Описание ивента
``title``         str   Название ивента
``finish_at``     int   Дата конца
``places``        list  Места
================  ====  ==============================================

Элементы ``places`` имеют следующую структуру.

===============  ====  ================================
Parameter        Type  Description
===============  ====  ================================
``id``           int   Id места
``title``        str   Заголовок
``description``  str   Описание
``start_at``     int   Дата старта
``finish_at``    int   Дата финиша
``order``        int   Порядок
``point``        dict  Географическая точка
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
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 2
    }

**Пример ответа**

.. code-block:: javascript

    {
       "status":"ok",
       "data":{
          "status":"PREPARATION",
          "start_at":1469049355,
          "description":"Just another hike",
          "title":"Yearly extreme",
          "finish_at":1469059355,
          "places": [
		      {
		  	     "id":1,
		  	     "title":"Start point",
		  	     "description":"Let's start!",
		  	     "start_at":1469049355,
		  	     "finish_at":1469059355,
		  	     "order":1,
		  	     "point": {
				     "lng": -74.78886216922375,
                     "lat": 40.32829276931833
		  	      }
		      },
		      {
		  	      "id":2,
		  	      "title":"Finish point",
		  	      "description":"Let's finish!",
		  	      "start_at":1470049355,
		  	      "finish_at":1470049355,
		  	      "order":2,
		  	      "point": {
					  "lng": -75.78886216922375,
					  "lat": 41.32829276931833
		  	      }
		      }
		  ]
       }
    }