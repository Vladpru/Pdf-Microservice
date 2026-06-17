import pytest
from app.schemas.payload import EntityPayload, GenerateResponse


def test_idea_payload_valid():
    payload = EntityPayload(
        entity_type="idea",
        entity_id="abc-123",
        title="My Idea",
        description="Some description",
        author={"name": "Alice", "avatar_url": None},
        status="PUBLISHED",
        stage=None,
        tags=[],
        like_count=0,
        view_count=0,
        comment_count=0,
        published_at=None,
        linked_entities=[],
        comments=[],
        cover_image_url=None,
        ai_summary=None,
    )
    assert payload.entity_type == "idea"


def test_entity_type_validation():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        EntityPayload(
            entity_type="invalid",
            entity_id="abc",
            title="T",
            description="D",
            author={"name": "A", "avatar_url": None},
            status="PUBLISHED",
            stage=None,
            tags=[],
            like_count=0,
            view_count=0,
            comment_count=0,
            published_at=None,
            linked_entities=[],
            comments=[],
            cover_image_url=None,
            ai_summary=None,
        )
