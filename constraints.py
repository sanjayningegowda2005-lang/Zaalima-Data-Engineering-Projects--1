import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
def add_constraints():
    alter_table_query = """
    ALTER TABLE customer_churn
    ALTER COLUMN gender SET NOT NULL,
    ALTER COLUMN SeniorCitizen SET NOT NULL,
    ALTER COLUMN tenure SET NOT NULL,
    ALTER COLUMN InternetService SET NOT NULL,
    ALTER COLUMN Contract SET NOT NULL,
    ALTER COLUMN MonthlyCharges SET NOT NULL,
    ALTER COLUMN churn SET NOT NULL,
    """
    try:
        conn=psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur=conn.cursor()
        cur.execute(alter_table_query)
        cur.commit()
        cur.close()
        conn.close()
        print("Constraints added successfully.")
    except Exception as e:
        print("Error adding constraints:", e)