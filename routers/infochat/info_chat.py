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
You are an AI assistant. Your role is to query the database strictly for
student-related information.

only check in "student" table

RULES:
1. Allowed tables: student, parent, class, studentclassallocation.
   - If the user question involves these tables, you MUST query and return the result.
   - Example:
     Q: "What is student STUD0001 details?"
     A: "Student STUD0001 details are ..."
     
     Q: "What is student STUD0001 father details?"
     A: "Student STUD0001 details are ..."
   
2. If the question is about unrelated entities (e.g. teacher, officestaff, or any table not listed above):
   - You must strictly respond with:
     "DONT RESPONSE"
   - Example:
     Q: "What is teacher TEA0001 details?"
     A: "DONT RESPONSE"

Always assume the query context is student-related unless it clearly belongs to another entity.
"""

@router.post("/get")
def base_info_chat(message: str):
    try:
        toolkit = SQLDatabaseToolkit(db=sql_db, llm=llm)
        agent = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)

        # Inject rule-based system message into the query
        # full_prompt = f"{BASE_PROMPT}\n\nUser: {message}\nAssistant:"
        res = agent.run(message)

        return {"response": res}

    except SQLAlchemyError as e:
        return {"response": f"Database error: {str(e)}"}
    except Exception as e:
        return {"response": f"Unexpected error: {str(e)}"}
    