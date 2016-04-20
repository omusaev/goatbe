step details
============

Информация по шагу.

**URL**::

    /{v}/steps/details/

**Method**::

    GET

**Параметры запроса**

===============  =======  =======  ========  ===========
Parameter        Default  Type     Required  Description
===============  =======  =======  ========  ===========
``event_id``              int      true      Id ивента
``step_id``               int      true      Id шага
===============  =======  =======  ========  ===========

**Структура data**

===============  ====  ================================
Parameter        Type  Description
===============  ====  ================================
``id``           int   Id шага
``assignees``    list  Асайни
``type``         str   :doc:`Тип <../other/step_types>`
``description``  str   Описание шага
``title``        str   Название шага
===============  ====  ================================

Элементы ``assignees`` имеют следующую структуру.

==============  ====  ================================================
Parameter       Type  Description
==============  ====  ================================================
``resolution``  str   :doc:`Резолюция <../other/assignee_resolutions>`
``account``     dict  Пользователь
==============  ====  ================================================

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
* STEP_NOT_FOUND
* STEP_IS_NOT_IN_EVENT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

   {
      "event_id": 1,
      "step_id": 2
   }

**Пример ответа**

.. code-block:: javascript

   {
      "status":"ok",
      "data":{
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
      }
   }