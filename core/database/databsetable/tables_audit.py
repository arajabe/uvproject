from sqlalchemy import Column,String, DateTime
from datetime import datetime
from sqlalchemy import Column
from core.database.databse import Base


class Audit(Base):
    __tablename__ = "audit_table"
    id = Column(String(50), primary_key= True, index= True)
    user_id = Column(String(50), index = True)
    table_name = Column(String(50), index = True)
    status = Column(String(50), index = True)
    field_name = Column(String(50), index = True)
    old_value = Column(String(500), index = True)
    new_value = Column(String(500), index = True)
    timestamp = Column(DateTime, default=datetime.utcnow)


