from langgraph.graph import StateGraph, END
from core.model.schema import ChatState
from core.node.adminnode import info_officestaff_node, info_parent_node, info_student_node, info_teacher_node
from core.node.routernode import node_router
from core.node.teachernode import teacher_assignement,teacher_term_mark,teacher_subject_term_mark_split


graph = StateGraph(ChatState)


graph.add_node("entry_node", node_router.parent_node)

graph.add_node("intent_node_office_staff", info_officestaff_node.intent_node_officestaff)
graph.add_node("node_office_staff", info_officestaff_node.node_officestaff)

graph.add_node("intent_node_parent", info_parent_node.intent_node_parent)
graph.add_node("node_parent", info_parent_node.node_parent)

graph.add_node("intent_node_student", info_student_node.intent_node_student)
graph.add_node("node_student", info_student_node.node_student)

graph.add_node("intent_node_teacher", info_teacher_node.intent_node_teacher)
graph.add_node("node_teacher", info_teacher_node.node_teacher)

graph.add_node("intent_node_assignement", teacher_assignement.intent_node_assignement)
graph.add_node("node_assignement", teacher_assignement.node_assignement)

graph.add_node("intent_node_term_mark", teacher_term_mark.intent_node_term_mark)
graph.add_node("node_term_mark", teacher_term_mark.node_term_mark)

graph.add_node("intent_node_subject_term_mark_split", teacher_subject_term_mark_split.intent_node_subject_term_mark_split)
graph.add_node("node_subject_term_mark_split", teacher_subject_term_mark_split.node_subject_term_mark_split)

graph.set_entry_point("entry_node")

graph.add_conditional_edges("entry_node", node_router.router_node, {
     "intent_node_office_staff" : "intent_node_office_staff",
     "intent_node_parent" : "intent_node_parent",
     "intent_node_student" : "intent_node_student",
     "intent_node_teacher" : "intent_node_teacher",
     "intent_node_assignement" : "intent_node_assignement",
     "intent_node_term_mark" : "intent_node_term_mark",
     "intent_node_subject_term_mark_split" : "intent_node_subject_term_mark_split",
})


graph.add_edge("intent_node_office_staff", "node_office_staff")
graph.add_edge("node_office_staff", END)

graph.add_edge("intent_node_parent", "node_parent")
graph.add_edge("node_parent", END)

graph.add_edge("intent_node_student", "node_student")
graph.add_edge("node_student", END)

graph.add_edge("intent_node_teacher", "node_teacher")
graph.add_edge("node_teacher", END)

graph.add_edge("intent_node_assignement", "node_assignement")
graph.add_edge("node_assignement", END)

graph.add_edge("intent_node_term_mark", "node_term_mark")
graph.add_edge("node_term_mark", END)

graph.add_edge("intent_node_subject_term_mark_split", "node_subject_term_mark_split")
graph.add_edge("node_subject_term_mark_split", END)

office_staff_graph = graph.compile()