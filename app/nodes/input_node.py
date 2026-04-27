from app.graph.state import GraphState


def input_node(state: GraphState) -> GraphState:
    return {
        "paragraph": state["paragraph"],
        "schema": state["schema"],
        "extracted_data": {},
        "missing_fields": [],
        "iteration_count": 0,
    }