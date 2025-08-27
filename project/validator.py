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
        required_type: Dict[str, str],
        available_type: Dict[str, str],
    ):
        issues = []

        for column in required_type.keys():
            if required_type[column] != available_type.get(column, None):
                if column == "date":
                    if available_type.get(column, None) in [
                        "datetime64[ns]",
                        "datetime64[ns, UTC]",
                    ]:
                        continue
                    issues.append(column)
                else:
                    if available_type.get(column, None) == "object":
                        continue
                    issues.append(column)

        if issues:
            return {"status": "error", "mismatched_types": issues}
        return {"status": "success"}

    def check_completeness(self, data: pd.DataFrame):
        missing = data.isna().any()
        if missing.any():
            cols = data.columns[missing].tolist()
            return {"status": "error", "incomplete_columns": cols}
        return {"status": "success"}
