from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
import os, json, requests
import re
from core.model.schema import ChatState
from core.node import teacher_node

graph = StateGraph(ChatState)

graph.add_node("intent_node", teacher_node.intent_node)

graph.add_node("intent_node_mark", teacher_node.intent_node_mark)
graph.add_node("intent_node_assignement", teacher_node.intent_node_assignement)


graph.add_node("intent_node_create_mark", teacher_node.intent_node_create_mark)
graph.add_node("intent_node_update_mark", teacher_node.intent_node_update_mark)
graph.add_node("intent_node_delete_mark", teacher_node.intent_node_delete_mark)

graph.add_node("intent_node_create_assignement", teacher_node.intent_node_create_assignement)

graph.add_node("chat_node_initial", teacher_node.chat_node_initial)


graph.set_entry_point("intent_node")

graph.add_conditional_edges("intent_node", teacher_node.router_node, {
     "intent_node_mark" : "intent_node_mark",
    "intent_node_assignement" : "intent_node_assignement",
    "chat_node_initial": "chat_node_initial"
})


graph.add_conditional_edges("intent_node_mark", teacher_node.router_node_mark, {
    "intent_node_create_mark" : "intent_node_create_mark",
    "intent_node_update_mark" : "intent_node_update_mark",
    "intent_node_delete_mark" : "intent_node_delete_mark",
    "chat_node_initial": "chat_node_initial"
})

graph.add_conditional_edges("intent_node_assignement", teacher_node.router_node_assignement, {
    "intent_node_create_assignement" : "intent_node_create_assignement",
    "chat_node_initial": "chat_node_initial"
})

graph.add_edge("intent_node_create_mark", END)

graph.add_edge("intent_node_create_assignement", END)



graph.add_edge("chat_node_initial", END)


teacher_graph = graph.compile()