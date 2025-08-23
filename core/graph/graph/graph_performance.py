from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import os, json, requests
import re
from core.model.schema import PerformanceState
from core.node.performancenode import performance_node

graph = StateGraph(PerformanceState)

graph.add_node("intent_chat_node", performance_node.intent_chat_node)

graph.set_entry_point("intent_chat_node")

graph.add_edge("intent_chat_node", END)

graph_performance = graph.compile()