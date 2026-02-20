# Тестовое задание  на  вакансию Python Backend Разработчик.

Описание:
Необходимо разработать простой RESTful API сервис для реферальной системы.

<h3> Функциональные требования: </h3>
<ul>
    <li>регистрация и аутентификация пользователя (JWT, Oauth 2.0);</li>
    <li>аутентифицированный пользователь должен иметь возможность создать или удалить свой реферальный код. Одновременно может быть активен только 1 код. При создании кода обязательно должен быть задан его срок годности;</li>
    <li>возможность получения реферального кода по email адресу реферера;</li>
    <li>возможность регистрации по реферальному коду в качестве реферала;</li>
    <li>получение информации о рефералах по id реферера;</li>
    <li>UI документация (Swagger/ReDoc).</li>
</ul>

<h3>Опциональные задачи:</h3>
<ul>
    <li>использование clearbit.com/platform/enrichment для получения дополнительной информации о пользователе при регистрации;</li>
    <li>использование emailhunter.co для проверки указанного email адреса;</li>
    <li>кеширование реферальных кодов с использованием in-memory БД.</li>
</ul>

<h3>Инструкциями по запуску и тестированию:</h3>

## Структура проекта

```
referral_service/
├── app/
│   ├── api/                  # Транспортный слой (Route handlers)
│   │   ├── v1/
│   │   │   ├── endpoints/    # Эндпоинты разделенные по логике
│   │   │   │   ├── auth.py
│   │   │   │   ├── users.py
│   │   │   │   └── referrals.py
│   │   │   └── api.py        # Объединение всех роутеров
│   │   └── deps.py           # Зависимости (Логика извлечения)
│   ├── core/                 # Глобальные настройки
│   │   ├── config.py         # Pydantic-settings (env)
│   │   └── security.py       # JWT, хеширование паролей
│   ├── db/                   # Слой работы с БД
│   │   ├── session.py        # Настройка асинхронного движка SQLAlchemy
│   │   └── base.py           # Импорт всех моделей для Alembic
│   ├── models/               # SQLAlchemy модели
│   │   ├── user.py
│   │   └── referral.py
│   ├── schemas/              # Pydantic модели (DTO)
│   │   ├── user.py
│   │   ├── token.py
│   │   └── referral.py
│   ├── services/             # Бизнес-логика (Service Layer)
│   │   ├── auth_service.py
│   │   ├── referral_service.py
│   │   └── integrations/     # Внешние API
│   │       ├── clearbit.py
│   │       └── hunter.py
│   ├── crud/                 # Базовые операции с БД (Create, Read, Update, Delete)
│   │   ├── base.py
│   │   ├── crud_user.py
│   │   └── crud_referral.py
│   └── main.py               # Точка входа FastAPI
├── migrations/               # Файлы миграций Alembic
├── tests/                    # Unit и Integration тесты (pytest)
├── .env                      # Секреты (не пушить в git)
├── .env.example              # Пример переменных окружения
├── alembic.ini               # Конфиг миграций
├── docker-compose.yml        # Оркестрация (App, Postgres, Redis)
├── Dockerfile                # Сборка образа приложения
├── pyproject.toml            # Зависимости (Poetry) или requirements.txt
└── README.md                 # Документация по запуску

```



