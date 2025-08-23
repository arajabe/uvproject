from fastapi import APIRouter, Depends
from langchain.schema import HumanMessage, AIMessage
from core.graph.graph.graph_parent import office_staff_graph
from core.graph.graph.graph_performance import graph_performance
from sqlalchemy.orm import Session
from core.database.curd import save_chat, get_chat_history
from core.database.databse import get_db
import requests

API = "http://127.0.0.1:8000"

router = APIRouter(prefix="/chat", tags=["chat"])
sessions = {}

@router.post("/")
def chat(session_id: str, message: str,  role : str, radio_action_on_person : str,
         db: Session = Depends(get_db)):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = office_staff_graph.invoke({"messages": history["messages"],
    "role": role,
    "radio_action_on_person": radio_action_on_person})
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role="admin rara", user_msg=message, bot_reply=reply, db=db)
    return {"reply": result['response'], "aireply" : reply}
@router.post("/performance")
def chat(session_id: str, message: str, role : str, exam : str, performance_request : str, db: Session = Depends(get_db),):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = graph_performance.invoke({"messages":history["messages"], 
                                       "exam" : exam, 
                                       "performance_request" : performance_request,
                                       "role": role})
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role="teacher", user_msg=message, bot_reply=reply, db=db)
   # return {"reply": reply}
    print("teacher/admin called")
   # return {"reply": result['response'], "aireply" : reply}
    print("reply")
    
    return {"reply": result['response_pd']}

@router.post("/teacher")
def chat(session_id: str, message: str, db: Session = Depends(get_db)):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = teacher_graph.invoke(history)
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role="teacher", user_msg=message, bot_reply=reply, db=db)
   # return {"reply": reply}
    print("teacher/admin called")
   # return {"reply": result['response'], "aireply" : reply}
    print("reply")
    print(reply)
    return {"reply": result['response']}



@router.get("/history")
def fetch_chat_history(session_id: str, db: Session = Depends(get_db)):
    print("fetch_chat_history")
    history = get_chat_history(session_id=session_id, db=db)
    print(history)

    return [{"user": h.user_msg, "bot": h.bot_reply} for h in history]


def chat(session_id: str, message: str, db: Session = Depends(get_db)):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = teacher_graph.invoke(history)
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role="teacher", user_msg=message, bot_reply=reply, db=db)
   # return {"reply": reply}
    print("teacher/admin called")
   # return {"reply": result['response'], "aireply" : reply}
    print("reply")
    print(reply)
    return {"reply": result['response']}