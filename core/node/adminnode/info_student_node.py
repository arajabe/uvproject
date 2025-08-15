from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import os, json, requests
import re
from core.model.schema import ChatState, StudentCreate
from llm.llm import llm


API = "http://127.0.0.1:8000"

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

# --- Action Nodes (call FastAPI) ---

def node_student(state: ChatState) -> ChatState:
    parms_value = state["params"]
    intent_value = state["intent"]

    match intent_value:

        case "create_student":
            required_keys = list(StudentCreate.model_fields.keys())
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                    res = requests.post(f"{API}/student/", json=parms_value)
                    reply = f"Created student {parms_value['name']}." if res.status_code == 200 else "Failed to create student."
                    response_data = res.json()
            else:
                    reply = "Need name and email."
                    response_data = "Data are inadequate, student not created"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
        
        case "delete_student":
            if "studentid" in parms_value:
                    res = requests.delete(f"{API}/student/{parms_value['studentid']}")
                    reply = "student deleted." if res.status_code == 200 else "student not found."
                    response_data = res.json()
            else:
                    reply = "Need a student ID to delete."
                    response_data = "Since, no student id, student details are not deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        
        case "update_student":
                if "studentid" in parms_value:
                    res = requests.patch(f"{API}/student/{parms_value['studentid']}", json=parms_value)
                    reply = "student updated." if res.status_code == 200 else "student not found."
                    response_data = res.json()
                else:
                    reply = "student ID to update."
                    response_data = "student not deleted"
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        case _:
              
              response_data = "student not created deleted or updated"
              return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
