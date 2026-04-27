from typing import TypedDict, Dict, List, Any
import pandas as pd


class GraphState(TypedDict):
    paragraph: str
    schema: Dict[str, Any]
    extracted_data: Dict[str, Any]
    missing_fields: List[str]
    iteration_count: int
    final_table: pd.DataFrame