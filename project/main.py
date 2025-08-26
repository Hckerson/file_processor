import argparse
import os
import sys
from .logging import Logger
from .reader import CsvReader
from .processor import process_file
from config.config import get_config


def Main(args):
    filename = args.file
    cfg = get_config()
    ##validate config
    cfg.validate()
    logger_instance = Logger(cfg.logs_dir)
    logger = logger_instance.setup_logging()
    input_dir = cfg.input_dir
    file_path = os.path.join(input_dir, filename)
    process_file(file_path, cfg, logger)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="main.py",
        description="A file processor",
        epilog="reads csv file and validates it",
    )
    parser.add_argument("file", help="File name", type=str)
    parser.add_argument("--date", "-d", help="Date parse option", action="store_true")
    args = parser.parse_args()
    Main(args)
