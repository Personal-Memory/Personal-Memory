from fastapi import APIRouter, HTTPException, Query, status, Depends

from app.schemas.notes import NoteListRead, NoteRead, NoteCreate, SearchResult
from app.models.users import User
from app.services.notes import NoteService
from app.core.dependencies import get_note_service
from app.core.dependencies import get_current_user
from app.services.embeddings import EmbeddingError

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

@router.post(
    "",
    response_model=NoteRead,
    status_code=status.HTTP_201_CREATED,
)
def create_note(
    data: NoteCreate,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    try:
        return note_service.create_note(data, current_user)
    except EmbeddingError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not index the note, so nothing was saved. Please try again.",
        )

@router.get(
    "",
    response_model=list[NoteListRead],
    status_code=status.HTTP_200_OK,
)
def get_notes(
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
):
    return note_service.get_notes(current_user)

@router.get(
    "/search",
    response_model=list[SearchResult],
    status_code=status.HTTP_200_OK,
)
def search_notes(
    q: str = Query(..., min_length=1, max_length=500),
    limit: int = Query(5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service),
):
    try:
        return note_service.search(q, current_user, limit)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error))
    except EmbeddingError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Search is temporarily unavailable. Please try again.",
        )

@router.get(
    "/{note_id}",
    response_model=NoteRead,
    status_code=status.HTTP_200_OK,
)
def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    note_service: NoteService = Depends(get_note_service)
): 
    return note_service.get_note(note_id, current_user)