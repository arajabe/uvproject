from langchain.schema import HumanMessage, AIMessage
from llm.llm import llm
import json, requests
import re
from core.model.schema import ChatState, MarkCreate
from config import API_URL

def intent_node_term_mark(state:ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""
You are an intent classification assistant. Your job is to classify a user message into one of the intent categories.
You want the AI assistant to analyze a message ({msg}) and determine the intent, specifically in the context of student academic data — like subject-wise marks, performance, or term results.

Rules : 
 the message contains a direct mention of an intent

Available intents:
- create_mark: The user wants to perform create operations on mrks. Examples: "create Term Mark details as follows".
- update_mark: The user wants to perform update operations on mrks. Examples: "update Term Mark details as follows".
- delete_mark: The user wants to perform delete operations on mrks. Examples: "delete Term Mark details as follows.

Only respond with one of the three intent values: "create_mark", "update_mark", "delete_mark".
Do not add any explanation or extra text.

Examples:

Message: "create Term Mark details as follows"
Intent: create_mark

Message: "update Term Mark details as follows"
Intent: update_mark

Message: "delete Term Mark details as follows"
Intent: delete_mark

Message: {msg}
Intent:

Database: testdb
        Table: Mark(student_id, term, language_1, language_2, maths, science. social_science)

Extract any parameters (student_id, term, language_1, language_2, maths, science. social_science) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_mark", "params": {{"student_id": 36, "maths": 98}}}}
        {{"intent": "create_mark", "params": {{"student_id": 45, "science": 10, "language_1": 76, "term": 1}}}}
""".strip()
    
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
    
    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    

    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}
        
def node_term_mark(state: ChatState) -> ChatState:
    parms_value = state["params"]
    intent_value = state["intent"]
    print("node_term_mark")

    match intent_value:
        case "create_mark":
            required_keys = list(MarkCreate.model_fields.keys())
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.post(f"{API_URL}/mark/", json= parms_value)
                reply = f"Created mark {parms_value['student_id']}." if res.status_code == 200 else "Failed to create mark list."
                respond_data = res.json()
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : respond_data}
            else:
                reply = "Data are inadequate"
                respond_data = "Data are inadequate"
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : respond_data}
            
        case "update_mark":
            required_keys = ["student_id","term"]
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.patch(f"{API_URL}/mark/{parms_value['student_id']}/{parms_value['term']}", json = parms_value)
                reply= "Term marks is updated" if res.status_code ==200 else "Term mark is not updated" 
                response_data = res.json()
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response":response_data}
            else:
                reply = "Data are inadequate to update"
                response_data = "Data are inadequate to update"
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response":response_data}
        case "delete_mark":
            required_keys = ["student_id","term"]
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.delete(f"{API_URL}/mark/{parms_value['student_id']}/{parms_value['term']}")
                reply = "mark list deleted." if res.status_code == 200 else "student list not found."
                response_data = res.json()
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
            else:
                reply = "Need a student ID to delete mark list"
                response_data = "Need a student ID to delete mark list"
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        case _:
            reply = "The term mark is not created/updated/deleted"
            response_data = "The term mark is not created/updated/deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}


