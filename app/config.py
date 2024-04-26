from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import MongoDsn

load_dotenv()


class Settings(BaseSettings):
    MONGO_URL: MongoDsn
    SECRET_KEY: str
    INTRANET_ID: str
    INTRANET_PW: str
    ADMIN_PASSWORD: str


settings = Settings()

if __name__ == "__main__":
    print(settings.dict())
