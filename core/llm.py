from langchain_groq.chat_models import ChatGroq
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

import os, json, requests
import re
from core.model.schema import ChatState


llm = ChatGroq(model="gemma2-9b-it", temperature=0, api_key="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")