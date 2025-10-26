import sys
from pathlib import Path  
from loguru import logger


class Logger:
    def __init__(self, logs_dir: Path):
        self.logs_dir = logs_dir
        self.setup_logging()

    def setup_logging(self):
        logger.remove()
        logger.add(
            f"{self.logs_dir}/info.logs", level="INFO", enqueue=True, rotation="10 MB"
        )
        logger.add(
            f"{self.logs_dir}/error.logs", level="ERROR", enqueue=True, rotation="10 MB"
        )
        
