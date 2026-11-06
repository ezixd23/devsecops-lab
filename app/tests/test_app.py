import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from app import app

def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_security_headers():
    client = app.test_client()
    for path in ("/health", "/does-not-exist"):
        response = client.get(path)
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert "default-src 'none'" in response.headers["Content-Security-Policy"]
        assert response.headers["Cross-Origin-Resource-Policy"] == "same-origin"
