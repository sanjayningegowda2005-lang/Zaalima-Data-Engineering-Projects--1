import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2
import pathlib
from audit_log import create_audit_table,log_audit

#import constraints from constraints.py
from constraints import add_constraints

# Load environment variables
env_path = pathlib.Path(__file__).resolve().parent / ".env"
print("Loading environment variables from:", env_path)
load_dotenv(dotenv_path=env_path)
# PostgreSQL connection using env variables
def get_postgre_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    con_str = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(con_str)
    return engine

# SQLite connection (optional for testing)
def get_sqlite_engine(db_path="mydb.sqlite"):
    engine = create_engine(f"sqlite:///{db_path}")
    return engine

# Test database connection
def test_connection(engine):
    try:
        with engine.connect() as conn:
            print("Connection successful")
    except Exception as e:
        print("Connection failed:", e)

# Table creation
def table_creation():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS customer_churn (
        customerID VARCHAR(50) PRIMARY KEY,
        gender VARCHAR(10),
        SeniorCitizen INT,
        Partner VARCHAR(10),
        Dependents VARCHAR(10),
        tenure INT,
        PhoneService VARCHAR(10),
        MultipleLines VARCHAR(10),
        InternetService VARCHAR(20),
        OnlineSecurity VARCHAR(10),
        OnlineBackup VARCHAR(10),
        DeviceProtection VARCHAR(10),
        TechSupport VARCHAR(10),
        StreamingTV VARCHAR(10),
        StreamingMovies VARCHAR(10),
        Contract VARCHAR(20),
        PaperlessBilling VARCHAR(10),
        PaymentMethod VARCHAR(50),
        MonthlyCharges FLOAT,
        TotalCharges FLOAT,
        Churn VARCHAR(10)
    );
    """
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        print("Table created successfully")
    except Exception as e:
        print("Error creating table:", e)

# Insert data from CSV
def insert_from_csv(csv_file="Telco.csv"):
    df = pd.read_csv(csv_file)
    df = df.replace(r'^\s*$', None, regex=True)
    #columns are converted to numeric
    df['MonthlyCharges'] = pd.to_numeric(df['MonthlyCharges'], errors='coerce')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    insert_query = """
        INSERT INTO customer_churn (
            customerID, gender, SeniorCitizen, Partner, Dependents,
            tenure, PhoneService, MultipleLines, InternetService,
            OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport,
            StreamingTV, StreamingMovies, Contract, PaperlessBilling,
            PaymentMethod, MonthlyCharges, TotalCharges, Churn
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customerID) DO NOTHING;
    """
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        data = [tuple(x) for _, x in df.iterrows()]
        cur.executemany(insert_query, data)
        conn.commit()
        print("Data inserted successfully")
        #log successful
        row_inserted = len(data)
        log_audit("customer_churn", row_inserted, "Success")
        cur.close()
        conn.close()
    except Exception as e:
        if conn:
            conn.rollback()
        print("Error inserting data,rolled back:", e)
        #log failed
        log_audit("customer_churn", 0, "Failed")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
if __name__ == "__main__":
    create_audit_table()
    table_creation()
    add_constraints()
    insert_from_csv("Telco.csv")
