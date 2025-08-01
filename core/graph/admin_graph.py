from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from core.llm import llm
import os, json, requests
import re
from core.model.schema import ChatState
from core.node import admin_node

graph = StateGraph(ChatState)

graph.add_node("intent_node", admin_node.intent_node)
graph.add_node("intent_node_user", admin_node.intent_node_user)
graph.add_node("intent_node_teacher", admin_node.intent_node_teacher)
graph.add_node("create_node_user", admin_node.create_node_user)
graph.add_node("delete_node_user", admin_node.delete_node_user)
graph.add_node("update_node_user", admin_node.update_node_user)
graph.add_node("chat_node", admin_node.chat_node)

graph.set_entry_point("intent_node")
graph.add_conditional_edges("intent_node", admin_node.router_node, {
    "intent_node_teacher" : "intent_node_teacher",
    "intent_node_user" : "intent_node_user",
    "chat_node": "chat_node"
})
graph.add_conditional_edges("intent_node_user", admin_node.router_node_user, {
    "create_node_user": "create_node_user",
    "delete_node_user": "delete_node_user",
    "update_node_user": "update_node_user",
    "chat_node": "chat_node"
})
graph.add_edge("create_node_user", END)
graph.add_edge("delete_node_user", END)
graph.add_edge("update_node_user", END)
graph.add_edge("intent_node_teacher", END)
graph.add_edge("chat_node", END)

intent_graph = graph.compile()