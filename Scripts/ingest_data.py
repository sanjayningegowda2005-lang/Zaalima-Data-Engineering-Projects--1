"""
Data Ingestion Engine
Author: Sanjay (Team Lead)
Description: Reads raw CSV data and stages it for ETL processing.
"""
import csv
import logging
from pathlib import Path

def ingest_raw_data(data_dir: Path):
    """Reads raw_data.csv from the data directory and returns ingested records."""
    file_path = data_dir / "raw_data.csv"
    
    logging.info(f"Searching for raw data file at: {file_path}")
    
    if not file_path.exists():
        logging.error(f"Raw data file not found at {file_path}")
        return []

    records = []
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            records.append(row)
            
    logging.info(f"Successfully ingested {len(records)} records from CSV.")
    return records