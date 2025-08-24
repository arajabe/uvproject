from sqlalchemy.orm import Session
from core.database.databse import get_db
from langchain.schema import AIMessage,HumanMessage
from langchain.prompts import ChatPromptTemplate
from core.model.schema import ChatState,PerformanceState
from llm.llm import llm
import re,requests
import json
import pandas as pd
from core.database.databsetable.tables_marks import Mark
import pandas as pd
import matplotlib.pyplot as plt
from config import API_URL

def intent_node_performance_initial(state : ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""
You are a helpful AI assistant. Analyze the given user message and classify its intent.

You must choose **only one** of the following two intent labels:

- **mark_list** → When the user is asking for specific subject marks in a term exam  
  (e.g., "What is my science mark in term 2?")

- **performance** → When the user is asking for overall performance in a term  
  (e.g., "How did I perform in term 1?" or "Give me my result analysis")

📌 Respond with exactly one word: **"mark_list"** or **"performance"** or  **"others"** 
📌 Do **not** explain your answer. Do **not** add punctuation or extra text.

---

Message: {msg}
Intent:
""".strip()
    result = llm.invoke([HumanMessage(content=prompt)])
    print("intent_node_performance_initial")
    print(result.content)
    # routing logic
    
    return{** state, "messages":state["messages"], "intent": result.content}

def router_node(state: ChatState) -> str:
    x = str(state["intent"]).strip().lower()
    print("router node")
    match x:
        case "mark_list" : return "intent_node_mark_list"
        case "performance": return "intent_node_performance"

        case _: 
            return "intent_chat_node"


def intent_node_performance(state: ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f"""
                you are AI assistant get student_id form the {msg} to do performance analyze.

        Return **only** valid JSON, no extra text. Example:
        {{"params": {{"student_id": 35}}}}
            """
    result = llm.invoke([HumanMessage(content=prompt)])

    print(result)
    raw_output = result.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip() 
    

    print("raw output")
    print(raw_output)
    parsed = json.loads(raw_output)

    student_id = parsed.get("params", {}).get("student_id")

    if not student_id:
        reply = "Student ID is required to analyze performance."
        return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": reply}

    db: Session = next(get_db())
    all_marks = db.query(Mark).all()

    if not all_marks:
        reply = "No mark data available to analyze."
        return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": reply}

    # Class average calculation
    def safe_avg(values): return sum(values) / len(values) if values else 0

    class_avg = {
        "language_1": safe_avg([m.language_1 for m in all_marks]),
        "language_2": safe_avg([m.language_2 for m in all_marks]),
        "maths": safe_avg([m.maths for m in all_marks]),
        "science": safe_avg([m.science for m in all_marks]),
        "social_science": safe_avg([m.social_science for m in all_marks])
    }

    # Current student's marks
    student_marks = [m for m in all_marks if m.student_id == student_id]
    if not student_marks:
        reply = f"No marks found for student ID {student_id}."
        return {**state, "messages": state["messages"] + [AIMessage(content=reply)], "response": reply}

    term_analysis = []
    for mark in student_marks:
        diff = {
            subject: {
                "student_score": getattr(mark, subject),
                "class_avg": class_avg[subject],
                "below_avg": getattr(mark, subject) < class_avg[subject]
            }
            for subject in class_avg
        }
        term_analysis.append({
            "term": mark.term,
            "diff": diff
        })

    # Generate a natural language prompt for LLM
    prompt_template = ChatPromptTemplate.from_template("""
You are a school performance assistant. A student has the following subject scores compared to the class averages.

Provide clear performance feedback, stating where the student is performing well, and what subjects they should focus on improving.

Student ID: {student_id}

Performance per term:
{performance_json}

Respond like you're advising a student.
""")

    # Serialize performance data
    prompt_json = prompt_template.format(
        student_id=student_id,
        performance_json=json.dumps(term_analysis, indent=2)
    )

    # Call LLM to generate response
    response = llm.predict(prompt_json)

    return {
        **state,
        "messages": state["messages"] + [AIMessage(content=response)],
        "response": response
    }

def intent_node_mark_list(state : ChatState) -> ChatState:
    msg = state["messages"][-1].content
    prompt = f""" You are AI assistint analyze the {msg} and return the paramaters.
        
        Database: testdb
        Table: Mark(student_id, term, language_1, language_2, maths, science. social_science)

        Extract any parameters (student_id, term, subject, other) mentioned.

        Examples:
        messages:
        - what is the mark for science in term 1 and 2 for student id 90
        - get student id 90 marks in term 1 and 2
        - get student id 90 marks in maths term 1, 2


        Return **only** valid JSON, no extra text. Example:
        {{"params": {{"student_id": 36, "subject": [maths,science], "term":[1,2]}}}}  
        {{"params": {{"student_id": 25, "subject": [maths,science], "term":[1,2]. "other":[rank,total]}}}}  
"""
    ai_resp = llm.invoke([HumanMessage(content=prompt)])
    print(ai_resp)

    raw_output = ai_resp.content.strip()

    # Clean any accidental code block markers (like ```json ... ```)
    raw_output = re.sub(r"^```(json)?|```$", "", raw_output).strip() 
    

    print("raw output")
    print(raw_output)
    p = json.loads(raw_output)

    # Only include non-None fields in PATCH
    payload = {key: p[key] for key in [
            "term", "student_id", "subject"
        ] if key in p and p[key] is not None}
    
    print("payload")
    print(p)
   
    r = requests.post(f"{API_URL}/performance/", json = p)  

    print("requests")
    print(r.json())


    return {"messages" : state["messages"] + [AIMessage(content= "i am intent_node_mark_list")], "response" : r.json()}

def intent_rank_node(state : ChatState):
    df = pd.read_sql("SELECT * FROM termmark", get_db)


def intent_chat_node_old(state : ChatState) -> ChatState:
    db = next(get_db()) 
    df = pd.read_sql("SELECT * FROM termmark", db.bind)
    subject_cols = ["language_1", "language_2", "maths", "science", "social_science"]

    df["total"] = df[subject_cols].sum(axis=1)
    df["average"] = df[subject_cols].mean(axis=1)

    # Rank by total within each term
    df["rank_total"] = df.groupby("term")["total"].rank(ascending=False, method="min")

    y = ""
    # Rank by each subject within term
    for subject in subject_cols:
        df[f"rank_{subject}"] = df.groupby("term")[subject].rank(ascending=False, method="min")
    y = df.to_markdown()

    # Term-wise performance summary
    term_summary = df.groupby("term")[subject_cols + ["total", "average"]].mean().reset_index()

    # Save final table with rankings
    df.to_csv("student_performance_ranked.csv", index=False)

    print("term_summary")
    # print(df.to_csv("student_performance_ranked.csv", index=False)
   # print(df[df["term"] == 1][["student_id", "term", "total", "rank_total"]].sort_values(["term", "rank_total"]))
    df = df[["student_id", "term", "total", "rank_total"]].sort_values(["term", "rank_total"])

    prompt = f"""Here is the average subject performance by term:
        {term_summary.to_markdown(index=False)}

            Please analyze which term had the best overall performance, and which subject needs improvement.
        """

    response = llm.invoke([HumanMessage(content=prompt)])
    
    x= df[df["student_id"] == 20].to_markdown(index=False)
    
    return {"messages" : state["messages"] + [AIMessage(content= response.content)], "response_pd" : y}

def intent_chat_node(state : PerformanceState) -> PerformanceState:
    db = next(get_db()) 
    table = state["exam"].strip().lower()
    df = pd.read_sql(f"SELECT * FROM {table}", db.bind)
    print("data frame")
    print(state["performance_request"].lower())
    option = state["performance_request"].lower()
    result = performance_analysis_overall(df, option)
    print("result")
    print(result)
    result_md = result.to_markdown(index=False)

    return {"messages" : state["messages"] + [AIMessage(content= "performance on total")], "response_pd" : result_md}

def performance_analysis_overall(df: pd.DataFrame, option: str):
    print("performance_analysis option")
    print(option)
    if option == "overall_total":
        # Average total per student
        return df.groupby("student_id")["total"].mean().reset_index(name="avg_total")

    elif option == "overall_subject":
        # Subject-wise average
        subjects = ["language_1", "language_2", "maths", "science", "social_science"]
        return df[subjects].mean().reset_index(name="avg_score")

    elif option == "overall_trend":
        # Student performance trend across terms
        return df.groupby(["student_id", "term"])["total"].mean().reset_index()

    elif option == "overall_rank":
        # Rank students within each term
        df["rank"] = df.groupby("term")["total"].rank(method="dense", ascending=False)
        return df[["term", "student_id", "total", "rank"]].sort_values(["term", "rank"])

    elif option == "overall_strength_weakness":
        # Best and weakest subject per student
        subjects = ["language_1", "language_2", "maths", "science", "social_science"]
        best = df.melt(id_vars=["student_id", "term"], value_vars=subjects,
                       var_name="subject", value_name="score")
        best_sub = best.loc[best.groupby(["student_id", "term"])["score"].idxmax()]
        worst_sub = best.loc[best.groupby(["student_id", "term"])["score"].idxmin()]
        return {"best_subject": best_sub, "worst_subject": worst_sub}

    else:
        return "Invalid option!"
    
#df = pd.DataFrame(data)

def performance_analysis_individual(df: pd.DataFrame, option: str, student_id: str):
    print("option")
    if option == "total":
        # Average total per student
        return df.groupby("student_id")["total"].mean().reset_index(name="avg_total")

    elif option == "subject":
        # Subject-wise average across all students
        subjects = ["language_1", "language_2", "maths", "science", "social_science"]
        return df[subjects].mean().reset_index(name="avg_score")

    elif option == "trend":
        # Student performance trend across terms
        return df.groupby(["student_id", "term"])["total"].mean().reset_index()

    elif option == "rank":
        # Rank students within each term
        df["rank"] = df.groupby("term")["total"].rank(method="dense", ascending=False)
        return df[["term", "student_id", "total", "rank"]].sort_values(["term", "rank"])

    elif option == "strength_weakness":
        # Best and weakest subject per student
        subjects = ["language_1", "language_2", "maths", "science", "social_science"]
        best = df.melt(id_vars=["student_id", "term"], value_vars=subjects,
                       var_name="subject", value_name="score")
        best_sub = best.loc[best.groupby(["student_id", "term"])["score"].idxmax()]
        worst_sub = best.loc[best.groupby(["student_id", "term"])["score"].idxmin()]
        return {"best_subject": best_sub, "worst_subject": worst_sub}

    elif option == "compare":
        if not student_id:
            return "❌ Please provide a student_id for comparison"

        # Overall average of all students
        overall_avg = df.groupby("student_id")["total"].mean().reset_index(name="avg_total")
        
        # Find this student's performance
        student_perf = overall_avg[overall_avg["student_id"] == student_id]
        
        # Class average
        class_avg = overall_avg["avg_total"].mean()

        # Rank
        overall_avg["rank"] = overall_avg["avg_total"].rank(method="dense", ascending=False)
        student_rank = overall_avg[overall_avg["student_id"] == student_id]

        return {
            "student_performance": student_perf,
            "class_average": class_avg,
            "student_rank": student_rank
        }

    else:
        return "Invalid option!"
