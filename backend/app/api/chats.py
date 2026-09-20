from fastapi import APIRouter, Depends, HTTPException, status
from app.core.dependencies import get_auth_service, get_current_user
from app.schemas.chats import ChatMessageCreate,ChatMessageRead,GetAllSessionRead
from app.services.chat import ChatService
from app.models.chat import ChatMessage

from app.core.dependencies import get_current_user,get_chat_service
from app.services.auth import User 
router  = APIRouter(
    prefix = "/chats",
    tags = ["Chats"]

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

@router.get(
   "/messages/{session_id}/{role}",
   response_model =  list[ChatMessageRead]
)

def get_all_message(
   session_id : int,
   role: str,
   current_user : User = Depends(get_current_user),
   chat_service : ChatService = Depends(get_chat_service)
):
   try:
     return chat_service.get_messages_by_role(session_id,role,current_user) 
   except ValueError as e:
      raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = str(e))   


@router.get(
   "/sessions", 
   response_model =list[GetAllSessionRead]
)
def get_all_sessions(
   current_user : User = Depends(get_current_user),
   chat_service : ChatService = Depends(get_chat_service)
   ):
    try:
       return  chat_service.get_all_sessions(current_user)
    except ValueError as e:
       raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, deatil = str(e))
   