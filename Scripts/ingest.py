import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def ingest_data(file_path="Data/telecom_customer_churn.csv"):
    logging.info(f"Loading raw data from {file_path}...")
    df = pd.read_csv(file_path)
    logging.info(f"Successfully ingested dataset: {df.shape[0]} rows, {df.shape[1]} columns.")
    return df

if __name__ == "__main__":
    df = ingest_data()
    print(df.head(3))