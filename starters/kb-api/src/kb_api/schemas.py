from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    path: str = Field(min_length=1, max_length=500, examples=["docs/solid_queue.md"])
    body: str
    tags: list[str] = []


class DocumentUpdate(BaseModel):
    """All fields optional: only the fields sent are changed (PATCH semantics)."""

    title: str | None = Field(default=None, min_length=1, max_length=200)
    body: str | None = None
    tags: list[str] | None = None


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # build from a SQLAlchemy object

    id: int
    title: str
    path: str
    body: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class DocumentPage(BaseModel):
    items: list[DocumentRead]
    next_cursor: int | None  # pass as ?after=... to get the next page
