from langchain.schema import HumanMessage, AIMessage
from llm.llm import llm
import os, json, requests
import re
from core.model.schema import ChatState, SubjectTermSplitCreate

API = "http://127.0.0.1:8000"

def intent_node_subject_term_mark_split(state:ChatState) -> ChatState:
    print("intent_node_subject_term_split")
    msg = state["messages"][-1].content
    prompt = f"""
You are an intent classification assistant. Your job is to classify a user message into one of the intent categories.
You want the AI assistant to analyze a message ({msg}) and determine the intent, specifically in the context of student academic data — like subject-wise marks, performance, or term results.

Rules : 
 the message contains a direct mention of an intent

Available intents:
- create_subject_term_split: The user wants to perform create operations on assignement. Examples: "create Subject Term Split details as follows".
- update_subject_term_split: The user wants to perform update operations on assignement. Examples: "update Subject Term Split details as follows".
- delete_subject_term_split: The user wants to perform delete operations on assignement. Examples: "delete Subject Term Split details as follows".
Only respond with one of the three values: "create_subject_term_split", "update_subject_term_split", "delete_subject_term_split".
Do not add any explanation or extra text.

Examples:

Message: "create Subject Term Split details as follows"
Intent: create_subject_term_split

Message: "update Subject Term Split details as follows"
Intent: update_subject_term_split

Message: "delete Subject Term Split details as follows"
Intent: delete_subject_term_split

Message: {msg}
Intent:

Database: testdb
        Table: SubjectTermSpli(student_id, term, subject, mark_section_A, mark_section_B, mark_section_C, mark_section_D, abscent)

Extract any parameters (student_id, term, subject, mark_section_A, mark_section_B, mark_section_C, mark_section_D, abscent) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_subject_term_split", "params": {{"student_id": 36, "term" : 1, "mark_section_A": 8, "abscent" = 'no'}}}}
        {{"intent": "update_subject_term_split", "params": {{"student_id": 45, "term": 10, "mark_section_B": 6, "mark_section_C": 8}}}}
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
    
def node_subject_term_mark_split(state: ChatState) -> ChatState:
    parms_value = state["params"]
    intent_value = state["intent"]
    print("intent_node_create_subject_term_split")

    required_keys = list(SubjectTermSplitCreate.model_fields.keys())

    match intent_value:
        case "create_subject_term_split":
            if all(parms_value.get(key) not in (None, "") for key in required_keys):        
                res = requests.post(f"{API}/subjecttermsplit/", json= parms_value )
                reply = f"Created subject term split mark {parms_value['student_id']}." if res.status_code == 200 else "Failed to create subject term split mark."
                response_data = res.json()
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
            else:
                reply = "Need all marks with subject "
                response_data = "Need all marks with subject"
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
        
        case "update_subject_term_split":
            if all(parms_value.get(key) not in (None, "") for key in required_keys):
                res = requests.patch(f"{API}/subjecttermsplit/student/{parms_value['student_id']}/subject/{parms_value['subject']}/term/{parms_value['term']}", 
                                     json = parms_value)
                reply =  "Subject term mark is updated" if res.status_code == 200 else "Subject term mark is not updated"
                response_data = res.json()
                return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}

            else:
                 reply = "Datas are inadequate to update the subject term split mark"
                 response_data = "Datas are inadequate to update the subject term split mark"
                 return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : response_data}
            
        case "delete_subject_term_split":
                required_keys = ["student_id","subject","term"]
                if all(parms_value.get(key) not in (None, "") for key in required_keys):
                    res = requests.delete(f"{API}/subjecttermsplit/student/{parms_value['student_id']}/subject/{parms_value["subject"]}/term/{parms_value['term']}")
                    reply = "subject term split mark deleted." if res.status_code == 200 else "subject term split mark is not deleted."
                    response_data = res.json()
                    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
                else:
                    reply = "Need a student ID, subject, term to delete mark"
                    response_data = "Need a student ID, subject, term to delete mark"
                    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
        case _:
            reply = "Split term mark is not created, updated, deleted"
            response_data = "Split term mark is not created, updated, deleted"
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": response_data}
