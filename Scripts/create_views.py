import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def build_views(db_path="telecom_staging.db", sql_file="SQL/views.sql"):
    logging.info(f"Connecting to database {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    logging.info(f"Executing SQL view definitions from {sql_file}...")
    with open(sql_file, 'r') as f:
        sql_script = f.read()
        
    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    
    logging.info("SQL Views created successfully in SQLite database!")

if __name__ == "__main__":
    build_views()