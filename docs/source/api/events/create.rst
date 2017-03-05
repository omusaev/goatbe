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

================  ====  ==============================================
Parameter         Type  Description
================  ====  ==============================================
``id``            int   Id ивента
``status``        str   :doc:`Статус ивента <../other/event_statuses>`
``start_at``      int   Дата старта
``description``   str   Описание ивента
``title``         str   Название ивента
``finish_at``     int   Дата конца
``secret``        str   Секретная строка
``participants``  list  Участники
``places``        list  Места
================  ====  ==============================================

Элементы ``participants`` имеют следующую структуру.

===========  ====  =============================================
Parameter    Type  Description
===========  ====  =============================================
``status``   str   :doc:`Статус <../other/participant_statuses>`
``account``  dict  Пользователь
===========  ====  =============================================

``account`` имеют следующую структуру.

==============  ====  ========================
Parameter       Type  Description
==============  ====  ========================
``name``        str   Имя пользователя
``avatar_url``  str   url аватара пользователя
==============  ====  ========================

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
          "id":2,
          "status":"PREPARATION",
          "start_at":1469049355,
          "description":"How about a trip to the georgia mountains, friends?!",
          "title":"My first hiking!",
          "finish_at":1469059355,
          "secret":"ym2e7k",
          "participants":[
             {
                "status":"ACTIVE",
                "account":{
                   "name":"Jerry",
                   "avatar_url":"http://avatars.com/123.png"
                }
             },
          ]
          "places": []
       }
    }