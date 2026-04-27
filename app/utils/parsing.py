import json
import re


def safe_json_parse(text, keys):
    if not isinstance(text, str):
        text = str(text)

    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass

    return {k: "" for k in keys}