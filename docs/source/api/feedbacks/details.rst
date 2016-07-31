feedback details
================

Информация по отзыву.

**URL**::

    /{v}/feedbacks/details/

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

===============  ====  ================================
Parameter        Type  Description
===============  ====  ================================
``id``           int   Id места
``comment``      str   Комментарий
``rating``       int   Оценка
``account_id``   int   ID аккаунта
``created_at``   int   Дата создания
===============  ====  ================================


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
      "status":"ok",
      "data":{
			"id":1,
			"comment":"It was great!",
			"rating":5,
			"account_id":1,
			"created_at":1469049355
	  }
   }