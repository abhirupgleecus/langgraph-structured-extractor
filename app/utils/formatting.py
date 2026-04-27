import pandas as pd


def to_dataframe(data: dict) -> pd.DataFrame:
    normalized = {
        k: v if v not in ["", None] else "unknown"
        for k, v in data.items()
    }

    return pd.DataFrame([
        {"Field": k, "Value": v}
        for k, v in normalized.items()
    ])