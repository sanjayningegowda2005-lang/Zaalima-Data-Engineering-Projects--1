import sqlite3
import pandas as pd

def execute_sql_file(db_path="telecom_staging.db", sql_file="SQL/analysis.sql"):
    conn = sqlite3.connect(db_path)
    with open(sql_file, 'r') as f:
        sql_script = f.read()
    
    # Split individual queries by semicolon
    queries = [q.strip() for q in sql_script.split(';') if q.strip()]
    
    for i, query in enumerate(queries, 1):
        print(f"\n--- Query {i} Results ---")
        df = pd.read_sql_query(query, conn)
        print(df.to_string(index=False))
        
    conn.close()

if __name__ == "__main__":
    execute_sql_file()