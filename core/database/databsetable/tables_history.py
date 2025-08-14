from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import CheckConstraint,UniqueConstraint
from sqlalchemy import Computed
from sqlalchemy import Column, Date
from core.database.databse import Base
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func, Text, DateTime


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    role = Column(String(24))
    user_msg = Column(Text)
    bot_reply = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)