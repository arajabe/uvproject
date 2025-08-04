from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from llm.llm import llm
import os, json, requests
import re
from core.model.schema import ChatState

API = "http://127.0.0.1:8000"

def intent_node_mark(state:ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""
You are an intent classification assistant. Your job is to classify a user message into one of the intent categories.
You want the AI assistant to analyze a message ({msg}) and determine the intent, specifically in the context of student academic data — like subject-wise marks, performance, or term results.

Available intents:
- create_mark: The user wants to perform create operations on mrks. Examples: "Add a mark", "add mark for this id", "create mark for this id", "create mark for this id".
- update_mark: The user wants to perform update operations on mrks. Examples: "update a mark", "add update for this id", "update mark for this id", "update mark for this id".
- delete_mark: The user wants to perform delete operations on mrks. Examples: "delete a mark", "add delete for this id", "delete mark for this id", "delete mark for this id".
Only respond with one of the three values: "create_mark", "user", "update_mark", "delete_mark".
Do not add any explanation or extra text.

Examples:

Message: "create a mark for this id"
Intent: create_mark

Message: "Add mark for this id"
Intent: create_mark

Message: "enter mark for this id"
Intent: create_mark

Message: "update mark for this id"
Intent: create_mark

Message: {msg}
Intent:

Database: testdb
        Table: Mark(student_id, term, language_1, language_2, maths, science. social_science)

Extract any parameters (student_id, term, language_1, language_2, maths, science. social_science) mentioned.

        Return **only** valid JSON, no extra text. Example:
        {{"intent": "create_student", "params": {{"student_id": 36, "maths": 98}}}}
        {{"intent": "create_student", "params": {{"student_id": 45, "science": 10, "language_1": 76, "term": 1}}}}
""".strip()
    
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
    print("intent node")
    print(ai_resp.content)
    # routing logic
    
    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()    

    try:
        parsed = json.loads(raw_output)
        print("student_id, term, language_1, language_2, maths, science. social_science")
        print(parsed)
    except:
        parsed = {"intent": "chat", "params": {}}
    return {**state, "intent": parsed.get("intent", "chat"), "params": parsed.get("params", {})}

def router_node_mark(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    print("router node")
    match x:
        case "create_mark" : return "intent_node_create_mark"
        case "update_mark": return "intent_node_update_mark"
        case "delete_mark": return "intent_node_delete_mark"
        case _: 
            print(" hello chat mark router")
            return "chat_node_initial"
    
    
def chat_node_initial(state: ChatState) -> ChatState:
    ai_reply = llm.invoke(state["messages"]).content
    print("chat node")
    #return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": AIMessage(content=ai_reply)}
    return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": "not allowed to create user id"}

def intent_node_create_mark(state: ChatState) -> ChatState:
    p = state["params"]
    print("create node mark node")

    if "student_id" in p and "term" in p and "language_1" in p and "language_2" in p and "maths" in p and "science" in p and "social_science" in p:
        
        r = requests.post(f"{API}/mark/", json={"student_id": p["student_id"], "term" : p["term"], "language_1": p["language_1"], "language_2" : p["language_2"],
                                                "maths" : p["maths"], "science": p["science"], "social_science" : p["social_science"]})
        reply = f"Created mark {p['student_id']}." if r.status_code == 200 else "Failed to create mark list."
    else:
        reply = "Need all marks with subject "
    
    print("r.json()")
    print(r)

    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : r.json()}

def intent_node_update_mark(state: ChatState) -> ChatState:
    pass

def intent_node_delete_mark(state: ChatState) -> ChatState:
    pass