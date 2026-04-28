# Todo Light — MVP веб-приложение

Учебный проект **ПР-04**. Менеджер задач на FastAPI + Jinja2 с хранением данных в JSON-файле.

## Структура проекта

```
todo_light/
├── main.py               # FastAPI приложение
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
pip install fastapi uvicorn jinja2 python-multipart
```

### 2. Запустить сервер

```bash
uvicorn main:app --reload
```

### 3. Открыть в браузере

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
