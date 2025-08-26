import pandas as pd
from pathlib import Path
from .validator import Validator
from config.config import AppConfig


def process_file(file_path: str, cfg: AppConfig, logger):
    validator = Validator()
    logger.info(f"Processing file: {file_path}")

    ## read the file
    try:
        with open(file_path, "r") as file:
            data = pd.read_csv(file, parse_dates=True)
            content = pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Failed to read file {file_path}:{e}")
        return {"status": "error", "reason": f"read failed: {e}"}

    ## check constraints
    required_columns = cfg.get("required_column", [])
    required_column_types = cfg.get("column_type", {})
    column_available = content.columns.to_list()
    column_available_types = content.dtypes.to_dict()

    try:
        column_check = validator.validate_column(required_columns, column_available)
        if column_check["status"] == "error":
            logger.error(
                f"Column validation failed for file {file_path}: {column_check['missing_columns']}"
            )
            return {
                "status": "error",
                "reason": f"column validation failed: {column_check['missing_columns']}",
            }
    except Exception as e:
        logger.error(f"Column validation error for file {file_path}: {e}")
        return {"status": "error", "reason": f"column validation failed: {e}"}

    try:
        type_check = validator.validate_types(
            required_column_types, column_available_types
        )
        if type_check["status"] == "error":
            logger.error(
                f"Type validation failed for file {file_path}: {type_check['mismatched_types']}"
            )
            return {
                "status": "error",
                "reason": f"type validation failed: {type_check['mismatched_types']}",
            }
    except Exception as e:
        logger.error(f"Type validation failed for file {file_path}: {e}")
        return {"status": "error", "reason": f"type validation failed: {e}"}


    ## check completeness
