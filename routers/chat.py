from fastapi import APIRouter
from langchain.schema import HumanMessage, AIMessage
from core.graph.admin_graph import intent_graph
from core.graph.teacher_graph import teacher_graph

router = APIRouter(prefix="/chat", tags=["chat"])
sessions = {}

@router.post("/admin")
def chat(session_id: str, message: str):
    print("i am post/chat")
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    print("before chat invoke")
    result = intent_graph.invoke(history)
    print("after invoke chat post")
    sessions[session_id] = {"messages": result["messages"]}
    print("after sharing session_id in chat post")
    print(result['response'])
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    
    print(reply)
   # return {"reply": reply}
    return {"reply": result['response']}

@router.post("/teacher")
def chat(session_id: str, message: str):
    history = sessions.get(session_id, {"messages": []})
    history["messages"].append(HumanMessage(content=message))
    result = teacher_graph.invoke(history)
    sessions[session_id] = {"messages": result["messages"]}
    reply = [m for m in result["messages"] if isinstance(m, AIMessage)][-1].content
    
    print("teacher graph")
   # return {"reply": reply}
    return {"reply": result['response']}
