import pytest
from unittest.mock import patch

VALID_PAYLOAD = {
    "entity_type": "idea",
    "entity_id": "abc-123",
    "title": "My Idea",
    "description": "Full description here.",
    "ai_summary": None,
    "author": {"name": "Alice", "avatar_url": None},
    "status": "PUBLISHED",
    "stage": None,
    "tags": [],
    "like_count": 0,
    "view_count": 0,
    "comment_count": 0,
    "published_at": None,
    "linked_entities": [],
    "comments": [],
    "cover_image_url": None,
}


def test_generate_returns_download_url(client, tmp_path):
    with patch("app.routers.generate.render_pdf", return_value=b"%PDF-fake"):
        response = client.post(
            "/generate",
            json=VALID_PAYLOAD,
            headers={"Authorization": "Bearer internal-secret"},
        )
    assert response.status_code == 200
    data = response.json()
    assert "download_url" in data
    assert "/pdf/" in data["download_url"]
    assert "expires_at" in data


def test_generate_rejects_wrong_secret(client):
    response = client.post(
        "/generate",
        json=VALID_PAYLOAD,
        headers={"Authorization": "Bearer wrong-secret"},
    )
    assert response.status_code == 401


def test_generate_rejects_missing_auth(client):
    response = client.post("/generate", json=VALID_PAYLOAD)
    assert response.status_code == 401


def test_generate_rejects_invalid_payload(client):
    response = client.post(
        "/generate",
        json={"entity_type": "invalid"},
        headers={"Authorization": "Bearer internal-secret"},
    )
    assert response.status_code == 422
