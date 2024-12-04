## **Тестовое задание на Python разработчика.**

Задание выполнено на FastAPI, база данных для упрощения взята SQLite с использованием SQLAlchemy.

Аутентификации и авторизации в тестовом не предусмотрено,
но в таблицу с пользователями добавлены хешированные пароли,
для добавления смысла эндпоинта по изменению данных пользователя.

## **Установка и запуск**

1. Для запуска необходим Python версии 3.Х
2. В приложении используются дополнительные библиотеки, все зависимости хранятся в файле requirements.txt

## **Описание ТЗ**
Нужно написать mini API для фильмотеки со следующей структурой:
1. Пользователи
- Возможность создания пользователей.
- Возможность изменения данных пользователя.
- Возможность удаления пользователя.
2. Фильмы
- Возможность добавления новых фильмов.
- Возможность изменения данных о фильме.
- Возможность удаления фильмов.
3. Избранное
- Пользователь может добавлять фильмы в свой список избранного.
- Пользователь может удалять фильмы из своего списка избранного.
- Возможность получения списка избранных фильмов для конкретного пользователя.
Базу данных можно использовать любую, но подойдет и sqlite.

