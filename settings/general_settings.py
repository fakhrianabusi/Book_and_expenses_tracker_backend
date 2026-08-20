from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralSettings(BaseSettings):
    APP_TITLE: str = "Book & Expenses Tracker"
    VERSION: str = "1.0.0"
    DATABASE_URL: str = "sqlite:///./expenses.db"
    ECHO: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


general_settings = GeneralSettings()
