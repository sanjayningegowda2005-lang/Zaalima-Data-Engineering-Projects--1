import os
import psycopg2
from dotenv import load_dotenv
import pathlib
#load env variables
env_path=pathlib.Path(__file__).resolve().parent/'.env'
load_dotenv(dotenv_path=env_path)
#create audit log table
def create_audit_table():
    """Create audit_log table if it doesn't exist."""
    try:
        conn=psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur=conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS audit_log(
        id SERIAL PRIMARY KEY,
        run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        table_name VARCHAR(100) NOT NULL,
        rows_inserted INT NOT NULL,
        status VARChAR(20) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Audit log table created successfully.")
    except Exception as e:
        print("Error creating audit_log table:",e)
def log_audit(table_name,rows_inserted,status):
    """Insert a record into audit_log table."""
    try:
        conn=psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur=conn.cursor()
        cur.execute("""
        INSERT INTO audit_log (table_name,rows_inserted,status)
        VALUES(%s,%s,%s);
        """,(table_name,rows_inserted,status))
        conn.commit()
        cur.close()
        conn.close()
        print("Audit log recorded")
    except Exception as e:
        print("Error logging audit:",e)
