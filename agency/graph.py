from langgraph.graph import StateGraph, END
from agency.state import AgencyState
from agency.nodes import researcher_node, writer_node, editor_node

def build_agency_graph():
    workflow = StateGraph(AgencyState)

    # Add the agents to the graph
    workflow.add_node("Researcher", researcher_node)
    workflow.add_node("Writer", writer_node)
    workflow.add_node("Editor", editor_node)

    # Set the starting point
    workflow.set_entry_point("Researcher")

    # Define the flow: Researcher -> Writer -> Editor
    workflow.add_edge("Researcher", "Writer")
    workflow.add_edge("Writer", "Editor")

    # The Router: Decide if we are done or need revisions
    def router(state: AgencyState):
        if "APPROVED" in state["feedback"] or state.get("revision_count", 0) >= 3:
            return END
        return "Writer" # Send back to writer if not approved

    # Add conditional logic after the editor
    workflow.add_conditional_edges("Editor", router)

    # Compile the graph
    return workflow.compile()