import pytest
from datetime import datetime, timezone
from app.services.pdf import render_pdf
from app.schemas.payload import EntityPayload, Author


def _make_payload(entity_type="idea"):
    return EntityPayload(
        entity_type=entity_type,
        entity_id="test-id",
        title="Test Title",
        description="Test description content.",
        ai_summary="AI generated summary.",
        author=Author(name="Alice", avatar_url=None),
        status="PUBLISHED",
        stage="PROTOTYPING",
        tags=["tag1", "tag2"],
        like_count=5,
        view_count=100,
        comment_count=2,
        published_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
        linked_entities=[],
        comments=[],
        cover_image_url=None,
    )


def test_render_idea_returns_bytes(set_env):
    result = render_pdf(_make_payload("idea"))
    assert isinstance(result, bytes)
    assert len(result) > 1000
    assert result[:4] == b"%PDF"


def test_render_problem_returns_bytes(set_env):
    result = render_pdf(_make_payload("problem"))
    assert isinstance(result, bytes)
    assert result[:4] == b"%PDF"
