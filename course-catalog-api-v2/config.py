from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from the local .env file."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    sql_echo: bool = False
    graphql_introspection: bool = True


settings = Settings()
