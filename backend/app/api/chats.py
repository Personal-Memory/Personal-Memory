from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_auth_service, get_current_user
from app.schemas.chats import ChatMessageCreate,ChatMessageRead

from app.services.chat import ChatService

from app.core.dependencies import get_current_user,get_chat_service
from app.services.auth import User 
router  = APIRouter(
    prefix = "/chats",
    tags = ["chats"]

)

@router.post(
    "",
    response_model = ChatMessageRead,
    status_code= status.HTTP_201_CREATED
)

def send_message(
    data:ChatMessageCreate,
    current_user : User = Depends(get_current_user),
    chat_service : ChatService = Depends(get_chat_service)
):
    try:
      return chat_service.send_message(data, current_user)
    except ValueError as e:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


    