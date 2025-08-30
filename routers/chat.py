from fastapi import APIRouter, Depends
from langchain.schema import HumanMessage, AIMessage
from core.graph.graph.graph_parent import parent_graph
from core.graph.graph.graph_performance import graph_performance
from sqlalchemy.orm import Session
from core.database.curd import save_chat, get_chat_history
from core.database.databse import get_db
from config import API_URL

router = APIRouter(prefix="/chat", tags=["chat"])
sessions = {}

@router.post("/")
def chat(session_id: str, message: str,  role : str, radio_action_on_person : str,
         db: Session = Depends(get_db)):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = parent_graph.invoke({"messages": history["messages"],
    "role": role,
    "radio_action_on_person": radio_action_on_person})
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role= role, user_msg=message, bot_reply=reply, db=db)
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
   # return {"reply": result['response'], "aireply" : reply}
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
   # return {"reply": result['response'], "aireply" : reply}
    return {"reply": result['response']}



@router.get("/history")
def fetch_chat_history(session_id: str, db: Session = Depends(get_db)):
    history = get_chat_history(session_id=session_id, db=db)
    return [{"user": h.user_msg, "bot": h.bot_reply} for h in history]


def chat(session_id: str, message: str, db: Session = Depends(get_db)):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = teacher_graph.invoke(history)
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    save_chat(session_id=session_id, role="teacher", user_msg=message, bot_reply=reply, db=db)
   # return {"reply": reply}
   # return {"reply": result['response'], "aireply" : reply}
    return {"reply": result['response']}