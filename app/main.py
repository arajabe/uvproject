from fastapi import FastAPI
from routers import (users, studentclassallocation,classteacherallocation,
                     chat, student,teacher, parent, mark, 
                     performance,login, officestaff, assignement, subjecttermsplit, bulk_subjecttermsplit)
from fastapi.middleware.cors import CORSMiddleware
from core.database.databse import Base, engine


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

@app.get("/")
def root():
    return {"status": "running"}