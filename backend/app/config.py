from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="EV_")

    # SQLite by default so local dev needs no Postgres; use a postgresql+psycopg:// URL in prod.
    database_url: str = "sqlite:///./election.db"
    cors_origins: list[str] = ["http://localhost:5173"]
    poll_interval_minutes: int = 5


settings = Settings()
