from langchain.schema import HumanMessage, AIMessage
import json, requests
import re
from core.model.schema import ChatState, TeacherCreate
from llm.llm import llm
from config import API_URL

# --- Node 1: Intent Analysis ---
def intent_node_teacher(state: ChatState) -> ChatState:

    user_msg = state["messages"][-1].content
    role = state["role"]
    radio_action_on_person = state["radio_action_on_person"]

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
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    

    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}

# --- Action Nodes (call FastAPI) ---

def node_teacher(state: ChatState) -> ChatState:
    intent_value = state["intent"]
    parms_value = state["params"]

    match intent_value:
        case "create_teacher":
            required_keys = list(TeacherCreate.model_fields.keys())
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.post(f"{API_URL}/teacher/", json=parms_value)
                reply = f"Created teacher {parms_value['name']}." if res.status_code == 200 else "Failed to create teacher."
                response_data = res.json()
            else:
                reply = "Need name and email."
                response_data = "Datas are inadequate to create teacher"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
        
        case "delete_teacher":
            if "teacherid" in parms_value:
                res = requests.delete(f"{API_URL}/teacher/{parms_value['teacherid']}")
                reply = "teacher deleted." if res.status_code == 200 else "teacher not found."
                response_data = res.json()

            else:
                reply = "Need a student ID to delete."
                response_data = "Since, no teacher id, teacher details not deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        
        case "update_teacher":
            if "teacherid" in parms_value:
                res = requests.patch(f"{API_URL}/teacher/{parms_value['teacherid']}", json=parms_value)
                reply = "teacher updated." if res.status_code == 200 else "teacher not found."
                response_data = res.json()
            else:
                reply = "Teacher ID to not update."
                response_data = "teacher ID to not update"
        
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
        case _:
            response_data = "teacher not created, updated, deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=response_data )], "response": response_data }