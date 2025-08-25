from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import get_history
from core.utils.audit_helper import log_audit
from core.database.databsetable.tables_audit import Audit
USER_CONTEXT = {}

def set_audit_user(user_id: str):
    USER_CONTEXT["user_id"] = user_id

def get_audit_user() -> str:
    return USER_CONTEXT.get("user_id")

@event.listens_for(Session, "after_flush")
def after_flush(session, flush_context):
    user_id = get_audit_user()

    for obj in session.new:
        if isinstance(obj, Audit):  
            continue
        for col in obj.__table__.columns:
            new_val = getattr(obj, col.name)
            log_audit(session, user_id, obj.__tablename__, "CREATE", col.name, None, new_val)

    for obj in session.dirty:
        if isinstance(obj, Audit):
            continue
        for col in obj.__table__.columns:
            hist = get_history(obj, col.name)
            if hist.has_changes():
                old_val = hist.deleted[0] if hist.deleted else None
                new_val = hist.added[0] if hist.added else None
                log_audit(session, user_id, obj.__tablename__, "UPDATE", col.name, old_val, new_val)

    for obj in session.deleted:
        if isinstance(obj, Audit):
            continue
        for col in obj.__table__.columns:
            old_val = getattr(obj, col.name)
            log_audit(session, user_id, obj.__tablename__, "DELETE", col.name, old_val, None)