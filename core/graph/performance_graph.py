from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import os, json, requests
import re
from core.model.schema import ChatState
from core.node import performance_node

graph = StateGraph(ChatState)

graph.add_node("intent_node_performance_initial", performance_node.intent_node_performance_initial)
graph.add_node("router_node", performance_node.router_node)
graph.add_node("intent_node_mark_list", performance_node.intent_node_mark_list)
graph.add_node("intent_node_performance", performance_node.intent_node_performance)
graph.add_node("intent_chat_node", performance_node.intent_chat_node)

graph.set_entry_point("intent_node_performance_initial")
graph.add_conditional_edges("intent_node_performance_initial", performance_node.router_node, {
    "intent_node_mark_list" : "intent_node_mark_list",
    "intent_node_performance" : "intent_node_performance",
    "intent_chat_node" : "intent_chat_node"
})


graph.add_edge("intent_node_performance", END)
graph.add_edge("intent_node_mark_list", END)
graph.add_edge("intent_chat_node", END)

performance_graph = graph.compile()