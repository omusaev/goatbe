update place
============

Редактирование места.

**URL**::

    /{v}/places/update/

**Method**::

    POST

**Параметры запроса**

===============  ========  =========   =======================  ========  ================================
Parameter        Default   Type        Format                   Required  Description
===============  ========  =========   =======================  ========  ================================
``event_id``               int                                  true      Id ивента
``title``                  unicode     Length(min=1, max=255)   false     Заголовок
``description``  ''        unicode     Length(min=1, max=2000)  false     Описание
``start_at``               timestamp                            false     Дата начала
``finish_at``              timestamp                            false     Дата окончания
``order``                  int                                  false     Порядок
``point``                  dict                                 false     Географическая точка
===============  ========  =========   =======================  ========  ================================

Элемент ``point`` имеют следующую структуру.

===============  =====  ================================
Parameter        Type   Description
===============  =====  ================================
``lng``          float  Долгота
``lat``        	 float  Широта
===============  =====  ================================


**Структура data**

Пустой словарь.

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* USER_IS_NOT_EVENT_PARTICIPANT
* PLACE_NOT_FOUND
* PLACE_IS_NOT_IN_EVENT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "place_id": 2,
        "title": "Second place"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }