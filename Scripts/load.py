import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_to_sqlite(df: pd.DataFrame, db_path="telecom_staging.db", table_name="stg_customer_churn"):
    logging.info(f"Connecting to SQLite database: {db_path}...")
    conn = sqlite3.connect(db_path)
    
    logging.info(f"Writing data to SQL staging table '{table_name}'...")
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    
    conn.close()
    logging.info("Data successfully persisted to SQL staging table!")

if __name__ == "__main__":
    from ingest import ingest_data
    from transform import transform_data
    
    raw_df = ingest_data()
    cleaned_df = transform_data(raw_df)
    load_to_sqlite(cleaned_df)