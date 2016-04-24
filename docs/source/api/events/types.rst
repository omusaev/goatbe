get event types
===============

Получение списка типов ивента и их описания.

**URL**::

    /{v}/events/types/

**Method**::

    POST

**Параметры запроса**

=========  =======  ====  ========  ==========================================
Parameter  Default  Type  Required  Description
=========  =======  ====  ========  ==========================================
``lang``            str   true      :doc:`Код языка <../other/language_codes>`
=========  =======  ====  ========  ==========================================

**Структура data**

Data представляет собой список типов ивента.
Тип это словарь со следующей структурой.

===============  ====  ====================================
Parameter        Type  Description
===============  ====  ====================================
``type``         str   Тип ивента
``title``        str   Локализованный заголовок типа ивента
``description``  str   Локализованное описание типа ивента
===============  ====  ====================================

**Возможные ошибки**

* INTERNAL_ERROR
* MISSING_PARAMETER
* INVALID_PARAMETER
* AUTH_REQUIRED

**Пример запроса**

.. code-block:: javascript

    {
        "lang": "en_EN"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": [
            {
                "type": "hiking",
                "title": "Hiking",
                "description": "Hiking in the nature"
            }
        ]
    }