short event details
===================

Короткая информация по ивенту для неактивного участника.

**URL**::

    /{v}/events/details/short/

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
``status``              str   :doc:`Статус ивента <../other/event_statuses>`
``start_at``            str   Дата старта
``description``         str   Описание ивента
``title``               str   Название ивента
``destination``         str   Место проведения
``finish_at``           str   Дата конца
``participants``        list  Участники
======================  ====  ==============================================

Элементы ``participants`` имеют следующую структуру.

===============  ====  =======================================================
Parameter        Type  Description
===============  ====  =======================================================
``status``       str   :doc:`Статус <../other/participant_statuses>`
``account``      dict  Пользователь
===============  ====  =======================================================

``account`` имеют следующую структуру.

==============  ====  ========================
Parameter       Type  Description
==============  ====  ========================
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
       }
    }