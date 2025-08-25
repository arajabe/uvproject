import uuid
from sqlalchemy.orm import Session
from core.database.databsetable.tables_audit import Audit

def log_audit(
    db: Session,
    user_id: str,
    table_name: str,
    status: str,
    field_name: str,
    old_value: str,
    new_value: str,
):
    audit = Audit(
        id=str(uuid.uuid4()),
        user_id=user_id,
        table_name=table_name,
        status=status,
        field_name=field_name,
        old_value=str(old_value) if old_value is not None else None,
        new_value=str(new_value) if new_value is not None else None,
    )
    db.add(audit)