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
    Task:
    Identify the exact intent from {msg} without inferring related meanings. Valid intents are: student, teacher, parent, officestaff
   
    Rules : 
        the message contains a direct mention of an intent

    - Output only valid JSON.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "parent"}}
        {{"intent": "teacher"}}
        """

    ai_resp = llm.invoke([HumanMessage(content=prompt)])   

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    
    print(raw_output)
    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat")}

def router_node(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    print("router node")
    print(x)
    match x:
        case "officestaff": return "intent_node_officestaff"
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

        Classify the intent of: "{user_msg}". and create_teacher, delete_teacher, update_teacher and chat history in database testdb

        Rules : 
            the message contains a direct mention of an intent

        Database: testdb
        Table: teacher(teacherid, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar,reason, graduatedegree, subject)

        Valid intents:
        - create_teacher (requires name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar, reason, graduatedegree, subject)
        - delete_teacher (requires teacherid, reason)
        - update_teacher (requires teacherid, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar/reason/graduatedegree/subject if given)

        Extract any parameters (teacherid, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar,reason, graduatedegree, subject) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_teacher", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        {{"intent": "update_teacher", "params": {{"name": "Bob", "email": "bob@x.com", "teacherid": "10", reason = "upgraded"}}}}
        {{"intent": "delete_teacher", "params": {{"teacherid": "10", reason="transfer"}}}}

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
def intent_node_officestaff(state: ChatState) -> ChatState:
    print("i am intent node user")
    user_msg = state["messages"][-1].content
    prompt = f"""

        You are AI assistant, clarify the intent of {user_msg} and work with testdb database.

        Classify the intent of: "{user_msg}". and create_officestaff, delete_officestaff,update_officestaff and chat history in database testdb

        Rules:
        the message contains a direct mention of an intent

        Database: testdb
        Table: OfficeStaff(id, name, email)

        Valid intents:
        Table: OfficeStaff(id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar, reason, role, graduatedegree, subject)

        Valid intents:
        - create_officestaff (requires name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar, reason, role, graduatedegree, subject)
        - delete_officestaff (requires officestaffid, reason)
        - update_officestaff (requires officestaffid, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar/graduatedegree/subject if given)

        Extract any parameters (parentid, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar, reason, role, graduatedegree, subject) mentioned.
        Extract any parameters (parentid, name, email) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_officestaff", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        {{"intent": "create_officestaff", "params": {{"name": "Bob", "email": "bob@x.com", "parentid": 10}}}}
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
        Table: student(id, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar, reason, parentid, parentrelation)

        Rules:
        The message contains a direct mention of an intent

        Valid intents:
        - create_student (requires name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar, reason, parentid, parentrelation)
        - delete_student (requires studentid, reason)
        - update_student (requires studentid, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar/reason/parentid/parentrelation if given)

        Extract any parameters (studentid, name, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, email, aadhar, reason, parentid, parentrelation) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_student", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        {{"intent": "create_student", "params": {{"name": "Bob", "email": "bob@x.com", "studentid": 10}}}}
        {{"intent": "delete_student", "params": {{"studentid": 10, reason: "transfer"}}}}
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

        Table: parent(name,email,fathername,mothername,dateofbirth,address,city,pincode,contactnumber,aadhar,reason,fatheroccupation,motheroccupation)

        Rules:
        The message contains a direct mention of an intent
        
        Valid intents:
        - create_parent (requires name, email, fathername, mothername, dateofbirth, address, city, pincode, contactnumber, aadhar, reason, fatheroccupation, motheroccupation)
        - delete_parent (requires parentid, reason)
        - update_parent (requires parentid and reason, name/fathername/mothername/dateofbirth/address/city/pincode/contactnumber/email/aadhar/fatheroccupation/motheroccupation if given)

        Extract any parameters (id,name,email,fathername,mothername,dateofbirth,address,city,pincode,contactnumber,aadhar,reason,fatheroccupation,motheroccupation) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_parent", "params": {{"name": "Bob", "email": "bob@x.com"}}}}
        {{"intent": "create_parent", "params": {{"name": "Bob", "email": none "parentid": "10}}}}
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
def router_node_officestaff(state: ChatState) -> str:
    print("router_node_user")
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_officestaff": return "create_node_officestaff"
        case "delete_officestaff": return "delete_node_officestaff"
        case "update_officestaff": return "update_node_officestaff"
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
def create_node_officestaff(state: ChatState) -> ChatState:

    print("create node user ")
    p = state["params"]
    if "name" in p and "email" in p:
        r = requests.post(f"{API}/officestaff/", json=p)
        reply = f"Created office staff {p['name']}." if r.status_code == 200 else "Failed to create office staff."
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
            reply = f"Created parent {p['name']}." if r.status_code == 200 else "Failed to create parent."
    else:
            reply = "Need name and email."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def create_node_teacher(state: ChatState) -> ChatState:
    p = state["params"]
    print("i am create_node_teacher")
    print(p)
    if "name" in p and "email" in p:
        r = requests.post(f"{API}/teacher/", json=p)
        reply = f"Created teacher {p['name']}." if r.status_code == 200 else "Failed to create teacher."
    else:
        reply = "Need name and email."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def delete_node_officestaff(state: ChatState) -> ChatState:
    p = state["params"]
    if "officestaffid" in p:
        r = requests.delete(f"{API}/officestaff/{p['officestaffid   ']}")
        reply = "office staff deleted." if r.status_code == 200 else "office staff not found."
    else:
        reply = "Need a officestaff ID to delete."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def delete_node_student(state: ChatState) -> ChatState:
    p = state["params"]
    if "studentid" in p:
        res = requests.delete(f"{API}/student/{p['studentid']}")
        reply = "student deleted." if r.status_code == 200 else "student not found."
        response_data = res.json()
    else:
        reply = "Need a student ID to delete."
        response_data = "Since, no student id, student details not updated"
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}

def delete_node_parent(state: ChatState) -> ChatState:
    p = state["params"]
    if "parentid" in p:
        res = requests.delete(f"{API}/parent/{p['parentid']}")
        reply = "parent deleted." if res.status_code == 200 else "parent not found."
        response_data = res.json()

    else:
        reply = "Need a student ID to delete."
        response_data = "Since, no parent id, parent details not updated"
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}

def delete_node_teacher(state: ChatState) -> ChatState:
    p = state["params"]
    if "teacherid" in p:
        r = requests.delete(f"{API}/teacher/{p['teacherid']}")
        reply = "teacher deleted." if r.status_code == 200 else "teacher not found."
    else:
        reply = "Need a teacher ID to delete."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_officestaff(state: ChatState) -> ChatState:
    p = state["params"]
    if "officestaffid" in p:
        r = requests.patch(f"{API}/officestaff/{p['officestaffid']}", json=p)
        reply = "office staff updated." if r.status_code == 200 else "User not found."
    else:
        reply = "Need office staff ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_student(state: ChatState) -> ChatState:
    p = state["params"]
    if "studentid" in p:
        r = requests.patch(f"{API}/student/{p['studentid']}", json=p)
        reply = "student updated." if r.status_code == 200 else "student not found."
    else:
        reply = "student ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def update_node_parent(state: ChatState) -> ChatState:
    p = state["params"]
    if "parentid" in p:
        res = requests.patch(f"{API}/parent/{p['parentid']}", json=p)
        reply = "parent updated." if res.status_code == 200 else "parent not found."
        response_data = res.json()
    else:
        response_data = {"error": "Provide parent id"}
        reply = "Since, no parent id, parent details not updated"

    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}

def update_node_teacher(state: ChatState) -> ChatState:
    p = state["params"]
    if "teacherid" in p:
        r = requests.patch(f"{API}/teacher/{p['teacherid']}", json=p)
        reply = "teacher updated." if r.status_code == 200 else "teacher not found."
    else:
        reply = "student ID to update."
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def chat_node(state: ChatState) -> ChatState:
    ai_reply = llm.invoke(state["messages"]).content
    print("chat node")
    #return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": AIMessage(content=ai_reply)}
    return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": {"hello":"This is irrelevant chat. we will assist you with student performance"}}