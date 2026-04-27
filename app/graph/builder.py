from langgraph.graph import StateGraph, END

from app.graph.state import GraphState
from app.nodes.input_node import input_node
from app.nodes.extraction_node import extraction_node
from app.nodes.validation_node import validation_node
from app.nodes.repair_node import repair_node
from app.nodes.output_node import output_node


def should_repair(state: GraphState):
    if state["missing_fields"] and state["iteration_count"] < 2:
        return "repair"
    return "output"


def build_graph():
    builder = StateGraph(GraphState)

    builder.add_node("input", input_node)
    builder.add_node("extract", extraction_node)
    builder.add_node("validate", validation_node)
    builder.add_node("repair", repair_node)
    builder.add_node("output", output_node)

    builder.set_entry_point("input")

    builder.add_edge("input", "extract")
    builder.add_edge("extract", "validate")

    builder.add_conditional_edges(
        "validate",
        should_repair,
        {
            "repair": "repair",
            "output": "output",
        },
    )

    builder.add_edge("repair", "validate")
    builder.add_edge("output", END)

    return builder.compile()