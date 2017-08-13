create event
============

Создание ивента.

**URL**::

    /{v}/events/create/

**Method**::

    POST

**Параметры запроса**

===============  =======  =========  =======================  ========  ==========================================
Parameter        Default  Type       Format                   Required  Description
===============  =======  =========  =======================  ========  ==========================================
``lang``                  str                                 true      :doc:`Код языка <../other/language_codes>`
``type``                  str                                 true      :doc:`Тип <types>`
``title``                 unicode    Length(min=1, max=255)   true      Заголовок
``description``  ''       unicode    Length(min=1, max=2000)  false     Описание
``start_at``              timestamp                           true      Дата начала
``finish_at``             timestamp                           true      Дата окончания
===============  =======  =========  =======================  ========  ==========================================

**Структура data**

======================  ====  ==============================================
Parameter               Type  Description
======================  ====  ==============================================
``id``                  int   Id ивента
``status``              str   :doc:`Статус ивента <../other/event_statuses>`
``start_at``            int   Дата старта
``description``         str   Описание ивента
``title``               str   Название ивента
``finish_at``           int   Дата конца
``participants``        list  Участники
``steps``               list  Шаги
``secret``              str   Секретная строка
``places``              list  Места
======================  ====  ==============================================

Элементы ``participants`` имеют следующую структуру.

===============  ====  =======================================================
Parameter        Type  Description
===============  ====  =======================================================
``id``           int   Id участника
``status``       str   :doc:`Статус <../other/participant_statuses>`
``is_owner``     bool  Является ли участник владельцем ивента
``account``      dict  Пользователь
``permissions``  list  Список :doc:`прав <../other/permissions>` участника
===============  ====  =======================================================


``account`` имеют следующую структуру.

==============  ====  ===================================
Parameter       Type  Description
==============  ====  ===================================
``id``          int   Id пользователя
``name``        str   Имя пользователя
``avatar_url``  str   url аватара пользователя
``identities``  list  Список идентификаторов пользователя
==============  ====  ===================================

Элементы ``identities`` имеют следующую структуру.

===============  ====  ===============================================================
Parameter        Type  Description
===============  ====  ===============================================================
``auth_method``  str   Тип :doc:`идентификатора <../other/account_types>` пользователя
``identifier``   str   Идентификатор пользователя
===============  ====  ===============================================================

Элементы ``steps`` имеют следующую структуру.

===============  ====  ================================
Parameter        Type  Description
===============  ====  ================================
``id``           int   Id шага
``assignees``    list  Асайни
``type``         str   :doc:`Тип <../other/step_types>`
``order``        int   Порядок шага
``description``  str   Описание шага
``title``        str   Название шага
===============  ====  ================================

Элементы ``assignees`` имеют следующую структуру.

==================  ====  ================================================
Parameter           Type  Description
==================  ====  ================================================
``resolution``      str   :doc:`Резолюция <../other/assignee_resolutions>`
``participant_id``  int   Id участника
==================  ====  ================================================

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
* AUTH_REQUIRED

**Пример запроса**

.. code-block:: javascript

    {
        "lang": "en",
        "type": "hiking",
        "title": "My first hiking!",
        "description": "How about a trip to the georgia mountains, friends?!",
        "start_at":1469049355,
        "finish_at":1469059355
    }

**Пример ответа**

.. code-block:: javascript

    {
       "status":"ok",
       "data":{
          "id":1,
          "status":"PREPARATION",
          "start_at":1469049355,
          "description":"Just another hike",
          "title":"Yearly extreme",
          "finish_at":1469059355,
          "secret":"ym2e7k",
          "participants":[
             {
                "id":1,
                "status":"ACTIVE",
                "is_owner":true,
                "account":{
                   "id":15,
                   "name":"Jerry",
                   "avatar_url":"http://avatars.com/123.png",
                   'identities':[
                      {
                         'auth_method': 'FB',
                         'identifier': 'r3y56u5j4'
                      }
                   ]
                },
                "permissions":[
                   "update_event_details",
                   "read_event_details",
                   "delete_event"
                ]
             },
             {
                "id":2,
                "status":"ACTIVE",
                "is_owner":false,
                "account":{
                   "id":16,
                   "name":"Tom",
                   "avatar_url":"http://avatars.com/456.png",
                   'identities':[
                      {
                         'auth_method': 'FB',
                         'identifier': 'j5l36ov'
                      }
                   ]
                },
                "permissions":[
                   "invite_event_participant",
                   "delete_event_participant"
                ]
             },
             {
                "id":3,
                "status":"INACTIVE",
                "is_owner":false,
                "account":{
                   "id":17,
                   "name":"Jerry",
                   "avatar_url":"http://avatars.com/123.png",
                   'identities':[
                      {
                         'auth_method': 'ANONYM',
                         'identifier': 'ryjo385ojf3f59'
                      }
                   ]
                },
                "permissions":[
                   "create_event_step",
                   "create_step_assignee"
                ]
             }
          ],
          "steps":[
             {
                "assignees":[],
                "id":1,
                "type":"COMMON",
                "order":1,
                "description":"Надо бы заполнить информацию",
                "title":"Заполнить информацию о походе"
             },
             {
                "assignees":[],
                "id":2,
                "type":"BACKPACK",
                "order":2,
                "description":"Надо бы составить списочек",
                "title":"Составить список снаряжения"
             }
          ],
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