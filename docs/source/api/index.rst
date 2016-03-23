API
===

API принимает на вход данные в формате json.

API отдаёт на выход данные в формате json.

В API реализован механизм сессий. При аутентификации пользователя выставляется кука sessionid. Эту куку клиент должен посылать на сервер при каждом запросе.

API версионируется. Номер версии добавляется в урл сразу за доменом. Например goat.be/v1/some/method/.

Методы API:

.. toctree::
   :maxdepth: 2

   accounts/index.rst
   events/index.rst
   steps/index.rst
   participants/index.rst
   assignees/index.rst

Дополнительная информация по API:

.. toctree::
   :maxdepth: 2

   errors.rst