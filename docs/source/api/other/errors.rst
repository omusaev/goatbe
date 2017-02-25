errors
======

В случае возникновения ошибки в любом из методов API, будет возвращён её код и сообщение.

=================================  =====================================================
Error code                         Description
=================================  =====================================================
INTERNAL_ERROR                     Общая ошибка
METHOD_IS_NOT_ALLOWED              Недопустимый HTTP метод
MISSING_PARAMETER                  Пропущен обязательный параметр
INVALID_PARAMETER                  Параметр не прошел валидацию
FACEBOOK_LOGIN_FAILED              Ошибка при попытке логина через Facebook
ACCOUNT_NOT_FOUND                  Аккаунт не найден
ALREADY_LOGGED_IN                  Пользователь уже аутентифицирован
AUTH_REQUIRED                      Необходима аутентификация
EVENT_NOT_FOUND                    Ивент не найден
USER_IS_NOT_EVENT_PARTICIPANT      Пользователь не является участником ивента
USER_IS_ALREADY_EVENT_PARTICIPANT  Пользователь уже является участником ивента
PERMISSION_DENIED                  Недостаточно прав
STEP_NOT_FOUND                     Шаг не найден
ASSIGNEE_NOT_FOUND                 Асайни не найден
STEP_IS_NOT_IN_EVENT               Шаг не найден в ивенте
INVALID_EVENT_STATUS               Текущий статус ивента не позволяет совершить действие
INVALID_EVENT_SECRET               Неверный секрет ивента
INVALID_AUTH_METHOD                Неверный метод аутентификации
INVALID_ACCOUNT_STATE              Аккаунт имеет неподходящее состояние
PLACE_NOT_FOUND          	       Место не найдено
PLACE_IS_NOT_IN_EVENT              Место не найдено в ивенте
EVENT_IS_NOT_FINISHED_MANUALLY     Ивент не был завершён вручную
=================================  =====================================================