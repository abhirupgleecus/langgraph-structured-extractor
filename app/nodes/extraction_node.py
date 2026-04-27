import json
import re
from app.graph.state import GraphState
from app.llm.gemini_client import get_llm
from app.utils.parsing import safe_json_parse

llm = get_llm()


def extraction_node(state: GraphState) -> GraphState:
    paragraph = state["paragraph"]
    schema = state["schema"]
    keys = list(schema.keys())

    prompt = f"""
        Extract structured data from the paragraph.

        Paragraph:
        {paragraph}

        Schema fields:
        {keys}

        Rules:
        - Return STRICT JSON only
        - Keys MUST match schema exactly
        - If value not found, return ""
        - Do NOT add explanation or extra text

        Example:
        {{
        "name": "John",
        "age": "",
        "city": "Bangalore"
        }}
        """

    raw_response = llm.invoke(prompt)

    # Normalize response to string
    if isinstance(raw_response.content, list):
        response = " ".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in raw_response.content
        )
    else:
        response = raw_response.content

    extracted = safe_json_parse(response, keys)

    # Ensure all keys exist (VERY IMPORTANT)
    extracted = {k: extracted.get(k, "") for k in keys}

    return {
        "extracted_data": extracted
    }