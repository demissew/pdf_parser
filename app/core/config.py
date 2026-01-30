from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "pdf_parser"
    temp_dir: str = "/tmp/pdf_parser"
    max_upload_mb: int = 25
    log_level: str = "INFO"
    log_format: str = "json"
    api_keys: str = ""
    workers: int = 2
    worker_timeout: int = 600
    docling_num_threads: int = 2
    docling_device: str = "auto"
    docling_timeout_s: float | None = 500.0
    docling_max_num_pages: int = 300
    docling_max_file_size_mb: int = 25

    model_config = SettingsConfigDict(
        env_prefix="PDF_PARSER_",
        case_sensitive=False,
    )

    def get_api_keys_list(self) -> list[str]:
        """Parse comma-separated API keys into a list."""
        if not self.api_keys:
            return []
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]


settings = Settings()
