import os
from unittest.mock import patch

from fastapi.testclient import TestClient


def test_health_check_no_auth() -> None:
    """Health check endpoint should not require authentication."""
    from app.main import app

    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_parse_endpoint_requires_auth_when_keys_configured() -> None:
    """Parse endpoints should require auth when API keys are configured."""
    with patch.dict(os.environ, {"PDF_PARSER_API_KEYS": "test-key-1,test-key-2"}):
        # Import app after patching environment
        from importlib import reload
        from app.core import config
        from app.api import auth
        from app import main

        reload(config)
        reload(auth)
        reload(main)

        client = TestClient(main.app)

        # Test without API key
        response = client.post("/parse/pdf", json={"url": "https://example.com/test.pdf"})
        assert response.status_code == 401
        assert "API key required" in response.json()["detail"]


def test_parse_endpoint_accepts_valid_key() -> None:
    """Parse endpoints should accept valid API key."""
    with patch.dict(os.environ, {"PDF_PARSER_API_KEYS": "test-key-1,test-key-2"}):
        from importlib import reload
        from app.core import config
        from app import main

        reload(config)
        reload(main)

        client = TestClient(main.app)

        # Test with valid API key (will fail for missing URL, but auth should pass)
        response = client.post(
            "/parse/pdf",
            json={"url": None},
            headers={"X-API-Key": "test-key-1"},
        )
        # Should not be 401, but 400 (bad request - missing URL)
        assert response.status_code == 400


def test_parse_endpoint_rejects_invalid_key() -> None:
    """Parse endpoints should reject invalid API key."""
    with patch.dict(os.environ, {"PDF_PARSER_API_KEYS": "test-key-1,test-key-2"}):
        from importlib import reload
        from app.core import config
        from app.api import auth
        from app import main

        reload(config)
        reload(auth)
        reload(main)

        client = TestClient(main.app)

        response = client.post(
            "/parse/pdf",
            json={"url": "https://example.com/test.pdf"},
            headers={"X-API-Key": "invalid-key"},
        )
        assert response.status_code == 401
        assert "Invalid API key" in response.json()["detail"]


def test_auth_disabled_when_no_keys() -> None:
    """Authentication should be disabled when no API keys are configured."""
    with patch.dict(os.environ, {"PDF_PARSER_API_KEYS": ""}, clear=False):
        from importlib import reload
        from app.core import config
        from app.api import auth
        from app import main

        reload(config)
        reload(auth)
        reload(main)

        client = TestClient(main.app)

        # Should proceed without API key (will fail for missing URL, but not auth)
        response = client.post("/parse/pdf", json={"url": None})
        assert response.status_code == 400  # Bad request, not 401
