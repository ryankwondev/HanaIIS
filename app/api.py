from datetime import datetime, timedelta

from fastapi import APIRouter, Response, Request
from fastapi.templating import Jinja2Templates
from jose import jwt
from pydantic import BaseModel

from app.config import settings
from app.database import database
from app.login import get_personal_code

templates = Jinja2Templates(directory="app/pages")

router = APIRouter(
    prefix="/api",
    tags=["API"],
)


class IntranetLoginData(BaseModel):
    login_id: str
    login_pw: str


@router.post("/login")
def login(data: IntranetLoginData, response: Response):
    data = get_personal_code(data.login_id, data.login_pw)

    student_id = data["student_id"]
    code = data["code"]

    if student_id == "DOCTY" or " " in code:
        response.status_code = 401
        return {"message": "로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요."}
    else:
        return {
            "token": jwt.encode(
                {
                    "exp": datetime.now() + timedelta(minutes=30),
                    "student_id": student_id,
                    "code": code,
                },
                settings.SECRET_KEY,
                algorithm="HS256",
            )
        }


@router.get("/event_list")
def event_list():
    return [event for event in database["search_key"].find({}, {"_id": 0})]


class EventData(BaseModel):
    event_name: str
    collection_name: str
    search_key: str
    admin_password: str
    csv_data: list


@router.post("/event")
def event(data: EventData, request: Request):
    if data.admin_password != settings.ADMIN_PASSWORD:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": "비밀번호가 일치하지 않습니다."})

    database["search_key"].insert_one(
        {
            "event": data.event_name,
            "collection": data.collection_name,
            "search_key": data.search_key,
        }
    )

    database[data.collection_name].insert_many(data.csv_data)

    return {"message": "이벤트가 성공적으로 등록되었습니다."}


class AdminPassword(BaseModel):
    admin_password: str


@router.delete("/event/{event_id}")
def delete_event(event_id: str, data: AdminPassword, request: Request):
    if data.admin_password != settings.ADMIN_PASSWORD:
        return templates.TemplateResponse("error.html", {"request": request, "error_message": "비밀번호가 일치하지 않습니다."})

    database["search_key"].delete_one({"collection": event_id})
    database[event_id].drop()

    return {"message": "이벤트가 성공적으로 삭제되었습니다."}
