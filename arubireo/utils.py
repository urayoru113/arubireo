from datetime import datetime

from pydantic import BaseSettings


class Settings(BaseSettings):
    channel_access_token: str = ""
    chennel_secret: str = ""
    group_id: str = ""
    sqlalchemy_database_url = ""

    class Config:
        env_file = ".env"


def validate_date(text) -> bool:
    try:
        datetime.strptime(text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_date_md(text) -> bool:
    try:
        datetime.strptime(text, "%m-%d")
        return True
    except ValueError:
        return False
