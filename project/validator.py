import pandas as pd


class Validator:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.is_empty: bool = self.check_if_empty()
        self.is_null = self.check_if_null()


    def check_if_empty(self):
        return self.data.empty
    
    def check_if_null(self):
        return self.data.isnull().values.any()
    
    
