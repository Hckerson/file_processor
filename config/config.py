import os
import datetime
from dataclasses import dataclass

@dataclass()
class AppConfig:
    current_dir: str = os.path.abspath(os.path.dirname(__file__))
    project_root: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    ## Paths
    output_dir: str = os.path.join(project_root, "output")
    input_dir: str = os.path.join(project_root, "input")
    logs_dir: str = os.path.join(output_dir, "logs")

def ensure_path(cfg: AppConfig):
    for path in [cfg.logs_dir, cfg.output_dir]:
        os.makedirs(path, exist_ok=True)


def get_config():
    cfg = AppConfig()
    ensure_path(cfg)
    return cfg
