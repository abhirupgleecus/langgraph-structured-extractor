from app.graph.state import GraphState
from app.utils.formatting import to_dataframe


def output_node(state: GraphState) -> GraphState:
    df = to_dataframe(state["extracted_data"])

    return {
        "final_table": df
    }