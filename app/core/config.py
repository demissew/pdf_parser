from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "pdf_parser"
    temp_dir: str = "/tmp/pdf_parser"
    max_upload_mb: int = 25
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_prefix="PDF_PARSER_",
        case_sensitive=False,
    )


settings = Settings()
