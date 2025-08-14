from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import os, json, requests
import re
from core.model.schema import ChatState
from llm.llm import llm


API = "http://127.0.0.1:8000"


# --- Node 1: Intent Analysis ---
def intent_node_officestaff(state: ChatState) -> ChatState:
    print("intent_node_officestaff")
    user_msg = state["messages"][-1].content
    role = state["role"]
    radio_action_on_person = state["radio_action_on_person"]
    print(role+ "_" + radio_action_on_person.replace(" ", "_"))
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
        {{"intent": "update_officestaff", "params": {{"name": "Bob", "email": "bob@x.com", "officestaffid": 10}}}}
        """
  
    ai_resp = llm.invoke([HumanMessage(content=prompt)])

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    

    try:
        parsed = json.loads(raw_output)
        print(parsed)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}


# --- Action Nodes (call FastAPI) ---
def node_officestaff(state: ChatState) -> ChatState:

    print("create node user")

    intent_value = str(state["intent"]).strip().lower()

    print(intent_value)

    parms_value = state["params"]

    match intent_value:
        case "create_officestaff":            
            
            if "name" in parms_value and "email" in parms_value:
                res = requests.post(f"{API}/officestaff/", json=parms_value)
                reply = f"Created office staff {parms_value['name']}." if res.status_code == 200 else "Failed to create office staff."
                response_data = res.json()
            else:
                reply = "Need name and email."
            
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : res.json()}
        
        case "delete_officestaff":
            if "officestaffid" in parms_value:
                res = requests.delete(f"{API}/officestaff/{parms_value['officestaffid']}")
                reply = "office staff deleted." if res.status_code == 200 else "office staff not found."
                response_data = res.json()
            else:
                reply = "Need a officestaff ID to delete."
                response_data = "Need a officestaff ID to delete."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": res.json()}
        
        case "update_officestaff":

            if "officestaffid" in parms_value:
                res = requests.patch(f"{API}/officestaff/{parms_value['officestaffid']}", json=parms_value)
                reply = "office staff updated." if res.status_code == 200 else "Office staff not found."
                response_data = res.json()
            else:
                reply = "Need office staff ID to update."
                response_data = "Need office staff ID to update."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
    
        case _: 
            response_data = "The office staff is not create/updated/deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=response_data)], "response": response_data}

