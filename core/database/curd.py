from sqlalchemy.orm import Session
from core.database.databsetable.tables_history import ChatHistory

def save_chat(session_id: str, role: str, user_msg: str, bot_reply: str, db: Session):
    chat = ChatHistory(
        session_id=session_id,
        role=role,
        user_msg=user_msg,
        bot_reply=bot_reply
    )
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def get_chat_history(session_id: str, db: Session):
    return db.query(ChatHistory).filter(ChatHistory.session_id == session_id).order_by(ChatHistory.timestamp).all()