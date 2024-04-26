from random import randint

import requests

from app.config import settings


def get_personal_code(login_id, login_pw):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
    headers = {
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    session = requests.Session()
    session.headers.update(headers)

    url_login_page = "https://hi.hana.hs.kr/member/login.asp"
    session.get(url_login_page)

    url_login_proc = "https://hi.hana.hs.kr/proc/login_proc.asp"
    login_data = {
        "login_id": login_id,
        "login_pw": login_pw,
        "x": str(randint(10, 99)),
        "y": str(randint(10, 99)),
    }
    session.post(url_login_proc, headers={"Referer": url_login_page}, data=login_data)

    url_mypage = "https://hi.hana.hs.kr/SYSTEM_Member/Member/MyPage/mypage.asp"
    response = session.get(url_mypage, headers={"Referer": "https://hi.hana.hs.kr/"})

    start_index = response.text.find("학번 : ") + len("학번 : ")
    student_id = response.text[start_index : start_index + 5]

    start_index = response.text.find("조회용 개인번호 : ") + len("조회용 개인번호 : ")
    code = response.text[start_index : start_index + 6]

    return {"student_id": student_id, "code": code}


if __name__ == "__main__":
    print(get_personal_code(settings.INTRANET_ID, settings.INTRANET_PW))
