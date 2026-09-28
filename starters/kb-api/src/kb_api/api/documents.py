from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from kb_api.api.deps import SessionDep, require_api_key
from kb_api.models import Document
from kb_api.schemas import DocumentCreate, DocumentPage, DocumentRead, DocumentUpdate

router = APIRouter(prefix="/documents", tags=["documents"])
WriteAccess = Depends(require_api_key)


@router.get("", response_model=DocumentPage)
async def list_documents(
    session: SessionDep,
    after: Annotated[int | None, Query(description="cursor: last id of the previous page")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> DocumentPage:
    stmt = select(Document).order_by(Document.id).limit(limit + 1)  # one extra to know if there is more
    if after is not None:
        stmt = stmt.where(Document.id > after)
    rows = list((await session.scalars(stmt)).all())
    has_more = len(rows) > limit
    items = rows[:limit]
    return DocumentPage(
        items=[DocumentRead.model_validate(d) for d in items],
        next_cursor=items[-1].id if has_more else None,
    )


@router.get("/{document_id}", response_model=DocumentRead)
async def get_document(document_id: int, session: SessionDep) -> Document:
    document = await session.get(Document, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail=f"Document {document_id} not found")
    return document


@router.post("", response_model=DocumentRead, status_code=status.HTTP_201_CREATED, dependencies=[WriteAccess])
async def create_document(payload: DocumentCreate, session: SessionDep) -> Document:
    document = Document(**payload.model_dump())
    session.add(document)
    try:
        await session.commit()
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=409, detail=f"A document with path {payload.path!r} exists") from None
    await session.refresh(document)
    return document


@router.patch("/{document_id}", response_model=DocumentRead, dependencies=[WriteAccess])
async def update_document(document_id: int, payload: DocumentUpdate, session: SessionDep) -> Document:
    document = await get_document(document_id, session)
    for field, value in payload.model_dump(exclude_unset=True).items():  # only fields the client sent
        setattr(document, field, value)
    await session.commit()
    await session.refresh(document)
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[WriteAccess])
async def delete_document(document_id: int, session: SessionDep) -> Response:
    document = await get_document(document_id, session)
    await session.delete(document)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
