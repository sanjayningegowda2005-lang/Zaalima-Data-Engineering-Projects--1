"""
SQL Views Execution Engine
Author: Sanjay (Team Lead)
Description: Builds analytical reporting views inside SQLite staging database.
"""
import sqlite3
import logging
from pathlib import Path

def create_analytical_views(db_path: Path, sql_file_path: Path):
    """
    Executes SQL script containing analytical view definitions.
    """
    if not db_path.exists():
        logging.error(f"Database file not found at {db_path}")
        return False

    if not sql_file_path.exists():
        logging.error(f"SQL file not found at {sql_file_path}")
        return False

    logging.info(f"Executing SQL views from: {sql_file_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        
        logging.info("[PASS] Analytical SQL Views successfully created in SQLite.")
        return True

    except Exception as e:
        logging.error(f"Failed to create SQL views: {e}")
        return False