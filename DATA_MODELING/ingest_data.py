import pandas as pd
import json
import logging
import os
import requests
import time
from DATAB import insert_from_csv, table_creation,get_connection
conn=get_connection()
# Ensure logs directory exists
os.makedirs("logs",exist_ok=True)
#CONFIGURE LOGGING
logging.basicConfig(filename="logs/ingestion.log",
                    level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

def load_schema(schema_file="schema.json"):
    try:
        with open(schema_file, "r") as f:
            schema = json.load(f)
        print("Schema loaded successfully")
        return schema
    except Exception as e:
        print("Error loading schema:", e)
        return None

def validate_file_extension(file_path):
    allowed=[".csv",".xlsx"]
    if any(file_path.endswith(ext) for ext in allowed):
        logging.info(f"File extension validated: {file_path}")
        return True
    else:
        logging.error(f"Invalid file extension:{file_path}")
        return False

def validate_schema(file_path,schema):
    try:
        df=pd.read_csv(file_path)
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
    response=requests.get(url)
    response.raise_for_status()
    data=response.json()
    return pd.DataFrame(data)

#data cleaning
def clean_dataframe(df):
    df=df.map(lambda x: x.strip() if isinstance(x,str) else x)
    df=df.convert_dtypes()
    return df

#BENCHMARKING RUNTIME
def benchmark_ingestion(file_path):
    start=time.time()
    df=pd.read_csv(file_path)
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
