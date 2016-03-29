create
========

Создание Event-a.


**URL**::

    /{v}/events/create/

**Method**::

    POST

**Параметры запроса**

=====================  =======  =======  =======================  ========  ===========================
Parameter              Default  Type     Format                   Required  Description
=====================  =======  =======  =======================  ========  ===========================
``lang``                        str                               true      Код языка (например, en_EN)
``type``                        str                               true      Тип
``title``                       unicode                           true      Заголовок
``description``                 unicode  Length(min=1, max=2000)  false     Описание
``destination``                 unicode  Length(min=1, max=255)   false     Место проведения
``start_at``                    str      2016-03-25 22:07:54      true      Дата начала
``finish_at``                   str      2016-03-25 22:07:54      true      Дата окончания
=====================  =======  =======  =======================  ========  ===========================


**Структура data**

=====================  ====  =====================================
Parameter              Type  Description
=====================  ====  =====================================
``event_id``           int   Id Event-a
=====================  ====  =====================================

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED

**Пример запроса**

.. code-block:: javascript

    {
        "lang": "en_EN",
        "type": "hiking",
        "title": "My first hiking!",
        "description": "How about a trip to the georgia mountains, friends?!",
        "destination": "Georgia",
        "start_at": "2016-06-27 16:30:00",
        "finish_at": "2016-07-11 18:30:00",
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {
            "event_id": 1
        }
    }