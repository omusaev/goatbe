update step
===========

Редактирование шага подготовки

**URL**::

    /{v}/events/steps/update/

**Method**::

    POST

**Параметры запроса**

===============  =======  =======  =======================  ========  ===========
Parameter        Default  Type     Format                   Required  Description
===============  =======  =======  =======================  ========  ===========
``event_id``              int                               true      Id ивента
``step_id``               int                               true      Id шага
``title``                 unicode  Length(min=1, max=255)   false     Заголовок
``description``           unicode  Length(min=1, max=2000)  false     Описание
===============  =======  =======  =======================  ========  ===========

**Структура data**

Пустой словарь.

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
        "step_id": 2,
        "title": "Buy a knife!"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }