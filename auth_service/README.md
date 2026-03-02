# Auth Service

Микросервис для авторизации и регистрации пользователей с поддержкой загрузки данных из Excel файлов.

## Функционал

- **Регистрация пользователей** (одиночная и массовая через Excel)
- **Аутентификация** с выдачей JWT токенов
- **Хеширование паролей** с использованием bcrypt
- **Загрузка пользователей из Excel** файлов

## Быстрый старт

### 1. Запуск базы данных

```bash
cd auth_service
docker-compose up -d db
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка окружения

Создайте файл `.env` в директории `auth_service`:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=6432
DB_NAME=postgres
JWT_SECRET_KEY=your-secret-key-change-in-production
DEBUG=true
```

### 4. Запуск сервиса

```bash
uvicorn auth_service.src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Authentication

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/auth/login` | Вход пользователя |
| POST | `/api/auth/register` | Регистрация пользователя |
| GET | `/api/auth/users` | Получить всех пользователей |

### Registration (Excel)

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | `/api/register/register-from-excel` | Массовая регистрация из Excel |

### Health Check

| Метод | Endpoint | Описание |
|-------|----------|----------|
| GET | `/health` | Проверка работоспособности |

## Примеры использования

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Вход

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### Массовая регистрация из Excel

Excel файл должен содержать колонки:
- `username` (обязательно)
- `password` (обязательно)
- `email` (опционально)
- `full_name` (опционально)
- `phone` (опционально)
- `department` (опционально)

```bash
curl -X POST "http://localhost:8000/api/register/register-from-excel" \
  -F "file=@users.xlsx"
```

## Запуск в Docker

```bash
docker-compose up -d
```

Сервис будет доступен по адресу: `http://localhost:8000`

## Документация API

После запуска сервиса документация доступна по адресам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Структура проекта

```
auth_service/
├── src/
│   ├── api/           # API endpoints
│   ├── core/          # Конфигурация и безопасность
│   ├── models/        # SQLAlchemy модели и CRUD
│   ├── schemas/       # Pydantic схемы
│   ├── database.py    # Подключение к БД
│   └── main.py        # Точка входа
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── .env
```

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **AsyncPG** - асинхронный драйвер PostgreSQL
- **Passlib + bcrypt** - хеширование паролей
- **AuthX** - JWT аутентификация
- **OpenPyXL** - работа с Excel файлами
