from fastapi import FastAPI
from routers import users, chat, student
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/")
def root():
    return {"status": "running"}