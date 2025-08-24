from langchain_groq.chat_models import ChatGroq
from config import LLM_MODEL, LLM_API_KEY


llm =  ChatGroq(model=LLM_MODEL, temperature=0, api_key=LLM_API_KEY)