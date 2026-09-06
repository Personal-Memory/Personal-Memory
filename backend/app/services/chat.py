from app.models.chat import ChatMessage,ChatSession
from app.repositories.chats import ChatRepository
from app.schemas.chats import ChatSessionCreate,ChatMessageCreate

class ChatService:
    def __init__(self,chat_repository: ChatRepository):
        self.chat_repository = chat_repository

    def send_message(self, data: ChatMessageCreate,chat_session:ChatSessionCreate)-> ChatMessage:
        if chat_session.session_id is None:
            new_session = ChatSession(
                title= chat_session.title

            )
            new_session = self.chat_repository.add_chat_session(new_session)
            self.chat_repository.commit()

        session_id =chat_session.session_id 

        new_message = ChatMessage(
            user_role = data.user_role,
            content =data.content,
            session_id = session_id,
        )

        new_message = self.chat_repository.add_chat_message(new_message)
        self.chat_repository.commit()

        return new_message

        