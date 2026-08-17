"""
Database Loading & Staging Engine
Author: Sanjay (Team Lead)
Description: Creates staging tables and loads clean records into SQLite database.
"""
import sqlite3
import logging
from pathlib import Path

def load_to_sqlite(transformed_records, db_path: Path):
    """
    Creates staging_orders table if it doesn't exist and inserts clean records.
    """
    if not transformed_records:
        logging.warning("No records provided to load into the database.")
        return

    logging.info(f"Connecting to SQLite database at: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Create staging table schema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS staging_orders (
                order_id INTEGER PRIMARY KEY,
                customer_name TEXT,
                product TEXT,
                quantity INTEGER,
                unit_price REAL,
                total_amount REAL,
                order_date TEXT
            )
        """)

        # Insert or update records using dictionary keys
        insert_query = """
            INSERT OR REPLACE INTO staging_orders 
            (order_id, customer_name, product, quantity, unit_price, total_amount, order_date)
            VALUES (:order_id, :customer_name, :product, :quantity, :unit_price, :total_amount, :order_date)
        """

        cursor.executemany(insert_query, transformed_records)
        conn.commit()
        
        # Verify database row count
        cursor.execute("SELECT COUNT(*) FROM staging_orders")
        count = cursor.fetchone()[0]
        
        conn.close()
        logging.info(f"Successfully staged {len(transformed_records)} records into 'staging_orders' table. Total rows: {count}")

    except Exception as e:
        logging.error(f"Failed to load data into database: {e}")