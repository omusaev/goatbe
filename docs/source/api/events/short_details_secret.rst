short event details by secret
=============================

Короткая информация по ивенту с доступом по секретной строке.

**URL**::

    /{v}/events/details/short/secret/

**Method**::

    POST

**Параметры запроса**

================  =======  ======================  ======  ========  =======================
Parameter         Default  Format                  Type    Required  Description
================  =======  ======================  ======  ========  =======================
``event_id``                                       int     true      Id ивента
``event_secret``           Length(min=32, max=32)  string  true      Секретная строка ивента
================  =======  ======================  ======  ========  =======================

**Структура data**

================  ====  ==============================================
Parameter         Type  Description
================  ====  ==============================================
``status``        str   :doc:`Статус ивента <../other/event_statuses>`
``start_at``      int   Дата старта
``description``   str   Описание ивента
``title``         str   Название ивента
``finish_at``     int   Дата конца
``participants``  list  Участники
``places``        list  Места
================  ====  ==============================================

Элементы ``participants`` имеют следующую структуру.

===========  ====  =============================================
Parameter    Type  Description
===========  ====  =============================================
``status``   str   :doc:`Статус <../other/participant_statuses>`
``account``  dict  Пользователь
===========  ====  =============================================

``account`` имеют следующую структуру.

==============  ====  ========================
Parameter       Type  Description
==============  ====  ========================
``name``        str   Имя пользователя
``avatar_url``  str   url аватара пользователя
==============  ====  ========================

Элементы ``places`` имеют следующую структуру.

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
* EVENT_NOT_FOUND
* INVALID_EVENT_SECRET

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 2,
        "event_secret": "3d34f6e82aad48c3909ea46ac2c33ccf"
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
          "participants":[
             {
                "status":"ACTIVE",
                "account":{
                   "name":"Jerry",
                   "avatar_url":"http://avatars.com/123.png"
                }
             },
             {
                "status":"INACTIVE",
                "account":{
                   "name":"Tom",
                   "avatar_url":"http://avatars.com/456.png"
                }
             }
          ]
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