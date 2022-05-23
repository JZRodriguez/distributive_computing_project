"""
Script to load the contents of the csv files into the database.
"""
import os
import sys
import time
import uuid
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
USER = config['POSTGRES']['USER']
PASSWORD = config['POSTGRES']['PASSWORD']
HOST = config['POSTGRES']['HOST']
PORT = config['POSTGRES']['PORT']
DATABASE_NAME = config['POSTGRES']['DATABASE_NAME']
CSV_FOLDER = config['CSV']['FOLDER']

def read_csv(file_name) -> pd.DataFrame:
    """
    Reads the csv file and returns a dataframe.
    """
    return pd.read_csv(file_name)

def load_in_database(df: pd.DataFrame, table_name: str, engine: create_engine) -> None:
    """
    Loads the dataframe into the database.
    """
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print("Data uploaded successfully.")
    except IntegrityError as e:
        print(e)
        print(f'{table_name} already exists. Skipping...')


def assign_unique_id(df: pd.DataFrame) -> pd.DataFrame:
    """
    Assigns a unique id in uuid4 format to each row based on the title.
    """
    df['id'] = df['title'].apply(lambda x: str(x).replace(' ', '-'))
    return df

def main():
    """
    Main function.
    """

    # Get the path of the csv files.
    csv_files = [os.path.join(CSV_FOLDER, f) for f in os.listdir(CSV_FOLDER) if f.endswith('.csv')]

    # Create the engine in PostgreSQL.
    engine = create_engine(f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}')

    # Create the session.
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load the data into the database.
    for csv_file in csv_files:
        # Get the table name.
        table_name = os.path.splitext(os.path.basename(csv_file))[0]

        # Read the csv file.
        df = read_csv(csv_file)

        # Clean the dataframe.
        df.dropna(inplace=True)

        # Assign a unique id to each row.
        df = assign_unique_id(df)

        # Load the data into the database.
        load_in_database(df, table_name, engine)

    # Close the session.
    session.close()


if __name__ == '__main__':
    main()