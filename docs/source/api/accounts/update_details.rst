update details
==============

Изменение аттрибутов аккаунта

**URL**::

    /{v}/accounts/details/update/

**Method**::

    POST

**Параметры запроса**

=====================  =======  ====  ========  =====================
Parameter              Default  Type  Required  Description
=====================  =======  ====  ========  =====================
``name``                        str   false     Имя пользователя
=====================  =======  ====  ========  =====================

**Возможные ошибки**

* INTERNAL_ERROR
* INVALID_PARAMETER
* AUTH_REQUIRED


**Пример запроса**

.. code-block:: javascript

    {
        "name": "Superman!"
    }

**Пример ответа**

.. code-block:: javascript

    {
        "status": "ok",
        "data": {}
    }