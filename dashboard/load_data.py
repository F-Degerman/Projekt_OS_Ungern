import pandas as pd
import hashlib as hl
from pathlib import Path

root_dir = Path(__file__).parent
csv_path = root_dir/"data"/"athlete_events.csv"

def load_anonymized_data(path=csv_path):
    """ Reading the Kaggle .csv-file and anonymizing the 'Name' column. Returning a DataFrame. """

    df = pd.read_csv(path)
    anonymized_name = df["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
    df["Name"] = anonymized_name

    return df
