create step
===========

Создание шага.

**URL**::

    /{v}/steps/create/

**Method**::

    POST

**Параметры запроса**

===============  ========  =======  =======================  ========  ================================
Parameter        Default   Type     Format                   Required  Description
===============  ========  =======  =======================  ========  ================================
``event_id``               int                               true      Id ивента
``title``                  unicode  Length(min=1, max=255)   true      Заголовок
``description``  ''        unicode  Length(min=1, max=2000)  false     Описание
``type``         'CUSTOM'  unicode                           false     :doc:`Тип <../other/step_types>`
===============  ========  =======  =======================  ========  ================================

**Структура data**

===============  ====  ===========
Parameter        Type  Description
===============  ====  ===========
``step_id``      int   Id шага
===============  ====  ===========

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* USER_IS_NOT_EVENT_PARTICIPANT
* PERMISSION_DENIED
* INVALID_EVENT_STATUS

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "title": "Buy a balloon",
        "description": "Just for fun"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {
            "step_id": 63
        }
    }