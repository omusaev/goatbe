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
``status``              str   Статус
``start_at``            str   Дата старта
``description``         str   Описание
``title``               str   Название
``destination``         str   Место проведения
``finish_at``           str   Дата конца
``participants_count``  int   Количество участников
``participants``        list  Участники
``steps``               list  Шаги
======================  ====  =====================

Элементы ``participants`` имеют следующую структуру.

===============  ====  ====================
Parameter        Type  Description
===============  ====  ====================
``status``       str   Статус
``is_owner``     bool  Владелец ивента
``account_id``   int   Id пользователя
``permissions``  list  Права (в разработке)
===============  ====  ====================

Элементы ``steps`` имеют следующую структуру.

===============  ====  ===========
Parameter        Type  Description
===============  ====  ===========
``assignees``    list  Асайни
``type``         str   Тип
``description``  str   Описание
``title``        str   Название
===============  ====  ===========

Элементы ``assignees`` имеют следующую структуру.

===============  ====  ===============
Parameter        Type  Description
===============  ====  ===============
``resolution``   str   Резолюция
``account_id``   int   Id пользователя
===============  ====  ===============

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
                "account_id":15,
                "permissions":null
             },
             {
                "status":"ACTIVE",
                "is_owner":false,
                "account_id":16,
                "permissions":null
             },
             {
                "status":"INACTIVE",
                "is_owner":false,
                "account_id":17,
                "permissions":null
             }
          ],
          "steps":[
             {
                "assignees":[
                   {
                      "resolution":"OPEN",
                      "account_id":15
                   },
                   {
                      "resolution":"SKIPPED",
                      "account_id":16
                   }
                ],
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
                "type":"BACKPACK",
                "description":"Надо бы составить списочек",
                "title":"Составить список снаряжения"
             }
          ]
       }
    }