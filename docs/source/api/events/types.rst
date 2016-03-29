types
===========

Получение списка типов Event-а и их описания.

**URL**::

    /{v}/events/types/

**Method**::

    GET

**Параметры запроса**

=====================  =======  ====  ========  ===========================
Parameter              Default  Type  Required  Description
=====================  =======  ====  ========  ===========================
``lang``                        str   true      Код языка (например, en_EN)
=====================  =======  ====  ========  ===========================

**Структура data**
Data представляет собой список объектов на каждый из типов Event-a. Каджый из объектов содержит следующие поля

=====================  ====  =====================================
Parameter              Type  Description
=====================  ====  =====================================
``type``               str   Тип Event-a
``title``              str   Локализованный заголовок типа Event-a
``description``        str   Локализованное описание типа Event-a
=====================  ====  =====================================

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