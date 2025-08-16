import argparse
import os
import sys
import logging
from .reader import CsvReader
from .validator import Validator
from config.config import get_config

logger = logging.getLogger(__name__)

def Main(args):
    filename = args.file
    config = get_config()
    logging.basicConfig(filename="main.py", level=logging.INFO)
    csv_reader = CsvReader()
    file_path = os.path.abspath(os.path.join(config.input_dir, filename))
    if(os.path.exists(file_path)):
        print(f"File {filename} exists")
        data = csv_reader.read_csv(file_path, args.date)
        if data is not None:
            validator = Validator(data)
            if validator.is_empty:
                logger.info("File is empty")
            elif validator.is_null:
                logger.info("File has null values")
            else:
                logger.info("File is valid")
  
    else:
        print("File does not exist")
        sys.exit(1)


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
