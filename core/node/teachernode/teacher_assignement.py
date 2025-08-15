from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from llm.llm import llm
import os, json, requests
import re
from core.model.schema import ChatState,AssignementCreate

API = "http://127.0.0.1:8000"

def intent_node_assignement(state:ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""
You are an intent classification assistant. Your job is to classify a user message into one of the intent categories.
You want the AI assistant to analyze a message ({msg}) and determine the intent, specifically in the context of student academic data — like subject-wise marks, performance, or term results.

Rules : 
 the message contains a direct mention of an intent

Available intents:
- create_assignement: The user wants to perform create operations on assignement. Examples: "create assignement details as follows".
- update_assignement: The user wants to perform update operations on assignement. Examples: "update assignement details as follows".
- delete_assignement: The user wants to perform delete operations on assignement. Examples: "delete assignement details as follows".
Only respond with one of the three values: "create_assignement", "update_assignement", "delete_assignement".
Do not add any explanation or extra text.

Examples:

Message: "create assignement details as follows"
Intent: create_assignement

Message: "update assignement details as follows"
Intent: update_assignement

Message: {msg}
Intent:

Database: testdb
        Table: Assignement(student_id, period, term, language_1, language_2, maths, science. social_science)

Extract any parameters (student_id, period, term, language_1, language_2, maths, science. social_science) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_assignement", "params": {{"student_id": 36, "period" : 1, "maths": 98}}}}
        {{"intent": "create_assignement", "params": {{"student_id": 45, "science": 10, "language_1": 76, "term": 1}}}}
""".strip()
    
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
    # routing logic
    
    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    

    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}
        
def node_assignement(state: ChatState) -> ChatState:
    parms_value = state["params"]
    intent_value = state["intent"]

    print("cintent_node_create_assignement")
    print(intent_value)

    match intent_value:

        case "create_assignement":

            required_keys = list(AssignementCreate.model_fields.keys())

            if all(parms_value.get(key) not in (None, "") for key in required_keys):        
                res = requests.post(f"{API}/assignement/", json= parms_value)
                reply = f"Created assigngment {parms_value['student_id']}." if res.status_code == 200 else "Failed to create assigngment list."
                response_data = res.json()
                return{**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
            else:
                reply = "Need all marks with subject "
                response_data = "The datas are inadequate to create assignement"
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
            
        case "update_assignement":
            required_keys = ["student_id", "term", "period"]
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.patch(f"{API}/assignement/{parms_value['student_id']}/term/{parms_value['term']}/period/{parms_value['period']}", json = parms_value)
                reply = f"Updated assigngment {parms_value['student_id']}." if res.status_code == 200 else "Failed to updated assigngment list."
                response_data = res.json()
                return{**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
            else:
                reply = "student_id, term, period are mandatory to update"
                response_data = "student_id, term, period are mandatory to update"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)],"response":response_data}
        
        case "delete_assignement":
            required_keys = ["student_id", "term", "period"]
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.delete(f"{API}/assignement/{parms_value['student_id']}/term/{parms_value['term']}/period/{parms_value['period']}")
                reply = "Assignement list deleted." if res.status_code == 200 else "Assignement list not found."
                response_data = res.json()
                return{**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
            else:
                reply = "Need a student ID to delete mark list"
                response_data = "Need a student ID to delete mark list"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        
        case _:
            reply = "Assignement is not create/updated/deleted"
            response_data = "Assignement is not create/updated/deleted"

            return{**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
