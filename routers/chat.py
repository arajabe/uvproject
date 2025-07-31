from fastapi import APIRouter
from langchain.schema import HumanMessage, AIMessage
from core.graph import intent_graph

router = APIRouter(prefix="/chat", tags=["chat"])
sessions = {}

@router.post("/")
def chat(session_id: str, message: str):
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
