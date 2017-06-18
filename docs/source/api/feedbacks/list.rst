feedbacks list
==============

Отзывы об ивенте.

**URL**::

    /{v}/feedbacks/list/

**Method**::

    POST

**Параметры запроса**

============  =======  ====  ========  ===========
Parameter     Default  Type  Required  Description
============  =======  ====  ========  ===========
``event_id``           int   true      Id ивента
============  =======  ====  ========  ===========

**Структура data**

=============  ====  ===========
Parameter      Type  Description
=============  ====  ===========
``feedbacks``  list  Отзывы
=============  ====  ===========

Элементы ``feedbacks`` имеют следующую структуру.

==================  ====  ================================
Parameter           Type  Description
==================  ====  ================================
``id``              int   Id места
``comment``         str   Комментарий
``rating``          int   Оценка
``participant_id``  int   ID участника
``created_at``      int   Дата создания
==================  ====  ================================


**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED
* EVENT_NOT_FOUND
* PERMISSION_DENIED

**Пример запроса**

.. code-block:: javascript

    {
        "event_id": 2
    }

**Пример ответа**

.. code-block:: javascript

    {
       "status":"ok",
       "data":{
          "feedbacks": [
		      {
		  	     "id":1,
			     "comment":"It was great!",
                 "rating":5,
			     "participant_id":1,
			     "created_at":1469049355
		      },
		      {
		  	     "id":2,
			     "comment":"Not so good",
                 "rating":2,
			     "participant_id":2,
			     "created_at":1469049366
		      }
		  ]
       }
    }