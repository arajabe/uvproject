from fastapi import FastAPI
from routers import (chat, login)
from fastapi.middleware.cors import CORSMiddleware
from core.database.databse import Base, engine
from routers.allocation import classteacherallocation, studentclassallocation
from routers.analysis import performance
from routers.bulkmarkposting import bulk_subjecttermsplit,bulk_assignement,bulk_term_mark
from routers.info import officestaff, parent, student, teacher, users,password
from routers.marks import assignement, mark, subjecttermsplit
from routers.bulkallocations import bulk_class_teacher_allocations,bulk_student_class_allocations
from routers.bulkinformations import bulk_parent,bulk_officestaff,bulk_teacher,bulk_student
from routers.infochat import info_chat
from routers.logging_config import setup_logger
import logging
import uvicorn

# Setup logging for backend
#logger = setup_logger("backend")
logger = logging.getLogger("backend")


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="UV LangGraph API Framework")


# Allow frontend (React on 5173)
origins = [
    "http://localhost:57526",
    "http://127.0.0.1:57526",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(AuditMiddleware)

app.include_router(users.router)
app.include_router(chat.router)
app.include_router(student.router)
app.include_router(teacher.router)
app.include_router(parent.router)
app.include_router(mark.router)
app.include_router(performance.router)
app.include_router(login.router)
app.include_router(officestaff.router)
app.include_router(assignement.router)
app.include_router(subjecttermsplit.router)
app.include_router(studentclassallocation.router)
app.include_router(classteacherallocation.router)
app.include_router(bulk_subjecttermsplit.router)
app.include_router(bulk_assignement.router)
app.include_router(bulk_term_mark.router)
app.include_router(bulk_class_teacher_allocations.router)
app.include_router(bulk_student_class_allocations.router)
app.include_router(bulk_parent.router)
app.include_router(bulk_officestaff.router)
app.include_router(bulk_teacher.router)
app.include_router(bulk_student.router)
app.include_router(info_chat.router)
app.include_router(password.router)




@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"status": "running"}

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Backend started and logging initialized!")
