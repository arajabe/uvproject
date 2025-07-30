from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import os, json, requests
import re


API = "http://127.0.0.1:8000"

class ChatState(TypedDict):
    messages: List
    intent: str
    params: dict

llm = ChatGroq(model="gemma2-9b-it", temperature=0, api_key="")

# --- Node 1: Intent Analysis ---
def intent_node(state: ChatState) -> ChatState:
    user_msg = state["messages"][-1].content
    prompt = f"""

        You are AI assistant, clarify the intenet of {user_msg} and work with testdb database.

        Classify the intent of: "{user_msg}". and create_user, delete_user,update_user, update_user and chat history in database testdb

        Database: testdb
        Table: users(id, name, email)

        Valid intents:
        - create_user (requires name, email)
        - delete_user (requires id)
        - update_user (requires id, name/email if given)
        - chat (free text, fallback if no DB action is needed)

        Extract any parameters (id, name, email) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_user", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        """
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
   
    print(ai_resp.content)

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()

    

    try:
        parsed = json.loads(raw_output)
        print(parsed)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}

# --- Node 2: Router ---
def router_node(state: ChatState) -> str:
    match state["intent"]:
        case "create_user": return "create_node"
        case "delete_user": return "delete_node"
        case "update_user": return "update_node"
        case _: return "chat_node"

# --- Action Nodes (call FastAPI) ---
def create_node(state: ChatState) -> ChatState:
    p = state["params"]
    print("i am create node")
    if "name" in p and "email" in p:
        r = requests.post(f"{API}/users/", json={"name": p["name"], "email": p["email"]})
        reply = f"Created user {p['name']}." if r.status_code == 200 else "Failed to create user."
    else:
        reply = "Need name and email."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}

def delete_node(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.delete(f"{API}/users/{p['id']}")
        reply = "User deleted." if r.status_code == 200 else "User not found."
    else:
        reply = "Need a user ID to delete."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}

def update_node(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.put(f"{API}/users/{p['id']}", json={"name": p.get("name"), "email": p.get("email")})
        reply = "User updated." if r.status_code == 200 else "User not found."
    else:
        reply = "Need user ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}

def chat_node(state: ChatState) -> ChatState:
    ai_reply = llm.invoke(state["messages"]).content
    return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)]}

# --- Graph ---
graph = StateGraph(ChatState)
graph.add_node("intent_node", intent_node)
graph.add_node("create_node", create_node)
graph.add_node("delete_node", delete_node)
graph.add_node("update_node", update_node)
graph.add_node("chat_node", chat_node)

graph.set_entry_point("intent_node")
graph.add_conditional_edges("intent_node", router_node, {
    "create_node": "create_node",
    "delete_node": "delete_node",
    "update_node": "update_node",
    "chat_node": "chat_node"
})
graph.add_edge("create_node", END)
graph.add_edge("delete_node", END)
graph.add_edge("update_node", END)
graph.add_edge("chat_node", END)

intent_graph = graph.compile()