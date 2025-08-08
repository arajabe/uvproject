from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import os, json, requests
import re
from core.model.schema import ChatState
from llm.llm import llm


API = "http://127.0.0.1:8000"

def intent_node(state:ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""

        You are AI assistant, clarify the intent of {msg} and work with testdb database.

        clarify the intent of :student, teacher, parent, officestaff, others

        Extract intent mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "parent"}}
        {{"intent": "teacher"}}
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
    return {**state, "intent": parsed.get("intent", "chat")}

def router_node(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    print("router node")
    print(x)
    match x:
        case "officestaff": return "intent_node_user"
        case "student": return "intent_node_student"
        case "parent": return "intent_node_parent"
        case "teacher": return "intent_node_teacher"
        case _: 
            print(" hello chat user case")
            return "chat_node"
    
    
def intent_node_teacher(state: ChatState) -> ChatState:
 
    print("i am intent node teacher")
    user_msg = state["messages"][-1].content
    prompt = f"""

        You are AI assistant, clarify the intent of {user_msg} and work with testdb database.

        Classify the intent of: "{user_msg}". and create_teacher, delete_teacher, update_teacher, update_teacher and chat history in database testdb

        Database: testdb
        Table: teacher(id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)

        Valid intents:
        - create_teacher (requires name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)
        - delete_teacher (requires id)
        - update_teacher (requires id, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar if given)

        Extract any parameters (id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_teacher", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        {{"intent": "create_teacher", "params": {{"name": "Bob", "email": "bob@x.com", "id": 10}}}}
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
        Table: users(id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)

        Valid intents:
        - create_user (requires name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)
        - delete_user (requires id)
        - update_user (requires id, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar if given)

        Extract any parameters (id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar) mentioned.
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

# --- Node 1: Intent Analysis ---
def intent_node_student(state: ChatState) -> ChatState:
    print("intent_node_student")
    user_msg = state["messages"][-1].content
    create_prompt = f"""

        You are AI assistant, clarify the intent of {user_msg}.
        Database: testdb
        Table: student(id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)

        Valid intents:
        - create_student (requires name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)
        - delete_student (requires id)
        - update_student (requires id, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar if given)

        Extract any parameters (id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_student", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        {{"intent": "create_student", "params": {{"name": "Bob", "email": "bob@x.com", "id": 10}}}}
        """
    print("before create_node invoke")
    ai_resp = llm.invoke([HumanMessage(content=create_prompt)])
   
    print("after create_node invoke")

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()   
    print("raw_output") 
    print(raw_output)

    try:
        parsed = json.loads(raw_output)
        print(parsed)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}

def intent_node_parent(state: ChatState) -> ChatState:
    print("intent_node_parent")
    user_msg = state["messages"][-1].content
    prompt = f"""

        You are AI assistant, clarify the intent of {user_msg}.

        Table: parent(id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)

        Valid intents:
        - create_parent (requires name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar)
        - delete_parent (requires id)
        - update_parent (requires id, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar if given)

        Extract any parameters (id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_parent", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        {{"intent": "create_parent", "params": {{"name": "Bob", "email": "bob@x.com", "id": 10}}}}
        """
    print("before create_node invoke")
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
   
    print("after create_node invoke")

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()   
    print("raw_output") 
    print(raw_output)

    try:
        parsed = json.loads(raw_output)
        print(parsed)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}



# --- Node 2: Router ---
def router_node_user(state: ChatState) -> str:
    print("router_node_user")
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_user": return "create_node_user"
        case "delete_user": return "delete_node_user"
        case "update_user": return "update_node_user"
        case _: return "chat_node"

def router_node_student(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_student": return "create_node_student"
        case "delete_student": return "delete_node_student"
        case "update_student": return "update_node_student"
        case _: return "chat_node"


def router_node_parent(state: ChatState) -> str:
    print("router node parent")
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_parent": return "create_node_parent"
        case "delete_parent": return "delete_node_parent"
        case "update_parent": return "update_node_parent"
        case _: return "chat_node"


def router_node_teacher(state: ChatState) -> str:

    print("routher node teacher")
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_teacher": return "create_node_teacher"
        case "delete_teacher": return "delete_node_teacher"
        case "update_teacher": return "update_node_teacher"
        case _: return "chat_node"

# --- Action Nodes (call FastAPI) ---
def create_node_user(state: ChatState) -> ChatState:

    print("create node user ")
    p = state["params"]
    if "name" in p and "email" in p:
        r = requests.post(f"{API}/users/", json=p)
        reply = f"Created user {p['name']}." if r.status_code == 200 else "Failed to create Teacher."
    else:
        reply = "Need name and email."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def create_node_student(state: ChatState) -> ChatState:
    p = state["params"]
    if "name" in p and "email" in p:
        r = requests.post(f"{API}/student/", json=p)
        reply = f"Created student {p['name']}." if r.status_code == 200 else "Failed to create student."
    else:
        reply = "Need name and email."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def create_node_parent(state: ChatState) -> ChatState:
    p = state["params"]
    if "name" in p and "email" in p:
            r = requests.post(f"{API}/parent/", json=p)
            reply = f"Created parent {p['name']}." if r.status_code == 200 else "Failed to create student."
    else:
            reply = "Need name and email."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def create_node_teacher(state: ChatState) -> ChatState:
    p = state["params"]
    print("i am create_node_teacher")
    print(p)
    if "name" in p and "email" in p:
        r = requests.post(f"{API}/teacher/", json=p)
        reply = f"Created teacher {p['name']}." if r.status_code == 200 else "Failed to create student."
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

def delete_node_student(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.delete(f"{API}/student/{p['id']}")
        reply = "student deleted." if r.status_code == 200 else "student not found."
    else:
        reply = "Need a student ID to delete."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def delete_node_parent(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.delete(f"{API}/parent/{p['id']}")
        reply = "parent deleted." if r.status_code == 200 else "parent not found."
    else:
        reply = "Need a student ID to delete."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def delete_node_teacher(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.delete(f"{API}/teacher/{p['id']}")
        reply = "teacher deleted." if r.status_code == 200 else "parent not found."
    else:
        reply = "Need a teacher ID to delete."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_user(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.put(f"{API}/users/{p['id']}", json={"name": p.get("name"), "email": p.get("email")})
        reply = "User updated." if r.status_code == 200 else "User not found."
    else:
        reply = "Need user ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_student(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.put(f"{API}/student/{p['id']}", json={"name": p.get("name"), "email": p.get("email")})
        reply = "student updated." if r.status_code == 200 else "student not found."
    else:
        reply = "student user ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_parent(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.put(f"{API}/parent/{p['id']}", json={"name": p.get("name"), "email": p.get("email")})
        reply = "parent updated." if r.status_code == 200 else "parent not found."
    else:
        reply = "student user ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_teacher(state: ChatState) -> ChatState:
    p = state["params"]
    if "id" in p:
        r = requests.put(f"{API}/teacher/{p['id']}", json={"name": p.get("name"), "email": p.get("email")})
        reply = "teacher updated." if r.status_code == 200 else "teacher not found."
    else:
        reply = "student user ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def chat_node(state: ChatState) -> ChatState:
    ai_reply = llm.invoke(state["messages"]).content
    print("chat node")
    #return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": AIMessage(content=ai_reply)}
    return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": {"hello":"This is irrelevant chat. we will assist you with student performance"}}