import pandas as pd
from typing import List, Dict


class Validator:
    def __init__(self):
        pass

    def validate_column(self, required: List[str], available: List[str]):
        missing = set(required) - set(available)
        if missing:
            return {"status": "error", "missing_columns": list(missing)}
        return {"status": "success"}

    def validate_types(
        self,
        required_type: Dict[str, Dict[str, str]],
        available_type: Dict[str, Dict[str, str]],
    ):
        mismatch = set(required_type.values()) - set(available_type.values())
        if mismatch:
            return {"status": "error", "mismatched_types": list(mismatch)}
        return {"status": "success"}

    def check_completeness(self, data: pd.DataFrame):
        missing = data.isna().any()
        print(missing)

