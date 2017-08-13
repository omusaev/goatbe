event details
=============

Информация по ивенту.

**URL**::

    /{v}/events/details/

**Method**::

    POST

**Параметры запроса**

===============  =======  =======  ========  ===========
Parameter        Default  Type     Required  Description
===============  =======  =======  ========  ===========
``event_id``              int      true      Id ивента
===============  =======  =======  ========  ===========

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
``plan_items``    		list  Пункты плана
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

Элементы ``plan_items`` имеют следующую структуру.

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
* USER_IS_NOT_EVENT_PARTICIPANT
* PERMISSION_DENIED

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
                        'auth_method': 'ANONYM',
                        'identifier': 'd4uro3yok3jyt03km'
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
               "is_owner":false,
               "account_id":17,
               "permissions":[
                  "create_event_step",
                  "create_step_assignee"
               ]
            }
         ],
         "steps":[
            {
               "assignees":[
                  {
                     "resolution":"OPEN",
                     "partitipant_id":1
                  },
                  {
                     "resolution":"SKIPPED",
                     "partitipant_id":2
                  }
               ],
               "id":1,
               "type":"COMMON",
               "order":1,
               "description":"Надо бы заполнить информацию",
               "title":"Заполнить информацию о походе"
            },
            {
               "assignees":[
                  {
                     "resolution":"RESOLVED",
                     "partitipant_id":1
                  }
               ],
               "id":2,
               "type":"BACKPACK",
               "order":2,
               "description":"Надо бы составить списочек",
               "title":"Составить список снаряжения"
            }
         ],
         "places":[
            {
               "id":1,
               "title":"Start point",
               "description":"Let's start!",
               "start_at":1469049355,
               "finish_at":1469059355,
               "order":1,
               "point":{
                  "lng":-74.78886216922375,
                  "lat":40.32829276931833
               }
            },
            {
               "id":2,
               "title":"Finish point",
               "description":"Let's finish!",
               "start_at":1470049355,
               "finish_at":1470049355,
               "order":2,
               "point":{
                  "lng":-75.78886216922375,
                  "lat":41.32829276931833
               }
            }
         ],
         "plan_items":[
            {
               "id":1,
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
   }