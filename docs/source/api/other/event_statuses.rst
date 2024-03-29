event statuses
==============

Статусы ивентов.

=============  ====================
Resolution     Description
=============  ====================
PREPARATION    Идёт подготовка
READY          Подготовка завершена
IN_PROGRESS    Ивент стартовал
FINISHED       Ивент завершён
CANCELED       Ивент отклонён
NOT_COMPLETED  Ивент незавершён
=============  ====================

При создании ивента, ему присваивается статус PREPARATION.

Статус READY ивент получает, когда :doc:`все шаги завершены всеми асайнями <../assignees/update_resolution>`.

Когда наступает дата старта ивента, ему автоматически присваивается статус IN_PROGRESS, если он находился в статусе READY. Если на момент старта, ивент в статусе PREPARATION, его статус не меняется. Но в нём всё ещё можно завершить все шаги для достижения статуса READY, и затем он автоматически станет IN_PROGESS.

Когда наступает дата финиша ивента, ему автоматически присваивается статус FINISHED, если он находился в статусе READY или IN_PROGRESS. Если на момент старта, ивент в статусе PREPARATION, его статус меняется на NOT_COMPLETED.

Ивент переходит в статус CANCELED, после :doc:`отмены <../events/cancel>`.

Так же есть возможность послать ивент в статус FINISHED :doc:`принудительным завершением <../events/finish>`.