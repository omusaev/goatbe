delete feedback
===============

Удаление отзыва.

**URL**::

    /{v}/feedbacks/delete/

**Method**::

    POST

**Параметры запроса**

===============  =======  ====  ========  ===========
Parameter        Default  Type  Required  Description
===============  =======  ====  ========  ===========
``event_id``              int   true      Id ивента
``feedback_id``           int   true      Id отзыва
===============  =======  ====  ========  ===========

**Структура data**

Пустой словарь.

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* USER_IS_NOT_EVENT_PARTICIPANT
* FEEDBACK_NOT_FOUND
* FEEDBACK_IS_NOT_IN_EVENT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "feedback_id": 1
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }