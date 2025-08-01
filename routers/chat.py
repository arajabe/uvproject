from fastapi import APIRouter, Depends
from langchain.schema import HumanMessage, AIMessage
from core.graph.admin_graph import intent_graph
from core.graph.teacher_graph import teacher_graph
from sqlalchemy.orm import Session
from core.db.curd import save_chat, get_chat_history
from core.db.db import get_db

router = APIRouter(prefix="/chat", tags=["chat"])
sessions = {}

@router.post("/admin")
def chat(session_id: str, message: str, db: Session = Depends(get_db)):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = intent_graph.invoke(history)
    print(result)
    sessions[session_id] = {"messages": result["messages"]}
    print(result['response'])
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role="admin", user_msg=message, bot_reply=reply, db=db)
    print(reply)
   # return {"reply": reply}
    return {"reply": result['response'], "aireply" : reply}

@router.post("/teacher")
def chat(session_id: str, message: str, db: Session = Depends(get_db)):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = teacher_graph.invoke(history)
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role="teacher", user_msg=message, bot_reply=reply, db=db)
    print("teacher graph")
   # return {"reply": reply}
    return {"reply": result['response']}

@router.post("/history")
def chat(session_id: str, message: str, db: Session = Depends(get_db)):
    # Call your intent_graph or logic
    reply = "Simulated reply from LLM or LangGraph"  # Replace with real output
    print("Simulated reply from LLM or LangGraph")

    save_chat(session_id=session_id, role="student", user_msg=message, bot_reply=reply, db=db)
    history = get_chat_history(session_id=session_id, db=db)
    print(history)
    return {"reply": reply}

@router.get("/history")
def fetch_chat_history(session_id: str, db: Session = Depends(get_db)):
    print("fetch_chat_history")
    history = get_chat_history(session_id=session_id, db=db)
    print(history)

    return [{"user": h.user_msg, "bot": h.bot_reply} for h in history]
