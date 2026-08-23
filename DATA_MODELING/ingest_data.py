import pandas as pd
import json
import os
import logging
from DATAB import insert_from_csv, table_creation

if not os.path.exists("logs"):
    os.makedirs("logs")
    
#CONFIGURE LOGGING
logging.basicConfig(
    filename="logs/ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def validate_file_extension(file_path):
    valid_extensions=[".csv",".xlsx"]
    ext=os.path.splitext(file_path)[1].lower()
    if ext not in valid_extensions:
        raise ValueError("Invalid file format:" + ext)
    print("File extension validated:",ext)
    return True


def load_schema(schema_file="schema.json"):
    try:
        with open(schema_file, "r") as f:
            schema = json.load(f)
        print("Schema loaded successfully")
        return schema
    except Exception as e:
        print("Error loading schema:", e)
        return None
    
def validate_schema(df, schema):
    expected_columns = list(schema["customer_churn"]["columns"].keys())
    file_columns = list(df.columns)

    if set(expected_columns) != set(file_columns):
        raise ValueError("Schema mismatch! Expected " + str(expected_columns) + " got " + str(file_columns))
    print("Schema validated successfully")
    return True
    

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

def log_ingestion(file_path,rows):
    logging.info("File:%s, Rows:%d, Status: Success",file_path,rows)

def push_to_database(file_path,schema_file):
    try:
        validate_file_extension(file_path)
        df = safe_read_csv(file_path)
        if df is not None:
            schema = load_schema(schema_file)
            if schema:
                validate_schema(df, schema)
                insert_from_csv(file_path)   # Pass DataFrame instead of file path
                log_ingestion(file_path, len(df))
                print("Data pushed to database successfully")
            else:
                print("Schema not loaded, skipping ingestion")
        else:
            print("No data ingested due to file read failure")
    except Exception as e:
        logging.error("Ingestion failed for %s: %s", file_path, e)
        print("Error during ingestion:", e)

if __name__ == "__main__":
    schema = load_schema("C:/Users/abhik/Desktop/DATA/DATA_MODELING/schema.json")
    print("Schema:", schema)
    table_creation()
    push_to_database("C:/Users/abhik/Desktop/DATA/DATA_MODELING/Telco.csv", "C:/Users/abhik/Desktop/DATA/DATA_MODELING/schema.json")
