import os
import yaml
import datetime
from pathlib import Path
from dataclasses import dataclass


DEFAULT_CONFIG = {
    "required_column": ["name", "date", "amount"],
    "column_type": {"name": "str", "date": "date", "amount": "float"},
    "date_format": "%Y-%m-%d",
    "currency_conversion": {"from": "EUR", "to": "USD"},
    "output_currency_symbol": "$",
}


class AppConfigError(Exception):
    """Error class for handling config errors"""

    pass


@dataclass()
class AppConfig:
    current_dir: str = os.path.abspath(os.path.dirname(__file__))
    project_root: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    ## Paths
    output_dir: str = os.path.join(project_root, "output")
    input_dir: str = os.path.join(project_root, "input")
    logs_dir: str = os.path.join(output_dir, "logs")

    ## config file
    CONFIG_FILE = "config.yml"

    p = Path(CONFIG_FILE)
    if not p.exists():
        p.write_text(yaml.safe_dump(DEFAULT_CONFIG))
    _data = yaml.safe_load(p.read_text())

    def validate(self) -> None:
        # minimal validation
        if "required_column" not in self._data:
            raise AppConfigError("required_column is missing in config")
        if "column_type" not in self._data:
            raise AppConfigError("column_type is missing in config")

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def as_dict(self):
        return dict(self._data)


def ensure_path(cfg: AppConfig):
    for path in [cfg.logs_dir, cfg.output_dir, cfg.input_dir]:
        os.makedirs(path, exist_ok=True)


def get_config():
    cfg = AppConfig()
    ensure_path(cfg)
    return cfg
