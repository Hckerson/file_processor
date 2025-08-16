import os
import pandas as pd
from typing import List, Dict


class CsvReader:
    """
    A class for processing CSV files.
    """

    def __init__(self):
        self.data = None

    def read_csv(self, file_path: str, date_parse: bool = False) -> pd.DataFrame | None:
        """ "
          Read csv file from path and returns status
        Args:
            file_path (str): file path
            date_parse (bool): date parse option
        """
        if os.path.exists(file_path):
            if date_parse:
                self.data = pd.read_csv(file_path, parse_dates=True)
            else:
                self.data = pd.read_csv(file_path)
            return self.data
        return None

    def extract_column(self)-> List[str] | None:
        ## Extract column headers and return a list if data is available
        if self.data is None:
            return
        columns = self.data.columns.tolist()
        return columns
