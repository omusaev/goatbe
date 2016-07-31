update feedback
===============

Редактирование отзыва.

**URL**::

    /{v}/feedbacks/update/

**Method**::

    POST

**Параметры запроса**

===============  ========  =========   =======================  ========  ================================
Parameter        Default   Type        Format                   Required  Description
===============  ========  =========   =======================  ========  ================================
``event_id``               int                                  true      Id ивента
``comment``                unicode     Length(min=1, max=2000)  false     Комментарий
``rating``                 int                                  false     Оценка
===============  ========  =========   =======================  ========  ================================

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
        "feedback_id": 1,
        "rating": 4
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }