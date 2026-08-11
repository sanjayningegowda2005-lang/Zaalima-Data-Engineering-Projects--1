import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def validate_staging(db_path="telecom_staging.db", table_name="stg_customer_churn"):
    logging.info("Running data quality validations...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Row count validation
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    
    # 2. Primary key integrity validation
    cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE customer_id IS NULL")
    null_keys = cursor.fetchone()[0]
    
    conn.close()
    
    if count == 0:
        raise ValueError("Validation failed: Staging table is empty!")
    if null_keys > 0:
        raise ValueError(f"Validation failed: Found {null_keys} null customer IDs!")
        
    logging.info(f"Validation passed: {count} records verified with 0 null primary keys.")
    return True

if __name__ == "__main__":
    validate_staging()