from langchain.schema import HumanMessage, AIMessage
import json, requests
import re
from core.model.schema import ChatState, StudentClassAllocationCreate
from llm.llm import llm
from config import API_URL

# --- Node 1: Intent Analysis ---
def intent_node_student_class_allocation(state: ChatState) -> ChatState:
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
        Table: StudentClassAllocation(id, student_id, student_class, class_section, reason)

        Valid intents:
        Table: student class allocation(id, student_id, student_class, class_section, reason)

        Valid intents:
        - create_student_class_allocation (requires student_id, student_class, class_section)
        - delete_student_class_allocation (requires student_class_allocation_id, reason)
        - update_student_class_allocation (requires student_class_allocationid, reason, student_id/student_class/class_section if given)

        Extract any parameters (student_id, student_class, class_section, student_class_allocation_id, reason) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_student_class_allocation", "params": {{"student_id": "STUD0001", "student_class": 10, "reason" : "new student"}}}}
        {{"intent": "update_student_class_allocation", "params": {{"student_id": "STUD0009", "student_class_allocation_id": "SCA0001"}}}}
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
def node_student_class_allocation(state: ChatState) -> ChatState:

    print("create node user")

    intent_value = str(state["intent"]).strip().lower()

    print(intent_value)

    parms_value = state["params"]

    match intent_value:        

        case "create_student_class_allocation":   

            required_keys = list(StudentClassAllocationCreate.model_fields.keys())  

            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.post(f"{API_URL}/studentclassallocation/", json=parms_value)
                reply = f"Created student class allocation." if res.status_code == 200 else "Failed to create student class allocation."
                response_data = res.json()
            else:
                reply = "data are inadequate to create student class allocation"
                response_data = "data are inadequate to student class allocation"
            
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
        
        case "delete_student_class_allocation":

            if "student_class_allocation_id" in parms_value:
                res = requests.delete(f"{API_URL}/studentclassallocation/{parms_value['student_class_allocation_id']}")
                reply = "student class allocation deleted." if res.status_code == 200 else "student class allocation not found."
                response_data = res.json()
            else:
                reply = "Need a student_class_allocation ID to delete."
                response_data = "Need a student_class_allocation ID to delete."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        
        case "update_student_class_allocation":

            if "student_class_allocation_id" in parms_value:
                res = requests.patch(f"{API_URL}/studentclassallocation/{parms_value['student_class_allocation_id']}", json=parms_value)
                reply = "student class allocation updated." if res.status_code == 200 else "student class allocation not found."
                response_data = res.json()
            else:
                reply = "Need student_class_allocation ID to update."
                response_data = "Need student_class_allocation ID to update."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
    
        case _: 
            response_data = "The student_class_allocation is not create/updated/deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=response_data)], "response": response_data}

