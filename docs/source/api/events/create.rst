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

============  ====  ===========
Parameter     Type  Description
============  ====  ===========
``event_id``  int   Id ивента
============  ====  ===========

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
        "status": "ok",
        "data": {
            "event_id": 1
        }
    }