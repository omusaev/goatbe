place details
=============

Информация по месту.

**URL**::

    /{v}/places/details/

**Method**::

    POST

**Параметры запроса**

===============  =======  =======  ========  ===========
Parameter        Default  Type     Required  Description
===============  =======  =======  ========  ===========
``event_id``              int      true      Id ивента
``place_id``              int      true      Id места
===============  =======  =======  ========  ===========

**Структура data**

===============  ====  ================================
Parameter        Type  Description
===============  ====  ================================
``id``           int   Id места
``title``        str   Заголовок
``description``  str   Описание
``start_at``     int   Дата старта
``finish_at``    int   Дата финиша
``order``        int   Подярок
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
* USER_IS_NOT_EVENT_PARTICIPANT
* PLACE_NOT_FOUND
* PLACE_IS_NOT_IN_EVENT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

   {
      "event_id": 1,
      "place_id": 2
   }

**Пример ответа**

.. code-block:: javascript

   {
      "status":"ok",
      "data":{
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
	  }
   }