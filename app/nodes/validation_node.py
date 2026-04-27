from app.graph.state import GraphState


def validation_node(state: GraphState) -> GraphState:
    data = state["extracted_data"]

    missing = [
        k for k, v in data.items()
        if v in ["", None]
    ]

    return {
        "missing_fields": missing
    }