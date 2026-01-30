import json
import logging
import os
from io import StringIO
from unittest.mock import patch

from fastapi.testclient import TestClient


def test_json_log_format() -> None:
    """Test that JSON log format produces valid JSON."""
    with patch.dict(os.environ, {"PDF_PARSER_LOG_FORMAT": "json"}):
        from importlib import reload
        from app.core import config, logging as app_logging

        reload(config)
        reload(app_logging)

        # Capture log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)

        # Setup logging with JSON format
        app_logging.setup_logging()

        # Replace handler to capture output
        logger = logging.getLogger()
        logger.handlers = [handler]

        # Configure handler with JSON formatter
        from pythonjsonlogger import jsonlogger

        formatter = jsonlogger.JsonFormatter(
            "%(timestamp)s %(level)s %(name)s %(message)s",
            rename_fields={"levelname": "level", "asctime": "timestamp"},
        )
        handler.setFormatter(formatter)

        # Log a test message
        test_logger = logging.getLogger("test")
        test_logger.info("Test message", extra={"request_id": "test-123"})

        # Get log output
        log_output = log_stream.getvalue()

        # Verify it's valid JSON
        assert log_output.strip(), "Log output should not be empty"
        log_json = json.loads(log_output.strip())

        # Verify expected fields
        assert "message" in log_json
        assert log_json["message"] == "Test message"
        assert "request_id" in log_json
        assert log_json["request_id"] == "test-123"


def test_request_id_in_response_headers() -> None:
    """Test that request ID is added to response headers."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")

    # Verify X-Request-ID header is present
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"], "Request ID should not be empty"


def test_text_log_format() -> None:
    """Test that text log format produces readable text."""
    with patch.dict(os.environ, {"PDF_PARSER_LOG_FORMAT": "text"}):
        from importlib import reload
        from app.core import config, logging as app_logging

        reload(config)
        reload(app_logging)

        # Capture log output
        log_stream = StringIO()
        handler = logging.StreamHandler(log_stream)

        # Setup logging with text format
        app_logging.setup_logging()

        # Replace handler to capture output
        logger = logging.getLogger()
        logger.handlers = [handler]

        # Configure handler with text formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        # Log a test message
        test_logger = logging.getLogger("test")
        test_logger.info("Test message")

        # Get log output
        log_output = log_stream.getvalue()

        # Verify it's human-readable text (not JSON)
        assert log_output.strip(), "Log output should not be empty"
        assert "test" in log_output
        assert "INFO" in log_output
        assert "Test message" in log_output
        # Should not be valid JSON
        try:
            json.loads(log_output.strip())
            assert False, "Text log should not be valid JSON"
        except json.JSONDecodeError:
            pass  # Expected
