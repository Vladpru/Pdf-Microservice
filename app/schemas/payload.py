from typing import Literal, Optional
from pydantic import BaseModel
from datetime import datetime


class Author(BaseModel):
    name: str
    avatar_url: Optional[str] = None


class LinkedEntity(BaseModel):
    id: str
    title: str
    type: Literal["idea", "problem"]


class Comment(BaseModel):
    author: str
    body: str
    created_at: datetime


class EntityPayload(BaseModel):
    entity_type: Literal["idea", "problem"]
    entity_id: str
    title: str
    description: str
    ai_summary: Optional[str] = None
    author: Author
    status: str
    stage: Optional[str] = None
    tags: list[str] = []
    like_count: int = 0
    view_count: int = 0
    comment_count: int = 0
    published_at: Optional[datetime] = None
    linked_entities: list[LinkedEntity] = []
    comments: list[Comment] = []
    cover_image_url: Optional[str] = None


class GenerateResponse(BaseModel):
    download_url: str
    expires_at: datetime
