import pytest
from datetime import datetime, timezone

try:
    from weasyprint import HTML  # noqa: F401
    _weasyprint_available = True
except (ImportError, OSError):
    _weasyprint_available = False

skip_no_weasyprint = pytest.mark.skipif(
    not _weasyprint_available,
    reason="WeasyPrint system libraries (pango/gobject) not available in this environment",
)

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


@skip_no_weasyprint
def test_render_idea_returns_bytes(set_env):
    from app.services.pdf import render_pdf
    result = render_pdf(_make_payload("idea"))
    assert isinstance(result, bytes)
    assert len(result) > 1000
    assert result[:4] == b"%PDF"


@skip_no_weasyprint
def test_render_problem_returns_bytes(set_env):
    from app.services.pdf import render_pdf
    result = render_pdf(_make_payload("problem"))
    assert isinstance(result, bytes)
    assert result[:4] == b"%PDF"
