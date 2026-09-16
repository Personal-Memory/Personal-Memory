from app.models.chat import ChatMessage,ChatSession
from app.repositories.chats import ChatRepository
from app.schemas.chats import ChatMessageCreate,ChatMessageRead,GetAllSessionMessagesByRole
from app.models.users import User

class ChatService:
    def __init__(self,chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def send_message(self, data: ChatMessageCreate,current_user: User)-> ChatMessageRead:
        if data.session_id is None:
            new_session = ChatSession(
                user_id = current_user.id,
                title= "New Chat"


            )
            new_session = self.chat_repository.add_chat_session(new_session)
            self.chat_repository.commit()
            session_id = new_session.id
        else:
              session_id = data.session_id
              existing_session = self.chat_repository.get_session_by_id(session_id)
            
              if existing_session is None:
                    raise ValueError("Chat session not found")
            
              if existing_session.user_id != current_user.id:
                    raise ValueError("This chat session does not belong to you")
        
  

        new_message = ChatMessage(
            user_role = data.user_role,
            content =data.content,
            session_id = session_id

        )

        new_message = self.chat_repository.add_chat_message(new_message)
        self.chat_repository.commit()

        return new_message

    def get_messages_by_role(self, data:GetAllSessionMessagesByRole, current_user: User) -> list[ChatMessage]:

         messages = self.chat_repository.get_messages_by_role(data.session_id, current_user.id, data.user_role)

         if messages is None:
              raise ValueError("No message is found for this User under this chat session!")
         
         return messages

    def get_all_sessions(self, current_user:User) -> list[ChatSession]:
         all_sessions = self.chat_repository.get_all_sessions(current_user.id)

         if all_sessions  is None:
              raise ValueError("No past chat session found for this User!")
         return  all_sessions
         

        