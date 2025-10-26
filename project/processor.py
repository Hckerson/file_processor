import os
import shutil
import pandas as pd
from pathlib import Path
from json import loads, dumps
from loguru import logger 
from .validator import Validator
from config.config import AppConfig
from .transformer import Transformer


def process_file(file_path: Path, cfg: AppConfig):
    validator = Validator()
    output_dir = Path(cfg.output_dir)
    logger.info(f"Processing file: {file_path}")
    processed_dir = Path(cfg.processed_dir)

    ## read the file
    try:
        with open(file_path, "r") as file:
            ##check if date is a expected column
            columns = cfg.get("required_column", [])
            if "date" in columns:
                data = pd.read_csv(file, parse_dates=["date"])
            else:
                data = pd.read_csv(file)
    except Exception as e:
        logger.error(f"Failed to read file {file_path}:{e}")
        return

    ## check constraints
    required_columns = cfg.get("required_column", [])
    required_column_types = cfg.get("column_type", {})
    column_available = data.columns.to_list()
    column_available_types = data.dtypes.to_dict()

    try:
        column_check = validator.validate_column(required_columns, column_available)
        if column_check["status"] == "error":
            logger.error(
                f"Column validation failed for file {file_path}: {column_check['missing_columns']}"
            )
            move_file("error", file_path, processed_dir)
            return
    except Exception as e:
        logger.error(f"Column validation error for file {file_path}: {e}")
        return

    try:
        type_check = validator.validate_types(
            required_column_types, column_available_types
        )
        if type_check["status"] == "error":
            logger.error(
                f"Type validation failed for file {file_path}: {type_check['mismatched_types']}"
            )
            move_file("error", file_path, processed_dir)
            return
    except Exception as e:
        logger.error(f"Type validation failed for file {file_path}: {e}")
        return {"status": "error"}

    ## check completeness
    try:
        completeness_check = validator.check_completeness(data)
        if completeness_check["status"] == "error":
            logger.error(
                f"Completeness check failed for file {file_path}: {completeness_check['incomplete_columns']}"
            )
            move_file("error", file_path, processed_dir)
            return
    except Exception as e:
        logger.error(f"Completeness check failed for file {file_path}: {e}")
        return

    ##transform data
    transformer = Transformer(data, file_path, cfg)

    try:
        date_converted = transformer.convert_date()
        if date_converted["status"] == "error":
            logger.error(f"Date transformation failed for file {file_path}")

        currency_converted = transformer.currency_converter(
            cfg.get("currency_rate", 1.0)
        )
        if currency_converted["status"] == "error":
            logger.error(f"Currency transformation failed for file {file_path}")
            move_file("error", file_path, processed_dir)
            return
    except Exception as e:
        logger.error(f"transformation failed for file {file_path}: {e}")
        return

    ## covert to json
    try:
        data_converted = transformer.data_converter()
        if data_converted["status"] == "error":
            logger.error(
                f"Data conversion to required format failed for file {file_path}"
            )
            move_file("error", file_path, processed_dir)
            return
        data = data_converted["data"]
        move_file("success", file_path, processed_dir)
    except Exception as e:
        logger.error(
            f"Failed to convert dataframe to required output format for file {file_path}: {e}  "
        )
        return

    ## output transformed data
    
    parsed_data = loads(data)
    file_name = output_dir / f"{file_path.stem}.json"
    with open(file_name, "w") as outfile:
        outfile.write(dumps(parsed_data, indent=2))


def move_file(status: str, file_path: Path, dest: Path): 
    try:
        destination_address = (
            dest / "success" if status == "success" else dest / "error"
        )
        os.makedirs(destination_address, exist_ok=True)
        shutil.move(str(file_path), str(destination_address))
    except Exception as e:
        print(f"Failed to move file {file_path} to {destination_address}: {e.__class__.__name__}")
