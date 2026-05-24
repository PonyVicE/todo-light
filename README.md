# Todo Light — MVP веб-приложение

Учебный проект **ПР-04 / ПР-05**. Менеджер задач на FastAPI + Jinja2 с хранением данных в JSON-файле и интеграцией с amoCRM.

## Структура проекта

```
todo_light/
├── main.py               # FastAPI приложение
├── amo_integration.py    # Интеграция с amoCRM
├── data.json             # Хранилище задач (JSON)
├── README.md
└── templates/
    ├── base.html         # Базовый шаблон (навигация, стили)
    ├── dashboard.html    # /dashboard — все задачи + форма
    ├── today.html        # /today — задачи на сегодня
    ├── important.html    # /important — важные задачи
    └── settings.html     # /settings — настройки (заглушка)
```

## Установка и запуск

### 1. Установить зависимости

```bash
pip install fastapi uvicorn jinja2 python-multipart requests
```

### 2. Настроить интеграцию с amoCRM

В файле `amo_integration.py` укажи свои данные:

```python
SUBDOMAIN = "terleev02"                     # твой субдомен в amoCRM
TOKEN = "твой_долгоживущий_токен"           # Long‑lived token
FIELD_DUE_DATE = 655727                     # ID поля «Срок выполнения»
FIELD_IMPORTANT = 655729                    # ID поля «Важное»
FIELD_NOTE = 655733                         # ID поля «Заметка»
```

### 3. Запустить сервер

```bash
uvicorn main:app --reload
```

### 4. Открыть в браузере

```
http://127.0.0.1:8000
```

Приложение автоматически перенаправит на `/dashboard`.

---

## Экраны приложения

| URL | Описание |
|---|---|
| `/dashboard` | Все задачи + форма добавления |
| `/today` | Задачи с due_date == сегодня |
| `/important` | Задачи с is_important == true |
| `/settings` | Настройки (статистика + info) |

## Таблица соответствия: атрибуты Task → поля формы

| Атрибут сущности Task | Тип (Python) | Поле формы HTML | Тип поля | Обязательное |
|---|---|---|---|---|
| `id` | int | — (автоинкремент) | — | авто |
| `title` | str | `<input name="title">` | text | ✅ да |
| `due_date` | str (YYYY-MM-DD) | `<input name="due_date">` | date | ❌ нет |
| `is_important` | bool | `<input name="is_important">` | checkbox | ❌ нет |
| `is_completed` | bool | — (через кнопку ✓) | button/POST | авто |
| `note` | str | `<textarea name="note">` | textarea | ❌ нет |
| `created_at` | str (YYYY-MM-DD) | — (авто, datetime.now) | — | авто |

---

## Интеграция с amoCRM (ПР-05)

При создании задачи через форму Todo Light автоматически создаётся Сделка в amoCRM с заполненными кастомными полями.

### Маппинг полей

| Поле формы (Todo Light) | Поле в amoCRM | Тип данных |
|---|---|---|
| `title` | Название сделки (name) | string |
| `due_date` | Кастомное поле «Срок выполнения» | date |
| `is_important` | Кастомное поле «Важное» (Да/Нет) | list |
| `note` | Кастомное поле «Заметка» | text |

### Пример запроса к API amoCRM

```python
data = [{
    "name": "Тестовая задача",
    "custom_fields_values": [
        {"field_id": 655727, "values": [{"value": "2026-05-25T00:00:00+03:00"}]},
        {"field_id": 655729, "values": [{"value": "Да"}]},
        {"field_id": 655733, "values": [{"value": "Проверка интеграции"}]}
    ]
}]
```

---

## Формат data.json

```json
[
  {
    "id": 1,
    "title": "Название задачи",
    "due_date": "2026-04-28",
    "is_important": true,
    "is_completed": false,
    "note": "Дополнительная заметка",
    "created_at": "2026-04-25"
  }
]
```

---

## Связь с учебными работами

- **ПР-04** — веб-интерфейс MVP
- **ПР-05** — интеграция с CRM (amoCRM)
