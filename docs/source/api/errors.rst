errors
======

В случае возникновения ошибки в любом из методов API, будет возвращён её код и сообщение.

=====================  ========================================
Error code             Description
=====================  ========================================
INTERNAL_ERROR         Общая ошибка
METHOD_IS_NOT_ALLOWED  Недопустимый HTTP метод
MISSING_PARAMETER      Пропущен обязательный параметр
INVALID_PARAMETER      Параметр не прошел валидацию
FACEBOOK_LOGIN_FAILED  Ошибка при попытке логина через Facebook
ACCOUNT_NOT_FOUND      Аккаунт не найден
=====================  ========================================

Response example:

.. code-block:: javascript

    {
        'status': 'error',
        'error_code': 'METHOD_IS_NOT_ALLOWED',
        'error_message': 'The request method is not allowed for this resource'
    }