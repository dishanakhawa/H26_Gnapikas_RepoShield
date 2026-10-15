
import sys
from pathlib import Path

import pytest
import requests

DEMO_REPO = Path(__file__).resolve().parents[1] / "demo_repo"
sys.path.insert(0, str(DEMO_REPO))

from app import get_status


def test_invalid_url_is_rejected():
    with pytest.raises(ValueError):
        get_status("not-a-valid-url")


def test_ftp_url_is_rejected():
    with pytest.raises(ValueError):
        get_status("ftp://example.com")


def test_http_url_is_accepted(monkeypatch):
    class FakeResponse:
        status_code = 200

    def fake_get(url, timeout):
        assert url == "https://example.com"
        assert timeout == 5
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    assert get_status("https://example.com") == 200


def test_timeout_error_is_reraised(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.Timeout("Request timed out")

    monkeypatch.setattr("app.requests.get", fake_get)

    with pytest.raises(requests.exceptions.Timeout):
        get_status("https://example.com")


def test_connection_error_is_reraised(monkeypatch):
    def fake_get(url, timeout):
        raise requests.exceptions.ConnectionError("Connection failed")

    monkeypatch.setattr("app.requests.get", fake_get)

    with pytest.raises(requests.exceptions.ConnectionError):
        get_status("https://example.com")
