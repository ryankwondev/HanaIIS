from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from jose import jwt, JWTError, ExpiredSignatureError

from app.config import settings
from app.database import database

router = APIRouter()
templates = Jinja2Templates(directory="app/pages")


@router.get("/")
def index():
    with open("app/pages/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@router.get('/admin')
def admin():
    with open('app/pages/admin.html', 'r', encoding='utf-8') as f:
        return HTMLResponse(f.read())


@router.get("/event/{event_id}")
def event(event_id: str, token: str, request: Request):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
    except ExpiredSignatureError:
        return templates.TemplateResponse(
            "error.html", {"request": request, "error_message": "토큰이 만료되었습니다."}
        )
    except JWTError:
        return templates.TemplateResponse(
            "error.html", {"request": request, "error_message": "토큰이 유효하지 않습니다."}
        )

    search_key = database["search_key"].find({"collection": event_id}, {"_id": 0})[0][
        "search_key"
    ]
    event_title = database["search_key"].find({"collection": event_id}, {"_id": 0})[0][
        "event"
    ]
    student_id = payload["student_id"]
    student_code = payload["code"]

    data = None

    if search_key == "student_id":
        data = database[event_id].find({"student_id": student_id}, {"_id": 0})
        data = [i for i in data]
        for i in data:
            del i["student_id"]
    elif search_key == "code":
        data = database[event_id].find({"code": student_code}, {"_id": 0})
        data = [i for i in data]
        for i in data:
            del i["code"]

    return templates.TemplateResponse(
        "event.html",
        {
            "request": request,
            "student_id": student_id,
            "event_title": event_title,
            "data": data,
        },
    )
