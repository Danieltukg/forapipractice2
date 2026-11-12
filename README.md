# api_yatube — CRUD для Yatube

REST API для социальной сети **Yatube**: посты, группы и комментарии.
Проект выполнен в рамках практической работы «CRUD для Yatube» на
**Django 3.2** и **Django REST Framework 3.12**.

## Возможности

- Аутентификация по токену (`TokenAuthentication`).
- API доступен только аутентифицированным пользователям
  (без токена — `401 Unauthorized`).
- Изменять и удалять пост или комментарий может только его автор,
  для остальных контент доступен только на чтение (`403 Forbidden`).
- Группы доступны только для чтения — создать группу через API нельзя
  (`405 Method Not Allowed`).
- Комментарии привязаны к посту: если поста нет — `404 Not Found`.
- Все модели зарегистрированы в админке Django.

## Технологии

- Python 3.9+
- Django 3.2
- Django REST Framework 3.12
- DRF Token Auth
- SQLite
- pytest

## Структура проекта

```
api_yatube/
├── postman_collection/        # коллекция Postman и скрипт тестовых данных
├── tests/                     # автотесты (pytest)
├── yatube_api/
│   ├── api/                   # приложение API (вся логика здесь)
│   │   ├── permissions.py     # IsAuthorOrReadOnly
│   │   ├── serializers.py     # Post, Group, Comment
│   │   ├── urls.py            # роутер router_v1
│   │   └── views.py           # вьюсеты
│   ├── posts/                 # модели Yatube + админка
│   ├── yatube_api/            # настройки проекта
│   └── manage.py
├── requirements.txt
└── README.md
```

## Как запустить проект

Клонировать репозиторий и перейти в него:

```bash
git clone https://github.com/Danieltukg/forapipractice2.git
cd forapipractice2
```

Создать и активировать виртуальное окружение:

```bash
# Windows
python -m venv venv
source venv/Scripts/activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

Установить зависимости:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции и создать суперпользователя:

```bash
cd yatube_api
python manage.py migrate
python manage.py createsuperuser
```

Запустить сервер разработки:

```bash
python manage.py runserver
```

API будет доступен по адресу `http://127.0.0.1:8000/api/v1/`,
админка — `http://127.0.0.1:8000/admin/`.

## Эндпоинты

| Метод | URL | Описание |
|---|---|---|
| POST | `/api/v1/api-token-auth/` | Получить токен по логину и паролю |
| GET, POST | `/api/v1/posts/` | Список постов / создать пост |
| GET, PUT, PATCH, DELETE | `/api/v1/posts/{post_id}/` | Получить / изменить / удалить пост |
| GET | `/api/v1/groups/` | Список групп |
| GET | `/api/v1/groups/{group_id}/` | Информация о группе |
| GET, POST | `/api/v1/posts/{post_id}/comments/` | Комментарии поста / добавить комментарий |
| GET, PUT, PATCH, DELETE | `/api/v1/posts/{post_id}/comments/{comment_id}/` | Получить / изменить / удалить комментарий |

Все запросы (кроме получения токена) требуют заголовок:

```
Authorization: Token <ваш_токен>
```

## Примеры запросов

Получение токена:

```http
POST /api/v1/api-token-auth/
{
    "username": "anton",
    "password": "password"
}
```

```json
{
    "token": "c1d2e3f4..."
}
```

Создание поста:

```http
POST /api/v1/posts/
Authorization: Token c1d2e3f4...
{
    "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре.",
    "group": 1
}
```

```json
{
    "id": 14,
    "text": "Вечером собрались в редакции «Русской мысли», чтобы поговорить о народном театре.",
    "author": "anton",
    "image": null,
    "group": 1,
    "pub_date": "2021-06-01T08:47:11.084589Z"
}
```

Добавление комментария к посту с `id=14`:

```http
POST /api/v1/posts/14/comments/
Authorization: Token c1d2e3f4...
{
    "text": "тест тест"
}
```

```json
{
    "id": 4,
    "author": "anton",
    "post": 14,
    "text": "тест тест",
    "created": "2021-06-01T10:14:51.388932Z"
}
```

Получение группы:

```http
GET /api/v1/groups/2/
Authorization: Token c1d2e3f4...
```

```json
{
    "id": 2,
    "title": "Математика",
    "slug": "math",
    "description": "Посты на тему математики"
}
```

## Тесты

Из корня репозитория (где лежит `pytest.ini`):

```bash
pytest
```

Проверка стиля кода:

```bash
flake8
```

## Проверка через Postman

1. Подготовить базу (скрипт очищает БД и создаёт пользователей
   `root` / `regular_user` и тестовую группу):
   ```bash
   cd postman_collection
   bash set_up_data.sh
   ```
2. Запустить сервер: `cd ../yatube_api && python manage.py runserver`.
3. В Postman нажать **Import** и выбрать
   `postman_collection/CRUD_for_yatube.postman_collection.json`.
4. Нажать `⋯` у коллекции → **Run collection**, включить
   **Persist responses for a session** и нажать **Run**.

Подробнее — в [postman_collection/README.md](postman_collection/README.md).
