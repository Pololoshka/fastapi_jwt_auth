# REST-сервис просмотра зарплаты

REST-сервис предназначен для просмотра текущей зарплаты и даты следующего повышения. Данные можно получить только при предъявлении валидного токена, который выдается сотруднику на 30 минут по логину и паролю.
Данные о сотрудниках хранятся в базе данных. По умолчанию в базе данных присутствуют данные о следующих сотрудниках:

```json
{"username": "@ivani", "password": "ivani"}
{"username": "@petri", "password": "petri"}
{"username": "@ivasya", "password": "ivasya"}
{"username": "@ilyai", "password": "ilyai"}
```

Проект покрыт интеграционными тестами.

Документация к API будет доступна после запуска сервиса по адресу:
[http://localhost:8001/docs](http://localhost:8000/docs)

# Содержание

- [Технологии](#technologies)
- [Запуск сервиса с помощью Docker](#docker)
- [Работа с сервисом](#interaction)
- [Разработка](#development)

  - [Требования](#requirements)
  - [Установка переменных окружения](#env)
  - [Установка зависимостей](#poetry)
  - [Создание и обновление схем в базе данных](#alembic)
  - [Структура базы данных](#db)
  - [Запуск Development сервера](#rundev)
  - [Тестирование](#tests)
  - [Форматирование и проверка кода](#check)
  - [Установка pre-commit](#precommit)

- [To do](#todo)
- [Команда](#team)

# Технологии

<a name="technologies"></a>

- Python
- FastAPI
- AsyncIO
- Pydantic
- SQLAlchemy
- Alembic
- REST API
- PyTest
- Ruff
- Docker
- Docker Compose

# Запуск сервиса с помощью Docker

<a name="docker"></a>

Для запуска контейнеров Docker c сервисом и с базой данных используйте команду:

```bash
docker compose up -d
```

Для отдельного запуска контейнера с DB используйте команду:

```bash
docker compose up -d db
```

# Работа с сервисом

<a name="interaction"></a>

Для получения токена для пользователя `{"username": "@ivani", "password": "ivani"}` используйте следующую команду:

```bash
curl -L -X POST 'http://127.0.0.1:8001/api/login/' \
-F 'username="@ivani"' \
-F 'password="ivani"'
```

Пример ответа:

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJAaXZhbmkiLCJleHAiOjE3MTQ4MzIzOTN9.t5d2DOFo1rhLQOkwdQdzeejNOEDy8b9Qq8WWTFYwtSk",
  "tokenType": "bearer"
}
```

Для получения данных о зарплате возьмите токен из предыдущей команды и используйте команду:

```bash
curl -L -X GET 'http://127.0.0.1:8001/api/salary/' \
-H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJAaXZhbmkiLCJleHAiOjE3MTQ4MzIzOTN9.t5d2DOFo1rhLQOkwdQdzeejNOEDy8b9Qq8WWTFYwtSk'
```

Пример ответа:

```json
{
  "username": "@ivani",
  "firstName": "Ivan",
  "lastName": "Ivanov",
  "salary": {
    "amount": 100000.0,
    "currency": "RUB",
    "nextIncreasesAt": "2024-09-14"
  }
}
```

# Разработка

<a name="development"></a>

## Требования

<a name="requirements"></a>
Для установки и запуска сервиса необходим
[Python3.12](https://www.python.org/downloads/release/python-3120/), а также [Poetry](https://python-poetry.org/).

## Установка переменных окружения

<a name="env"></a>

Создайте файл .env, скопируйте данные из файла [.env.tests](.env.tests) и замените DB_NAME:

```bash
cp .env.tests .env
vim .env
```

Также замените SECRET_KEY:

```bash
openssl rand -hex 32
```

## Установка зависимостей

<a name="poetry"></a>

Для установки зависимостей и активации виртуального окружения выполните команду:

```bash
poetry install

poetry shell
```

## Создание и обновление схем в базе данных

<a name="alembic"></a>

Для создания и обновления схем в базе данных используйте команду:

```bash
alembic upgrade head
```

## Структура базы данных

<a name="db"></a>
UML диаграмма

![diagram](uml_db.png)

## Запуск Development сервера

<a name="rundev"></a>

Чтобы запустить сервер для разработки, выполните команду:

```bash
python -m src.main
```

## Тестирование

<a name="tests"></a>

Для тестирования требуется создать тестовую базу данных. Смотрите файл [.env.tests](.env.tests)

Для создания тестовой базы данных используйте следующие комнады:

```bash
docker compose exec -it db psql -U <DB_USER> <DB_NAME>  # from .env
CREATE DATABASE <DB_NAME>;  # from .env.test
```

Для запуска тестов используйте команду:

```bash
pytest tests
```

## Форматирование и проверка кода

<a name="check"></a>

Для форматирования и проверки кода используйте команды из файла [Makefile](Makefile):

```bash
make fix
make check
```

## Установка pre-commit

<a name="precommit"></a>

Чтобы установить pre-commit, используйте команду из файла [Makefile](Makefile):

```bash
make install_pre_commit
```

# To do

<a name="todo"></a>

- [x] Продумать и реализовать архитекуру сервиса
- [x] Создать модели и подключить базу данных
- [x] Написать интеграционные тесты
- [x] Развернуть REST-сервис с использованием Docker

# Команда проекта

<a name="team"></a>
[Sokolova Polina — Python developer](https://github.com/Pololoshka)
