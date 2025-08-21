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
                you have to reply for the {user_message} accordingly in sql language

                RULE :
                1. only sql query start with select
                2. no other sql query

                examples:
                user_message : select * from table classteacherallocation where all teacher
                your answer : select * from  "classteacherallocation";

                user_message : select * from table classteacherallocation where get details of class teacher allocation
                your answer : select * from  "classteacherallocation";

                user_message : select [id] from table classteacherallocation where all teacher
                your answer : select id from  "classteacherallocation";

                user_message :select ['teacher_class'] from table classteacherallocation where teacher id TEA0001
                Your answer : select teacher_class from classteacherallocation where teacher_id = "TEA0001"

                user_message : select * from table classteacherallocation where teacher id TEA0003 teacher class 1
                your answer : SELECT * from classteacherallocation where teacher_id = 'TEA0003' and teacher_class = '1';
                """
    result = llm.invoke([HumanMessage(content = chat_prompt)])
    print("result content")
    print(result.content)
    res = requests.post(f"{API}/info_chat/get", params={"message" : result.content})
    response_data = res.json()
    return {**state, "messages": state["messages"] + [AIMessage(content="check the response")], "response" : response_data}