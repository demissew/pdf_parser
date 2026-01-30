import logging
from pathlib import Path

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI

from app.api.middleware import RequestLoggingMiddleware
from app.api.routes import router
from app.core.config import settings
from app.core.logging import setup_logging

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    # Setup logging before anything else
    setup_logging()

    # Disable docs in production (when API keys are configured)
    docs_url = None if settings.get_api_keys_list() else "/docs"
    redoc_url = None if settings.get_api_keys_list() else "/redoc"

    app = FastAPI(
        title=settings.app_name,
        docs_url=docs_url,
        redoc_url=redoc_url,
    )

    # Add middleware (order matters - correlation ID must be first)
    app.add_middleware(CorrelationIdMiddleware)
    app.add_middleware(RequestLoggingMiddleware)

    # Include routes
    app.include_router(router)

    # Create temp directory
    temp_dir = Path(settings.temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    # Log startup information
    logger.info(
        "Application started",
        extra={
            "app_name": settings.app_name,
            "log_level": settings.log_level,
            "log_format": settings.log_format,
            "temp_dir": settings.temp_dir,
            "max_upload_mb": settings.max_upload_mb,
            "docling_device": settings.docling_device,
            "auth_enabled": bool(settings.get_api_keys_list()),
            "docs_enabled": docs_url is not None,
        },
    )

    return app


app = create_app()
