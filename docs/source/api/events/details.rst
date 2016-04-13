event details
=============

Информация по ивенту.

**URL**::

    /{v}/events/details/

**Method**::

    GET

**Параметры запроса**

===============  =======  =======  ========  ===========
Parameter        Default  Type     Required  Description
===============  =======  =======  ========  ===========
``event_id``              int      true      Id ивента
===============  =======  =======  ========  ===========

**Структура data**

======================  ====  =====================
Parameter               Type  Description
======================  ====  =====================
``status``              str   Статус ивента
``start_at``            str   Дата старта
``description``         str   Описание ивента
``title``               str   Название ивента
``destination``         str   Место проведения
``finish_at``           str   Дата конца
``participants_count``  int   Количество участников
``participants``        list  Участники
``steps``               list  Шаги
======================  ====  =====================

Элементы ``participants`` имеют следующую структуру.

===============  ====  =============================================
Parameter        Type  Description
===============  ====  =============================================
``status``       str   Статус
``is_owner``     bool  Является ли участник владельцем ивента
``account``      dict  Пользователь
``permissions``  list  Список :doc:`прав <../permissions>` участника
===============  ====  =============================================

Элементы ``steps`` имеют следующую структуру.

===============  ====  =============
Parameter        Type  Description
===============  ====  =============
``id``           int   Id шага
``assignees``    list  Асайни
``type``         str   Тип
``description``  str   Описание шага
``title``        str   Название шага
===============  ====  =============

Элементы ``assignees`` имеют следующую структуру.

==============  ====  ============
Parameter       Type  Description
==============  ====  ============
``resolution``  str   Резолюция
``account``     dict  Пользователь
==============  ====  ============

``account`` имеют следующую структуру.

==============  ====  ========================
Parameter       Type  Description
==============  ====  ========================
``id``          int   Id пользователя
``name``        str   Имя пользователя
``avatar_url``  str   url аватара пользователя
==============  ====  ========================

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
          "status":"PREPARATION",
          "start_at":"2016-08-10 12:12:12",
          "description":"Just another hike",
          "title":"Yearly extreme",
          "destination":"Georgia",
          "finish_at":"2016-09-10 12:12:12",
          "participants_count":3,
          "participants":[
             {
                "status":"ACTIVE",
                "is_owner":true,
                "account":{
                   "id":15,
                   "name":"Jerry",
                   "avatar_url":"http://avatars.com/123.png"
                },
                "permissions":[
                   "update_event_details",
                   "read_event_details",
                   "delete_event"
                ]
             },
             {
                "status":"ACTIVE",
                "is_owner":false,
                "account":{
                   "id":16,
                   "name":"Tom",
                   "avatar_url":"http://avatars.com/456.png"
                },
                "permissions":[
                   "invite_event_participant",
                   "delete_event_participant"
                ]
             },
             {
                "status":"INACTIVE",
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
                      "account":{
                         "id":15,
                         "name":"Jerry",
                         "avatar_url":"http://avatars.com/123.png"
                      }
                   },
                   {
                      "resolution":"SKIPPED",
                      "account":{
                         "id":16,
                         "name":"Tom",
                         "avatar_url":"http://avatars.com/456.png"
                      }
                   }
                ],
                "id":1,
                "type":"COMMON",
                "description":"Надо бы заполнить информацию",
                "title":"Заполнить информацию о походе"
             },
             {
                "assignees":[
                   {
                      "resolution":"RESOLVED",
                      "account_id":15
                   }
                ],
                "id":2,
                "type":"BACKPACK",
                "description":"Надо бы составить списочек",
                "title":"Составить список снаряжения"
             }
          ]
       }
    }