from sqlalchemy.orm import Session
from core.db.db import Mark, Student
from sqlalchemy import event
from sqlalchemy.orm import Session
from core.model.schema import MarkCreate

@event.listens_for(MarkCreate, "before_insert")
@event.listens_for(MarkCreate, "before_update")
def populate_student_name(mapper, db : Session, target):
    print("populate_student_name")
    student = db.query(Student).filter(Student.id == target.student_id).first()
    if student:
        target.student_name = student.name
    db.close()