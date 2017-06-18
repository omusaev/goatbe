step details
============

Информация по шагу.

**URL**::

    /{v}/steps/details/

**Method**::

    POST

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
               "participant_id":1
            },
            {
               "resolution":"SKIPPED",
               "participant_id":2
            }
         ],
         "id":1,
         "type":"COMMON",
         "order":1,
         "description":"Надо бы заполнить информацию",
         "title":"Заполнить информацию о походе"
      }
   }