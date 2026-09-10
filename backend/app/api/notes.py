from fastapi import APIRouter, status, Depends

from app.schemas.notes import NoteListRead, NoteRead, NoteCreate
from app.models.users import User
from app.services.notes import NoteService
from app.core.dependencies import get_note_service
from app.core.dependencies import get_current_user

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
    return note_service.create_note(data, current_user)

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