import json
import os
from datetime import date, datetime
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from amo_integration import send_task_to_amo

app = FastAPI()
templates = Jinja2Templates(directory="templates")

DATA_FILE = "data.json"


def load_tasks() -> list[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(tasks: list[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks: list[dict]) -> int:
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard")
async def dashboard(request: Request, error: str = ""):
    tasks = load_tasks()
    today = date.today().isoformat()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "tasks": tasks,
        "today": today,
        "error": error,
        "active": "dashboard",
    })


@app.post("/dashboard")
async def add_task(
    request: Request,
    title: str = Form(...),
    due_date: str = Form(""),
    is_important: bool = Form(False),
    note: str = Form(""),
):
    title = title.strip()
    if not title:
        return RedirectResponse(url="/dashboard?error=Название+задачи+не+может+быть+пустым", status_code=303)

    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": title,
        "due_date": due_date if due_date else None,
        "is_important": is_important,
        "is_completed": False,
        "note": note.strip() if note.strip() else None,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }
    tasks.append(task)
    save_tasks(tasks)

    # ── Отправка в amoCRM ─────────────────────────────────────────────
    # Отправляем данные, даже если отправка не удалась — задача уже сохранена
    try:
        send_task_to_amo(
            task_title=title,
            due_date=due_date,
            is_important=is_important,
            note=note
        )
    except Exception as e:
        print(f"Ошибка при отправке в amoCRM: {e}")
    # ───────────────────────────────────────────────────────────────────

    return RedirectResponse(url="/dashboard", status_code=303)


@app.post("/complete/{task_id}")
async def complete_task(task_id: int, request: Request):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["is_completed"] = not t["is_completed"]
            break
    save_tasks(tasks)
    referer = request.headers.get("referer", "/dashboard")
    return RedirectResponse(url=referer, status_code=303)


@app.post("/delete/{task_id}")
async def delete_task(task_id: int, request: Request):
    tasks = load_tasks()
    tasks = [t for t in tasks if t["id"] != task_id]
    save_tasks(tasks)
    referer = request.headers.get("referer", "/dashboard")
    return RedirectResponse(url=referer, status_code=303)


@app.get("/today")
async def today_view(request: Request):
    tasks = load_tasks()
    today = date.today().isoformat()
    today_tasks = [t for t in tasks if t.get("due_date") == today]
    return templates.TemplateResponse("today.html", {
        "request": request,
        "tasks": today_tasks,
        "today": today,
        "active": "today",
    })


@app.get("/important")
async def important_view(request: Request):
    tasks = load_tasks()
    important_tasks = [t for t in tasks if t.get("is_important")]
    today = date.today().isoformat()
    return templates.TemplateResponse("important.html", {
        "request": request,
        "tasks": important_tasks,
        "today": today,
        "active": "important",
    })


@app.get("/settings")
async def settings_view(request: Request):
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("is_completed"))
    important = sum(1 for t in tasks if t.get("is_important"))
    return templates.TemplateResponse("settings.html", {
        "request": request,
        "total": total,
        "completed": completed,
        "important": important,
        "active": "settings",
    })