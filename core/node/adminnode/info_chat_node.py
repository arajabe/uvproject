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
                You are role is AI assistant and query in user asking table name.
                you have to reply for the {user_message}.

                your asswer format likely : 1. select * from table name where field name = "value"
                                            2. select fields from table name where field name = "value"

                RULE :
                1. only sql query start with select
                2. no other sql query

                examples:
                user_message : select * from table classteacherallocation where all teacher
                your answer : select * from  "classteacherallocation";

                user_message : select * from table parent where parent id PA0002
                your answer : select * from  parent where parent_id = "PA0002";

                user_message : select [id] from table teacher where all teacher
                your answer : select id from  "teacher";

                user_message :select ['fathername'] from table student where student id TEA0001
                Your answer : select teacher_class from student where student_id = "STUD0001"

                user_message :select ['class_section'] from table studentclassallocation where student id TEA0001
                Your answer : select class_section from studentclassallocation where student_id = "STUD0001"

                user_message : select * from table classteacherallocation where teacher id TEA0003 teacher class 1
                your answer : SELECT * from classteacherallocation where teacher_id = 'TEA0003' and teacher_class = '1';

                user_message : select ['count'] from studentclassallocation where student id STUD0011
                your answer : select count(*) from studentclassallocation where student_id = STUD0011

                user_message : get details of class teacher allocation
                your answer : not allowed

                user_message : you are not allowed to do this
                your answer : not allowed

                user_message : select * from table classteacherallocation where get details of class student get details of class student 
                your answer : not allowed
                """.strip()
    ai_resp = llm.invoke([HumanMessage(content = chat_prompt)])

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip()
    raw_output = f"{raw_output}"
    print("result content")
    print(raw_output)
    if raw_output is not "not allowed":
        res = requests.post(f"{API}/info_chat/get", params={"message" : raw_output})
        response_data = res.json()
        return {**state, "messages": state["messages"] + [AIMessage(content="check the response")], "response" : response_data}
    else:
        return {**state, "messages": state["messages"] + [AIMessage(content="check the response")], "response" : "you are not allowed"}