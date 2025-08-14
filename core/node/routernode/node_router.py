from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import os, json, requests
import re
from core.model.schema import ChatState
from llm.llm import llm


API = "http://127.0.0.1:8000"

def parent_node(state: ChatState) -> ChatState:

    return{"response" : "welcome to Performance Analysis"}

def router_node(state: ChatState) -> str:
    role = state["role"]
    radio_action_on_person = state["radio_action_on_person"]
    print("new router node")
    router_value = role + "_" + radio_action_on_person.replace(" ", "_")
    match router_value.lower():
        case "admin_office_staff":  
            return "intent_node_office_staff"
        case "admin_parent":
            return "intent_node_parent"
        case "admin_student":
            return "intent_node_student"
        case "admin_teacher":
            return "intent_node_teacher"
        case _: 
            print(" hello chat user case")
            return "chat_node"