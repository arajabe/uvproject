from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import os, json, requests
import re
from core.model.schema import ChatState, OfficeStaffCreate
from llm.llm import llm


API = "http://127.0.0.1:8000"

def chat_node(state : ChatState) -> ChatState:
    message = state["messages"][-1].content
    chat_prompt = f""" 
                You are role is AI assistant and query with data base regards student information related tables.
                you have to reply for the {message} accordingly
                """
    result = llm.invoke([HumanMessage(content = chat_prompt)])

    reply = "welcome to information customer care"
    return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response" : result.content}

def intent_node_admin_view(state : ChatState) -> ChatState:
    user_message = state["messages"][-1].content
    chat_prompt = f""" 
                You are role is AI assistant and query with data base regards student information related tables.
                you have to reply for the {user_message} accordingly

                RULE :
                example : 1.what is student STUD0001 detaisl?
                answer : you will response
                example : 2. What is father name of teacher TEA0002?
                ANSWER : DONT RESPONSE?
                """
    result = llm.invoke([HumanMessage(content = chat_prompt)])
    res = requests.post(f"{API}/info_chat/get", params={"message" : user_message})
    response_data = res.json()
    return {**state, "messages": state["messages"] + [AIMessage(content="check the response")], "response" : response_data}