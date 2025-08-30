from sqlalchemy import event,delete
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import get_history
from core.utils.audit_helper import log_audit
from core.database.databsetable.tables_audit import Audit
from core.database.databsetable.tables_users import UserPasswordNew
USER_CONTEXT = {}

def set_audit_user(user_id: str):
    USER_CONTEXT["user_id"] = user_id

def get_audit_user() -> str:
    return USER_CONTEXT.get("user_id")

EXCLUDED_TABLES = {"audit", "chat_history"}  # 👈 add any table names to skip

@event.listens_for(Session, "after_flush")
def after_flush(session, flush_context):
    user_id = get_audit_user()

    for obj in session.new:
        if isinstance(obj, Audit) or obj.__tablename__ in EXCLUDED_TABLES:
            continue
        for col in obj.__table__.columns:
            new_val = getattr(obj, col.name)
            log_audit(session, user_id, obj.__tablename__, "CREATE", col.name, None, new_val)

    for obj in session.dirty:
        if isinstance(obj, Audit) or obj.__tablename__ in EXCLUDED_TABLES:
            continue
        for col in obj.__table__.columns:
            hist = get_history(obj, col.name)
            if hist.has_changes():
                old_val = hist.deleted[0] if hist.deleted else None
                new_val = hist.added[0] if hist.added else None
                log_audit(session, user_id, obj.__tablename__, "UPDATE", col.name, old_val, new_val)

    for obj in session.deleted:
        if isinstance(obj, Audit) or obj.__tablename__ in EXCLUDED_TABLES:
            continue
        for col in obj.__table__.columns:
            old_val = getattr(obj, col.name)
            log_audit(session, user_id, obj.__tablename__, "DELETE", col.name, old_val, None)
            
    for obj in session.deleted:
            if hasattr(obj, "__tablename__") and obj.__tablename__ in ["users", "student", "parent", "officestaff", "teacher"]:
                session.execute(
                    delete(UserPasswordNew).where(UserPasswordNew.id == obj.id)
            )
