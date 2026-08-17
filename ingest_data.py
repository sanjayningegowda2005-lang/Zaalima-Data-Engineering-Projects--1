import pandas as pd
import json
from DATAB import insert_from_csv, table_creation

def load_schema(schema_file="schema.json"):
    try:
        with open(schema_file, "r") as f:
            schema = json.load(f)
        print("Schema loaded successfully")
        return schema
    except Exception as e:
        print("Error loading schema:", e)
        return None

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

def push_to_database(file_path):
    # Pass file path directly to insert_from_csv
    insert_from_csv(file_path)

if __name__ == "__main__":
    schema = load_schema()
    print("Schema:", schema)
    table_creation()
    push_to_database("Telco.csv")
