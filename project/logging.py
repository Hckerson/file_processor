import sys
from loguru import logger


class Logger:
    def __init__(self, logs_dir: str):
        self.logs_dir = logs_dir

    def setup_logging(self):
        logger.remove()
        logger.add(
            sys.stdout,
            level="INFO",
            format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>",
        )
        logger.add(
            f"{self.logs_dir}/info.logs", level="INFO", enqueue=True, rotation="10 MB"
        )
        logger.add(
            f"{self.logs_dir}/error.logs", level="ERROR", enqueue=True, rotation="10 MB"
        )
        return logger
