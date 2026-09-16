from sqlalchemy.orm import Session

from app.models.chat import ChatSession,ChatMessage

class ChatRepository:
    def __init__(self,session:Session):
        self.session = session

    def get_session_by_id(self, id:int) -> ChatSession | None:
        return(
            self.session.query(ChatSession)
            .filter(ChatSession.id == id )
            .first()
        )
    def get_all_sessions(self, user_id: int) -> list[ChatSession] | None:
        return(
            self.session.query(ChatSession)
            .filter(ChatSession.user_id == user_id)
            .all() 
        )
    def get_messages_by_role(self, session_id: int, user_id: int, role: str) -> list[ChatMessage]:
                return (
                    self.session.query(ChatMessage)
                    .join(ChatSession, ChatMessage.session_id == ChatSession.id)
                    .filter(
                        ChatMessage.session_id == session_id,
                        ChatMessage.user_role == role,
                        ChatSession.user_id == user_id,
                    )
                    .all()
                )
    def get_message_by_id(self,id:int) ->ChatMessage | None:
        return(
            self.session.query(ChatMessage)
            .filter(ChatMessage.id == id)
            .first()

        )
    def add_chat_session(self,chat_session:ChatSession) -> ChatSession:
        self.session.add(chat_session)
        self.session.flush()

        return chat_session

    def add_chat_message(self,chat_message:ChatMessage) -> ChatMessage:
        self.session.add(chat_message)
        self.session.flush()

        return chat_message

    def commit(self):
        self.session.commit()
    