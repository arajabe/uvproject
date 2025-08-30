from core.model.schema import ChatState
from llm.llm import llm

def parent_node(state: ChatState) -> ChatState:
    return{"response" : "welcome to Performance Analysis"}

def router_node(state: ChatState) -> str:
    role = state["role"]
    radio_action_on_person = state["radio_action_on_person"]
    router_value = str(role + "_" + radio_action_on_person.replace(" ", "_")).strip()
    match router_value.lower():
        case "admin_office_staff" | "officestaff_office_staff":  
            return "intent_node_office_staff"
        case "admin_parent":
            return "intent_node_parent"
        case "admin_student":
            return "intent_node_student"
        case "admin_teacher":
            return "intent_node_teacher"
        case "teacher_assignement":
            return "intent_node_assignement"
        case "teacher_subject_term_split":
            return "intent_node_subject_term_mark_split"
        case "teacher_term_mark":
            return "intent_node_term_mark"
        case "admin_student_class_allocation":
            return "intent_node_student_class_allocation"
        case "admin_class_teacher_allocation":
            return "intent_node_class_teacher_allocation"
        case "admin_information" | "teacher_information":
            return "intent_node_admin_view"
        case _: 
            return "chat_node"
        
