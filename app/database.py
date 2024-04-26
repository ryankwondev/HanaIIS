from pymongo import MongoClient

from app.config import settings

client = MongoClient(str(settings.MONGO_URL))
database = client["default"]

if __name__ == "__main__":
    print(client.server_info())
