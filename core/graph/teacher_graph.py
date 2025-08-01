from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from core.llm import llm
import os, json, requests
import re
from core.model.schema import ChatState
from core.node import teacher_node

graph = StateGraph(ChatState)

graph.add_node("teacher_node", teacher_node.teacher_node)


graph.set_entry_point("teacher_node")


graph.add_edge("teacher_node", END)

teacher_graph = graph.compile()