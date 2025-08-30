from langchain.schema import HumanMessage, AIMessage
from llm.llm import llm
import json, requests
import re
from core.model.schema import ChatState
from config import API_URL

def intent_node(state:ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""
    Task:
    Identify the exact intent from the message: "{msg}" without inferring unrelated meanings.
    Valid intents are exactly: term mark, assignement, pratical, Subject Term Split.

    Rules:
    - Match case-insensitively.
    1. If the message contains a direct mention of an intent (exact, partial, or misspelled), map it to the closest valid intent.
    2. If multiple possible intents appear, choose the one most explicitly present.
    3. If none match exactly, pick the closest match based on meaning or spelling similarity.
    4. Match is case-insensitive and tolerant of minor spelling mistakes.
    5. Output exactly one JSON object in this format:
   {{"intent": "<term mark | assignement | pratical | subject_term_split>"}}
    6. Do not output explanations or extra text.

    - Return exactly one JSON object in this format:
        {{"intent": "<term mark | assignement | pratical | subject_term_split>"}}
    - Never output explanations or extra text.

    Examples:

    Message: create Assignement details as follows
    Output: {{"intent": "assignement"}}

    Message: create Term mark details as follows
    Output: {{"intent": "term mark"}}

    Message: update Term mark details as follows
    Output: {{"intent": "term mark"}}

    Message: delete Assignemen details as follows
    Output: {{"intent": "assignement"}}

    Message: create practical test result
    Output: {{"intent": "pratical"}}

    Message: create Subject Term Split test result
    Output: {{"intent": "subject_term_split"}}

    Message: update Subject Term Split test result
    Output: {{"intent": "subject_term_split"}}
"""

    ai_resp = llm.invoke([HumanMessage(content=prompt)])   

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    
    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat")}

def router_node(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    match x:
        case "term mark": return "intent_node_mark"
        case "assignement": return "intent_node_assignement"
        case "pratical": return "intent_node_pratical"
        case "subject_term_split" : return "intent_node_subject_term_split"
        case _: 
            return "chat_node"


def intent_node_mark(state:ChatState) -> ChatState:
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
    # routing logic
    
    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    

    try:
        parsed = json.loads(raw_output)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}

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

def intent_node_subject_term_split(state:ChatState) -> ChatState:
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
        Table: SubjectTermSpli(student_id, term, subject, mark_section_A, mark_section_B, mark_section_C, mark_section_D)

Extract any parameters (student_id, term, subject, mark_section_A, mark_section_B, mark_section_C, mark_section_D) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_subject_term_split", "params": {{"student_id": 36, "term" : 1, "mark_section_A": 8}}}}
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

def router_node_mark(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_mark" : return "intent_node_create_mark"
        case "update_mark": return "intent_node_update_mark"
        case "delete_mark": return "intent_node_delete_mark"
        case _: 
            return "chat_node_initial"
        
def router_node_assignement(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_assignement" : return "intent_node_create_assignement"
        case "update_assignement": return "intent_node_update_assignement"
        case "delete_assignement": return "intent_node_delete_assignement"
        case _: 
            return "chat_node_initial"
        
def router_node_subject_term_split(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    match x:
        case "create_subject_term_split" : return "intent_node_create_subject_term_split"
        case "update_subject_term_split": return "intent_node_update_subject_term_split"
        case "delete_subject_term_split": return "intent_node_delete_subject_term_split"
        case _: 
            return "chat_node_initial"
    
    
def chat_node_initial(state: ChatState) -> ChatState:
    ai_reply = llm.invoke(state["messages"]).content
    #return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": AIMessage(content=ai_reply)}
    return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": "chat_node_initial"}

def intent_node_create_mark(state: ChatState) -> ChatState:
    p = state["params"]

    if "student_id" in p and "term" in p and "language_1" in p and "language_2" in p and "maths" in p and "science" in p and "social_science" in p:
        
        r = requests.post(f"{API_URL}/mark/", json={"student_id": p["student_id"], "term" : p["term"], "language_1": p["language_1"], "language_2" : p["language_2"],
                                                "maths" : p["maths"], "science": p["science"], "social_science" : p["social_science"]})
        reply = f"Created mark {p['student_id']}." if r.status_code == 200 else "Failed to create mark list."
    else:
        reply = "Need all marks with subject "

    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def intent_node_create_assignement(state: ChatState) -> ChatState:
    p = state["params"]

    if "student_id" in p and "term" in p and "language_1" in p and "language_2" in p and "maths" in p and "science" in p and "social_science" in p:
        
        r = requests.post(f"{API_URL}/assignement/", json= p )
        reply = f"Created assigngment {p['student_id']}." if r.status_code == 200 else "Failed to create assigngment list."
    else:
        reply = "Need all marks with subject "
 
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def intent_node_create_subject_term_split(state: ChatState) -> ChatState:
    p = state["params"]

    if "student_id" in p and "term" in p and "subject" in p:
        
        r = requests.post(f"{API_URL}/subjecttermsplit/", json= p )
        reply = f"Created assigngment {p['student_id']}." if r.status_code == 200 else "Failed to create assigngment list."
    else:
        reply = "Need all marks with subject "
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def intent_node_update_mark(state: ChatState) -> ChatState:
    p = state["params"]

    # Check required params
    if "student_id" in p and "term" in p:
        url = f"{API_URL}/mark/{p['student_id']}/{p['term']}"

        # Only include non-None fields in PATCH
        payload = {key: p[key] for key in [
            "language_1", "language_2", "maths", "science", "social_science"
        ] if key in p and p[key] is not None}

        if not payload:
            reply = "No fields provided to update."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}

        r = requests.patch(url, json=payload)

        if r.status_code == 200:
            reply = "Mark updated successfully."
        elif r.status_code == 404:
            reply = "Mark record not found."
        else:
            reply = f"Update failed with status {r.status_code}"

        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "response": r.json() if r.status_code == 200 else {}
        }

    else:
        reply = "Both student ID and term are required to update marks."
        return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}
    
def intent_node_update_assignement(state: ChatState) -> ChatState:
    p = state["params"]

    # Check required params
    if "student_id" in p and "term" in p and "period" in p: 
        url = f"{API_URL}/assignement/{p['student_id']}/term/{p['term']}/period/{p['period']}"

        # Only include non-None fields in PATCH
        payload = {key: p[key] for key in [
            "language_1", "language_2", "maths", "science", "social_science", "period", "term", "student_id"
        ] if key in p and p[key] is not None}

        if not payload:
            reply = "No fields provided to update."
            return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}

        r = requests.patch(url, json=payload)

        if r.status_code == 200:
            reply = "Mark updated successfully."
        elif r.status_code == 404:
            reply = "Mark record not found."
        else:
            reply = f"Update failed with status {r.status_code}"

        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "response": r.json() if r.status_code == 200 else {}
        }

    else:
        reply = "Both student ID and term are required to update marks."
        return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}
    
def intent_node_update_subject_term_split(state: ChatState) -> ChatState:
    p = state["params"]
 
    # Check required params
    if "student_id" in p and "term" in p:
        url = f"{API_URL}/subjecttermsplit/{p['student_id']}/{p['subject']}/{p['term']}"

        r = requests.patch(url, json=p)

        if r.status_code == 200:
            reply = "Mark updated successfully."
        elif r.status_code == 404:
            reply = "Mark record not found."
        else:
            reply = f"Update failed with status {r.status_code}"

        return {
            **state,
            "messages": state["messages"] + [AIMessage(content=reply)],
            "response": r.json() if r.status_code == 200 else {}
        }

    else:
        reply = "Both student ID and term are required to update marks."
        return {**state, "messages": state["messages"] + [AIMessage(content=reply)]}

def intent_node_delete_mark(state: ChatState) -> ChatState:
    p = state["params"]
    if "student_id" in p:
        r = requests.delete(f"{API_URL}/mark/{p['student_id']}/{p['term']}")
        reply = "mark list deleted." if r.status_code == 200 else "student list not found."
    else:
        reply = "Need a student ID to delete mark list"
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def intent_node_delete_assignement(state: ChatState) -> ChatState:
    p = state["params"]
    if "student_id" in p:
        r = requests.delete(f"{API_URL}/assignement/{p['student_id']}/term/{p['term']}/period/{p['period']}")
        reply = "mark list deleted." if r.status_code == 200 else "student list not found."
    else:
        reply = "Need a student ID to delete mark list"
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}

def intent_node_delete_subject_term_split(state: ChatState) -> ChatState:
    p = state["params"]
    if "student_id" in p:
        r = requests.delete(f"{API_URL}/subjecttermsplit/{p['student_id']}/{p["subject"]}/{p['term']}")
        reply = "mark list deleted." if r.status_code == 200 else "student list not found."
    else:
        reply = "Need a student ID to delete mark list"
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": r.json()}
