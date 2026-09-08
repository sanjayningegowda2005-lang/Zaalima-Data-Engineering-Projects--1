import pandas as pd
import json
import logging
import os
import requests
import time
from pathlib import Path
from DATAB import insert_from_csv, table_creation,get_connection

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
    if Path(file_path).suffix.lower() in allowed:
        logging.info(f"File extension validated: {file_path}")
        return True
    else:
        logging.error(f"Invalid file extension:{file_path}")
        return False

def validate_schema(file_path,schema):
    try:
        reader = pd.read_excel if Path(file_path).suffix.lower() == ".xlsx" else pd.read_csv
        df=reader(file_path)
        expected_cols=schema.get("customer_churn",{}).get("columns",[])
        expected_cols = [
            column.get("name", "") if isinstance(column, dict) else column
            for column in expected_cols
        ]
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
#INCREMENTAL LOADING(DUPLICATE DETECTION)
def load_incremental(file_path,conn,table_name):
    if table_name != "customer_churn":
        raise ValueError("Unsupported table name")
    df=pd.read_csv(file_path)
    #fetch existing keys from DB
    with conn.cursor() as cur:
        cur.execute(f"SELECT customerID FROM {table_name}")
        existing_keys={row[0] for row in cur.fetchall()}
    #filter new records
    new_records=df[~df['customerID'].isin(existing_keys)]
    return new_records

#API DATA FETCHING
def fetch_api_data(url):
    response=requests.get(url, timeout=30)
    response.raise_for_status()
    data=response.json()
    if not isinstance(data, list):
        raise ValueError("API response must be a JSON array")
    return pd.DataFrame(data)

#data cleaning
def clean_dataframe(df):
    df=df.map(lambda x: x.strip() if isinstance(x,str) else x)
    df=df.convert_dtypes()
    return df

#BENCHMARKING RUNTIME
def benchmark_ingestion(file_path):
    start=time.time()
    reader = pd.read_excel if Path(file_path).suffix.lower() == ".xlsx" else pd.read_csv
    df=reader(file_path)
    end=time.time()
    print(f"Execution time :{end-start:.2f} seconds")
    return df

if __name__ == "__main__":
    schema = load_schema()
    table_creation()
    push_to_database("Telco.csv",schema)
    #incremental loading example
    conn=get_connection()
    new_records=load_incremental("mock_data.csv",conn,"customer_churn")
    if not new_records.empty:
        logging.info(f"Incremental load:{len(new_records)} new records found")
    conn.close()
    api_df=fetch_api_data("https://jsonplaceholder.typicode.com/posts")
    api_df=clean_dataframe(api_df)
    logging.info(f"API ingestion :{len(api_df)} records fetched")
    benchmark_ingestion("Telco.csv")
