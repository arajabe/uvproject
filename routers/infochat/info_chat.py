from fastapi import APIRouter
from sqlalchemy.exc import SQLAlchemyError
from llm.llm import llm
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from core.database.databse import get_db
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from config import DATABASE_URL
from langchain.agents import AgentExecutor

router = APIRouter(prefix="/info_chat", tags=["info chat"])

# DATABASE_URL = "mysql+pymysql://root:Nannilam123@127.0.0.1/testdb"
engine = create_engine(DATABASE_URL, echo=True, future=True)
sql_db = SQLDatabase(engine)

# System prompt with rules
BASE_PROMPT = """
You are an AI assistant. 
Your role is to query the database strictly based on the user message.

RULES:
1. The user message will be very close to an SQL query (not natural language).
   - Example user message: "select fathername from student where id = 'STUD0003';"
   - Example user message: "student STUD0003 details"
2. You must generate and run the closest valid SQL query for the given message.
3. Do not explain your reasoning. Only return the final result. 
4. Never modify the user’s intent — only clean and execute the closest valid SQL.
4. Never modify the user’s intent table — only clean and execute the closest valid SQL.

Your job: take the message, translate it to the correct SQL if needed, execute, 
and return only the result.

"""
toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)
agent: AgentExecutor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

@router.post("/get")
def base_info_chat(message: str):
    max_attempts = 2
    attempt = 0
    last_response = None

    full_prompt = f"{BASE_PROMPT}\n\nUser: {message}\nAssistant:"

    while attempt < max_attempts:
        try:
            res = agent.run(full_prompt)
            logger.info(f"Agent success on attempt {attempt + 1}: {res}")
            return {"response": res}
        except Exception as e:
            # Only handle LLM output parsing errors
            if "Could not parse LLM output" in str(e):
                attempt += 1
                last_response = f"Attempt {attempt} failed: {str(e)}"
                logger.warning(f"Parsing error on attempt {attempt}: {str(e)}")
            else:
                # Other errors, immediately return
                logger.error(f"Unexpected error: {str(e)}")
                return {"response": f"Unexpected error: {str(e)}"}

    # After 2 attempts, return last error
    logger.error(f"Agent failed after {max_attempts} attempts: {last_response}")
    return {"response": last_response}
    