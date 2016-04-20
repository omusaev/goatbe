event list
==========

Список ивентов, в которых текущий пользователь является участником.

**URL**::

    /{v}/events/list/

**Method**::

    GET

**Параметры запроса**

Входящих параметров нет.

**Структура data**

======================  ====  =============================================================================
Parameter               Type  Description
======================  ====  =============================================================================
``status``              str   :doc:`Статус ивента <../other/event_statuses>`
``start_at``            str   Дата старта
``description``         str   Описание ивента
``title``               str   Название ивента
``destination``         str   Место проведения
``finish_at``           str   Дата конца
``participant_status``  str   :doc:`Статус участника(текущий пользователь) <../other/participant_statuses>`
``is_owner``            bool  Является ли владельцем ивента текущий пользователь
======================  ====  =============================================================================

**Возможные ошибки**

* INTERNAL_ERROR
* AUTH_REQUIRED

**Пример ответа**

.. code-block:: javascript

    {
       "status":"ok",
       "data":[
           {
             "status":"PREPARATION",
             "start_at":"2016-08-10 12:12:12",
             "description":"Just another hike",
             "title":"Yearly extreme",
             "destination":"Georgia",
             "finish_at":"2016-09-10 12:12:12",
             "participant_status":"ACTIVE",
             "is_owner":true
           },
           {
             "status":"PREPARATION",
             "start_at":"2016-09-25 12:12:12",
             "description":"Wow! Qomolangma!",
             "title":"Yearly extreme",
             "destination":"Qomolangma",
             "finish_at":"2016-10-13 12:12:12",
             "participant_status":"INACTIVE",
             "is_owner":false
           },
       ]
    }