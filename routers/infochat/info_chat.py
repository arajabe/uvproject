from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.model.schema import AssignementCreate, AssignementUpdate
from core.database.databse import get_db
from core.database.databsetable.tables_users import Student
from core.database.databsetable.tables_marks import Mark, Assignement
from core.database.databsetable.tables_allocations import StudentClassAllocation
from sqlalchemy.exc import SQLAlchemyError
from langchain_experimental.sql import SQLDatabaseChain
from llm.llm import llm
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine,MetaData
from core.database.databse import get_db
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

router = APIRouter(prefix="/info_chat", tags=["info chat"])

DATABASE_URL = "mysql+pymysql://root:Nannilam123@127.0.0.1/testdb"
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
agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

@router.post("/get")
def base_info_chat(message: str):
    try:
        

        #Inject rule-based system message into the query
        full_prompt = f"{BASE_PROMPT}\n\nUser: {message}\nAssistant:"
        res = agent.run(full_prompt )

        return {"response": res}

    except SQLAlchemyError as e:
        return {"response": f"Database error: {str(e)}"}
    except Exception as e:
        return {"response": f"Unexpected error: {str(e)}"}
    