import pandas as pd
import json
from DATAB import insert_from_csv

def read_csv_file(file_path):
    return pd.read_Csv(file_path)
def read_excel_file(file_path):
    return pd.read_csv(file_path)

def load_schema(schema_file="schema.json"):
    try:
        with open(schema_file,"r") as f:
            schema=json.load(f)
        print("schema loaded successfully")
        return schema
    except Exception as e:
        print("error loading schema:",e)
        return None
def safe_read_csv(file_path):
    for enc in ["utf-8", "latin-1"]:
        try:
            df=pd.read_csv(file_path,encoding=enc)
            print("Read successful with",enc)
            return df
        except Exception as e:
            print("Failed with", enc, ":", e)
            continue
    print("Failed to read file with common encodings.")
    return None
def push_to_database(file_path):
    df=safe_read_csv(file_path)
    if df is not None:
        insert_from_csv(df)
    else:
        print( "No data ingested due to file read failure.")
if __name__=="__main__":
    schema=load_schema()
    print("Schema:", schema)
    push_to_database(r"C:\Users\abhik\OneDrive\Documents\telco.csv")
    