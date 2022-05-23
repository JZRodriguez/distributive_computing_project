"""
Script to process the data from the raw data and clean
the csv files to upload them to the database.
"""
import pandas as pd

def read_csv(file_name) -> pd.DataFrame:
    """
    Reads the csv file and returns a dataframe.
    """
    return pd.read_csv(file_name)
