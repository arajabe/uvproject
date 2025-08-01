from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from core.llm import llm
import os, json, requests
import re
from core.model.schema import ChatState


API = "http://127.0.0.1:8000"

def intent_node(state:ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""
You are an intent classification assistant. Your job is to classify a user message into one of the intent categories.
You are an AI assistant. Clarify the intent of this message: "{msg}".

Available intents:
- teacher: The user wants to perform create, read, update, or delete operations on teachers. Examples: "Add a new teacher", "Update John's phone number", "Delete teacher Mike", "Show me my teachers".
- user: The user wants to perform create, read, update, or delete operations on users. Examples: "Create a new user", "Get user info for ID 5", "Update user email", "Delete user 7".
- parents: The user wants to perform create, read, update, or delete operations on parents. Examples: "Create a new parent", "Get parent info for ID 5", "Update parent email", "Delete parent 7".
- others: If the user wants to perform create, read, update, or delete operations on something other than teacher, user, or parents.
- error : If the user wants to perform create, read, update, or delete operations like following Examples: "create raja", "delete 7" , "update phone number"

Only respond with one of the fiver values: "teacher", "user", "parents", "others", "error".
Do not add any explanation or extra text.

Examples:

Message: "Add a new teacher for John"
Intent: teacher

Message: {msg}
Intent:
""".strip()
    
    result = llm.invoke([HumanMessage(content=prompt)])
    print("intent node")
    print(result.content)
    # routing logic
    
    return{** state, "messages":state["messages"], "intent": result.content}
    
    
def intent_node_teacher(state: ChatState) -> ChatState:
 
    result = llm.invoke(state['messages']).content
    print(result)
    return{"messages" : state["messages"] + [AIMessage(content=result)], "response" : {"node" : "i am teacher intent node"}}

# --- Node 1: Intent Analysis ---
def intent_node_user(state: ChatState) -> ChatState:
    print("i am intent node user")
    user_msg = state["messages"][-1].content
    prompt = f"""

        You are AI assistant, clarify the intent of {user_msg} and work with testdb database.

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
        {{"intent": "create_user", "params": {{"name": "Bob", "email": "bob@x.com", "id": 10}}}}
        """
    print("before create_node invoke")
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
   
    print("after create_node invoke")

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    

    try:
        parsed = json.loads(raw_output)
        print(parsed)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}

def router_node(state: ChatState) -> str:
    print("i am router node")
    print(state["intent"])
    x = str(state["intent"]).strip().lower()
    print(type(x))
    if x == str("teacher"):
        return "intent_node_teacher"
    elif x == str("user"):
        return "intent_node_user"
    else:
        print("router chat node")
        return "chat_node"

    match x:
        case "contact" : return "intent_node_contact"
        case "user": return "intent_node_user"
        case _: 
            print(" hello chat user case")
            return "chat_node"

# --- Node 2: Router ---
def router_node_user(state: ChatState) -> str:
    match state["intent"]:
        case "create_user": return "create_node_user"
        case "delete_user": return "delete_node_user"
        case "update_user": return "update_node_user"
        case _: return "chat_node"

# --- Action Nodes (call FastAPI) ---
def create_node_user(state: ChatState) -> ChatState:
    p = state["params"]
   
    if "name" in p and "email" in p:
        print("before graph request post")
        r = requests.post(f"{API}/users/", json={"name": p["name"], "email": p["email"]})
        print("after graph request post")
        print(r.json())
        reply = f"Created user {p['name']}." if r.status_code == 200 else "Failed to create user."
    else:
        reply = "Need name and email."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def delete_node_user(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.delete(f"{API}/users/{p['id']}")
        reply = "User deleted." if r.status_code == 200 else "User not found."
    else:
        reply = "Need a user ID to delete."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_user(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.put(f"{API}/users/{p['id']}", json={"name": p.get("name"), "email": p.get("email")})
        reply = "User updated." if r.status_code == 200 else "User not found."
    else:
        reply = "Need user ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}

def chat_node(state: ChatState) -> ChatState:
    ai_reply = llm.invoke(state["messages"]).content
    print("chat node")
    #return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": AIMessage(content=ai_reply)}
    return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": {"hello":"i am chat node"}}