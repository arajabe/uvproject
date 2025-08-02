from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from llm.llm import llm
import os, json, requests
import re
from core.model.schema import ChatState

def teacher_node(state: ChatState) -> ChatState:
    ai_reply = llm.invoke(state["messages"]).content
    #return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": AIMessage(content=ai_reply)}
    return {**state, "messages": state["messages"] + [AIMessage(content=ai_reply)], "response": {"hello":"i am teacher node llm"}}