import pandas as pd
from pathlib import Path
from .logging import Logger
from config.config import AppConfig


class Transformer:
    def __init__(self, data: pd.DataFrame, file_path: Path, cfg: AppConfig):
        self.data = data
        self.file_path = file_path
        self.logger = Logger(Path(cfg.logs_dir)).setup_logging()
        self.cfg = cfg

    def convert_date(self):
        # converting all date rows to the expected
        self.logger.info(f"Transforming date column for file {self.file_path}")
        try:
            format = self.cfg.get("date_format", "%Y-%m-%d")
            if "date" in self.data.columns:
                self.data["date"] = pd.to_datetime(
                    self.data["date"], format=format, errors="coerce"
                )
                return {"status": "success"}
            return {"status": "failed"}
        except Exception as e:
            self.logger.error(f"Date conversion error for file {self.file_path}: {e}")
            return {"status": "error"}

    def currency_converter(self, rate: str):
        self.logger.info(f"Transforming amount column for file {self.file_path}")
        try:
            self.data["amount"] = self.data["amount"] * rate
            return {"status": "success"}
        except Exception as e:
            self.logger.error(
                f"Currency conversion error for file {self.file_path}: {e}"
            )
            return {"status": "error"}

    def data_converter(self):
        self.logger.info(f"Converting dataframe to required output format")
        format_mapper = {
            "json": self.data.to_json(orient="records"),
            "csv": self.data.to_csv(index=False),
        }
        try:
            ## get required format
            output_format = self.cfg.get("required_output_format")
            json_format = format_mapper.get(output_format)
            return {"status": "success", "data": json_format}
        except Exception as e:
            return {"status": "error"}
