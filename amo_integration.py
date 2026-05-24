import requests
import json
from datetime import datetime

def send_task_to_amo(task_title: str, due_date: str, is_important: bool, note: str):
    SUBDOMAIN = "terleev02"
    TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6ImNiMzQzOTU5ODk5ZDFkNmM2YTEwZTAwZTJjZjk1ZmZkN2NiNmQyNTEyZTFmNGYxMDE2OGRmNjNhY2QyNjIxZGRjOGRlNTVjZDljNmU2NWIzIn0.eyJhdWQiOiJjYTEwZDAwYi1kYzA4LTQ3ZmUtOWQ3YS01ZTllMjJlNmZhMGMiLCJqdGkiOiJjYjM0Mzk1OTg5OWQxZDZjNmExMGUwMGUyY2Y5NWZmZDdjYjZkMjUxMmUxZjRmMTAxNjhkZjYzYWNkMjYyMWRkYzhkZTU1Y2Q5YzZlNjViMyIsImlhdCI6MTc3OTYzMTkxNywibmJmIjoxNzc5NjMxOTE3LCJleHAiOjE3ODI3Nzc2MDAsInN1YiI6IjEzODU5MDg2IiwiZ3JhbnRfdHlwZSI6IiIsImFjY291bnRfaWQiOjMzMDcwODkwLCJiYXNlX2RvbWFpbiI6ImFtb2NybS5ydSIsInZlcnNpb24iOjIsInNjb3BlcyI6WyJwdXNoX25vdGlmaWNhdGlvbnMiLCJmaWxlcyIsImNybSIsImZpbGVzX2RlbGV0ZSIsIm5vdGlmaWNhdGlvbnMiXSwiaGFzaF91dWlkIjoiNThmNzViODctY2UyMS00ZDZlLWEwYzMtYWIwZTA0NzEyZmZiIiwiYXBpX2RvbWFpbiI6ImFwaS1iLmFtb2NybS5ydSJ9.N913cPsE3JyEDsuYRlj7cO-tru2etIy-7t7OkfvpQiGhRD4lSABSkGvhmyGcKkM9vTf8W8EkMVgcQrNabp2JczLEzmDPfiL4ElMtl66BvDd7vU9BOVMct_ku1BVKiaoxHo7kF96LkYDYBj0PhWN25kneiEqe1ibJbUwL47DuXZECArroePu_AVAPl4o6VNxle7LrbIdHtOLXU0Ls-vgeueeXnE7j3JYEeZjtYjV91SwOc9uDDIswlhPm_kbRj_dtV_sIi5AuctARyhkCDk-HzRZijSLcLXdL-f2W4dElx-BRiZDI5AiFdLOGsDsM0NODr5l04l_qyW5XUklO_Vjq6w"

    FIELD_DUE_DATE = 655727
    FIELD_IMPORTANT = 655729
    FIELD_NOTE = 655733

    url = f"https://{SUBDOMAIN}.amocrm.ru/api/v4/leads"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    custom_fields = []
    if due_date:
        # Добавляем время 00:00:00 + часовой пояс
        due_date_formatted = f"{due_date}T00:00:00+03:00"
        custom_fields.append({
            "field_id": FIELD_DUE_DATE,
            "values": [{"value": due_date_formatted}]
        })

    custom_fields.append({
        "field_id": FIELD_IMPORTANT,
        "values": [{"value": "Да" if is_important else "Нет"}]
    })

    if note:
        custom_fields.append({
            "field_id": FIELD_NOTE,
            "values": [{"value": note}]
        })

    data = [{
        "name": task_title,
        "custom_fields_values": custom_fields
    }]

    # Диагностика
    print("[DEBUG] Отправляемые данные:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"[DEBUG] Статус: {response.status_code}")
        print(f"[DEBUG] Ответ: {response.text}")
        response.raise_for_status()
        print(f"[OK] Задача '{task_title}' отправлена в amoCRM")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Ошибка: {e}")
        if e.response is not None:
            print(f"[DEBUG] Тело ответа: {e.response.text}")
        return None