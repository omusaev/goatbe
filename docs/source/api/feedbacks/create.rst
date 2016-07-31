create feedback
===============

Создание отзыва.

**URL**::

    /{v}/feedbacks/create/

**Method**::

    POST

**Параметры запроса**

===============  ========  =========   =======================  ========  ================================
Parameter        Default   Type        Format                   Required  Description
===============  ========  =========   =======================  ========  ================================
``event_id``               int                                  true      Id ивента
``comment``                unicode     Length(min=1, max=2000)  true      Комментарий
``rating``                 int                                  false     Оценка
===============  ========  =========   =======================  ========  ================================

**Структура data**

===============  ====  =============
Parameter        Type  Description
===============  ====  =============
``feedback_id``  int   Id отзыва
``order``        int   Порядок места
===============  ====  =============

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* USER_IS_NOT_EVENT_PARTICIPANT
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 1,
        "comment":"It was great!",
        "rating":5
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {
            "feedback_id": 1
        }
    }