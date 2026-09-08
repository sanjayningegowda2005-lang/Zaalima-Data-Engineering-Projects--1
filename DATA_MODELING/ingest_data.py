import pandas as pd
import json
import logging
import os
from pathlib import Path
try:
    from .DATAB import insert_from_csv, table_creation
except ImportError:
    from DATAB import insert_from_csv, table_creation

BASE_DIR = Path(__file__).resolve().parent

# Ensure logs directory exists
os.makedirs(BASE_DIR / "logs", exist_ok=True)
#CONFIGURE LOGGING
logging.basicConfig(filename=BASE_DIR / "logs" / "ingestion.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def load_schema(schema_file=None):
    try:
        schema_path = Path(schema_file) if schema_file else BASE_DIR / "schema.json"
        with open(schema_path, "r") as f:
            schema = json.load(f)
        print("Schema loaded successfully")
        return schema
    except Exception as e:
        print("Error loading schema:", e)
        return None

def validate_file_extension(file_path):
    allowed=[".csv",".xlsx"]
    file_path = os.fspath(file_path)
    if any(file_path.lower().endswith(ext) for ext in allowed):
        logging.info(f"File extension validated: {file_path}")
        return True
    else:
        logging.error(f"Invalid file extension:{file_path}")
        return False

def validate_schema(file_path,schema):
    try:
        df=pd.read_csv(file_path, encoding="utf-8-sig")
        df.columns = (
            df.columns.astype(str)
            .str.replace("\ufeff", "", regex=False)
            .str.replace("ï»¿", "", regex=False)
            .str.strip()
        )
        expected_cols=schema.get("customer_churn",{}).get("columns",[])
        if set(expected_cols)==set(df.columns):
            logging.info("Schema validation passed")
            return True
        else:
            logging.error(f"Schema mismatch.Expected:{expected_cols}, Found: {list(df.columns)}")
            return False
    except Exception as e:
        logging.error(f"Error validating schema:{e}")
        return False
    

def safe_read_csv(file_path):
    for enc in ["utf-8", "latin-1"]:
        try:
            df = pd.read_csv(file_path, encoding=enc)
            print("Read successful with", enc)
            return df
        except Exception as e:
            print("Failed with", enc, ":", e)
            continue
    print("Failed to read file with common encodings.")
    return None


def clean_dataframe(df):
    """Trim string values and use pandas' nullable dtypes."""
    cleaned = df.map(lambda value: value.strip() if isinstance(value, str) else value)
    return cleaned.convert_dtypes()

def push_to_database(file_path,schema):
    if not validate_file_extension(file_path):
        return
    if not validate_schema(file_path, schema):
        return
    try:
        insert_from_csv(file_path)
        logging.info(f"Data pushed to database from {file_path}")
    except Exception as e:
        logging.error(f"Error pushing data to database: {e}")

if __name__ == "__main__":
    schema = load_schema()
    table_creation()
    push_to_database(BASE_DIR / "Telco.csv", schema)
