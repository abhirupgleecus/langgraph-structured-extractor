import json
import re
from app.graph.state import GraphState
from app.llm.gemini_client import get_llm
from app.utils.parsing import safe_json_parse

llm = get_llm()


def repair_node(state: GraphState) -> GraphState:
    paragraph = state["paragraph"]
    data = state["extracted_data"]
    missing = state["missing_fields"]
    keys = list(data.keys())

    prompt = f"""
        You are repairing missing fields in structured data.

        Paragraph:
        {paragraph}

        Current data (DO NOT MODIFY EXISTING VALUES):
        {data}

        Missing fields:
        {missing}

        Rules:
        - ONLY fill missing fields
        - DO NOT change existing values
        - If value cannot be inferred:
            - use "unknown" or "not mentioned"
        - Return FULL JSON with ALL fields
        - No explanations, only JSON

        Output:
        {{
        "field": "value"
        }}
        """

    raw_response = llm.invoke(prompt)

    # normalize response
    if isinstance(raw_response.content, list):
        response = " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in raw_response.content
        )
    else:
        response = raw_response.content

    repaired = safe_json_parse(response, keys)

    # 🔒 HARD LOCK: prevent overwriting existing values
    final_data = {}
    for k in keys:
        if data.get(k) not in ["", None]:
            final_data[k] = data[k]  # keep original
        else:
            final_data[k] = repaired.get(k, "")

    return {
        "extracted_data": final_data,
        "iteration_count": state["iteration_count"] + 1
    }