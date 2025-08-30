from langchain.schema import HumanMessage, AIMessage
import json, requests
import re
from core.model.schema import ChatState, ClassTeacherAllocationCreate
from llm.llm import llm
from config import API_URL

# --- Node 1: Intent Analysis ---
def intent_class_teacher_allocation(state: ChatState) -> ChatState:
    user_msg = state["messages"][-1].content
    role = state["role"]
    radio_action_on_person = state["radio_action_on_person"]
    prompt = f"""

        You are AI assistant, clarify the intent of {user_msg} and work with testdb database.

        Classify the intent of: "{user_msg}". and create_class_teacher_allocation, delete_class_teacher_allocation,update_class_teacher_allocation
        
        Rules:
        the message contains a direct mention of an intent

        Database: testdb
        Table: ClassTeacherAllocation(id, teacher_id, teacher_class, class_section, rason)

        Valid intents:
        Table: classteacherallocation(teacher_id, teacher_class, class_section, reason, class_teacher_allocation_id)

        Valid intents:
        - create_class_teacher_allocation (requires teacher_id, teacher_class, class_section)
        - delete_class_teacher_allocation (requires class_teacher_allocation_id, reason)
        - update_class_teacher_allocation (requires class_teacher_allocation_id, reason, teacher_id/teacher_class/class_section if given)

        Extract any parameters (teacher_id, teacher_class, class_section, reason, class_teacher_allocation_id) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_class_teacher_allocation", "params": {{"teacher_id": TEA0001, "teacher_class": 10, "class_section" : "B" }}}}
        {{"intent": "update_class_teacher_allocation", "params": {{"class_teacher_allocation_id": "CTA0001", "teacher_id": TEA0001, "class_section" : "B" , "rason": "any}}}}
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
def node_class_teacher_allocation(state: ChatState) -> ChatState:

    intent_value = str(state["intent"]).strip().lower()
    parms_value = state["params"]

    match intent_value:        

        case "create_class_teacher_allocation":   

            required_keys = list(ClassTeacherAllocationCreate.model_fields.keys())       
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.post(f"{API_URL}/classteacherallocation/", json=parms_value)
                reply = f"Created class teacher allocation" if res.status_code == 200 else "Failed to create class teacher allocation."
                response_data = res.json()
            else:
                reply = "data are inadequate to create class teacher allocation"
                response_data = "data are inadequate to create class teacher allocation"
            
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
        
        case "delete_class_teacher_allocation":

            if "class_teacher_allocation_id" in parms_value:
                res = requests.delete(f"{API_URL}/classteacherallocation/{parms_value['class_teacher_allocation_id']}")
                reply = "class teacher allocation deleted." if res.status_code == 200 else "class teacher allocation not found."
                response_data = res.json()
            else:
                reply = "Need a class teacher allocation ID to delete."
                response_data = "Need a class teacher allocation ID to delete."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        
        case "update_class_teacher_allocation":

            if "class_teacher_allocation_id" in parms_value:
                res = requests.patch(f"{API_URL}/classteacherallocation/{parms_value['class_teacher_allocation_id']}", json=parms_value)
                reply = "class teacher allocation updated." if res.status_code == 200 else "class teacher allocation id not found."
                response_data = res.json()
            else:
                reply = "Need class teacher allocation ID to update."
                response_data = "Need class teacher allocation ID to update."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
    
        case _: 
            response_data = "The class teacher allocation is not create/updated/deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=response_data)], "response": response_data}

