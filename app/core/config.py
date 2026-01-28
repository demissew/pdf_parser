from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "pdf_parser"
    temp_dir: str = "/tmp/pdf_parser"
    max_upload_mb: int = 25
    log_level: str = "INFO"
    docling_num_threads: int = 2
    docling_device: str = "cpu"
    docling_timeout_s: float | None = 180.0
    docling_max_num_pages: int = 300
    docling_max_file_size_mb: int = 25

    model_config = SettingsConfigDict(
        env_prefix="PDF_PARSER_",
        case_sensitive=False,
    )


settings = Settings()
