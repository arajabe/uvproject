from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import os, json, requests
import re
from core.model.schema import ChatState
from llm.llm import llm


API = "http://127.0.0.1:8000"


# --- Node 1: Intent Analysis ---

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


# --- Action Nodes (call FastAPI) ---

def node_parent(state: ChatState) -> ChatState:
    parms_value = state["params"]

    intent_value = state["intent"]

    match intent_value:
         
        case "create_parent" :
            if "name" in parms_value and "email" in parms_value:
                res = requests.post(f"{API}/parent/", json=parms_value)
                reply = f"Created parent {parms_value['name']}." if  res.status_code == 200 else "Failed to create parent."
                response_data = res.json()
            else:
                reply = "Need name and email."
                response_data = "Details not adequate to create parent"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
        
        case "delete_parent":
            if "parentid" in parms_value:
                res = requests.delete(f"{API}/parent/{parms_value['parentid']}")
                reply = "parent deleted." if res.status_code == 200 else "parent not found."
                response_data = res.json()
            else:
                reply = "Need a student ID to delete."
                response_data = "Since, no parent id, parent details are not deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        case "update_parent":
            if "parentid" in parms_value:
                res = requests.patch(f"{API}/parent/{parms_value['parentid']}", json=parms_value)
                reply = "parent updated." if res.status_code == 200 else "parent not found."
                response_data = res.json()
            else:
                response_data = {"error": "Provide parent id"}
                reply = "Since, no parent id, parent details not updated"

            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        case _:
            response_data = "Parent is notcreate/deleted/updated"
            return {**state, "messages": state["messages"] + [AIMessage(content=response_data)], "response" : response_data}

