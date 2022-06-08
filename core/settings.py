from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AuthServer API"
    admin_email: str = ''
    items_per_user: int = 50
    secret_key = 'SECRET_KEY'
    algorithm = "HS256"
    docs_username = "valenchits"
    docs_password = "123"


settings = Settings(_env_file='.env', _env_file_encoding='utf-8')
