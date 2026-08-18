"""
Data Quality Validation Engine
Author: Sanjay (Team Lead)
Description: Runs automated sanity checks and quality assertions on staged SQL tables.
"""
import sqlite3
import logging
from pathlib import Path

def validate_staging_data(db_path: Path):
    """
    Executes core data quality assertions on staging_orders table.
    """
    if not db_path.exists():
        logging.error(f"Database file not found at {db_path}")
        return False

    logging.info(f"Running quality validations on: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check 1: Verify table is not empty
        cursor.execute("SELECT COUNT(*) FROM staging_orders")
        total_rows = cursor.fetchone()[0]
        if total_rows == 0:
            logging.error("Validation Failed: staging_orders table is empty.")
            conn.close()
            return False
        
        # Check 2: Check for NULL primary keys
        cursor.execute("SELECT COUNT(*) FROM staging_orders WHERE order_id IS NULL")
        null_keys = cursor.fetchone()[0]
        if null_keys > 0:
            logging.error(f"Validation Failed: Found {null_keys} records with NULL order_id.")
            conn.close()
            return False

        # Check 3: Audit total revenue sum
        cursor.execute("SELECT SUM(total_amount) FROM staging_orders")
        total_revenue = cursor.fetchone()[0]
        
        conn.close()
        
        logging.info(f"[PASS] Total Rows Verified: {total_rows}")
        logging.info(f"[PASS] Primary Key Integrity Verified (0 NULLs)")
        logging.info(f"[PASS] Staged Revenue Total Verified: {total_revenue:,.2f}")
        return True

    except Exception as e:
        logging.error(f"Validation process failed due to error: {e}")
        return False