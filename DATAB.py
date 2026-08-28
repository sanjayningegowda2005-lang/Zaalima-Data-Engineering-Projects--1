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

#connection function for psycopg2
def get_connection():
    """return a psycopg2 connection using env variables"""
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

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
    #removed man_close and called get_connection():
    try:
       with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(create_table_query)
            conn.commit()
            print("Table created successfully")
    except Exception as e:
        print("Error creating table:", e)


#api response staging table
def create_api_res_tab():
    create_table_query="""
    CREATE TABLE IF NOT EXISTS api_response_staging(
    id SERIAL PRIMARY KEY,
    source VARCHAR(100),
    response_json JSONB,
    status_code INT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE);
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                print("Table created API response staging")
    except Exception as e:
            print("Error creating API response staging table:", e)


#dynamic table creation based on pandas dtypes
def create_table_from_df(df,table_name="customer_churn"):
    dtype_map={
        "int64": "INTEGER",
        "float64": "FLOAT",
        "object": "VARCHAR(255)",
        "dattime64[ns]": "TIMESTAMP"
    }
    columns=[]
    for col,dtype in df.dtypes.items():
        sql_type=dtype_map.get(str(dtype),"VARCHAR(255)")
        if col=="customerID":
            columns.append(f"{col} {sql_type} PRIMARY KEY")
        else:
            columns.append(f"{col} {sql_type}")
    create_table_query=f"""CREATE TABLE IF NOT EXISTS {table_name}(
    {", ".join(columns)});"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(create_table_query)
                conn.commit()
                print("Table created API response staging")
    except Exception as e:
        print("Error creating API response staging table:", e)


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
        ON CONFLICT (customerID) DO UPDATE SET
            gender=EXCLUDED.gender,
            SeniorCitizen=EXCLUDED.SeniorCitizen,
            partner=EXCLUDED.Partner,
            Dependents=EXClUDED.Dependents,
            tenure=EXCLUDED.tenure,
            PhoneService=EXCLUDED.PhoneService,
            MultipleLines=EXCLUDED.MultipleLines,
            InternetService=EXCLUDED.InternetService,
            OnlineSecurity=EXCLUDED.OnlineSecurity,
            OnlineBackup=EXCLUDED.OnlineBackup,
            DeviceProtection=EXCLUDED.DeviceProtection,
            TechSupport=EXCLUDED.TechSupport,
            StreamingTV=EXCLUDED.StreamingTV,
            StreamingMovies=EXCLUDED.StreamingMovies,
            Contract=EXCLUDED.Contract,
            PaperlessBilling=EXCLUDED.PaperlessBilling,
            PaymentMethod=EXCLUDED.PaymentMethod,
            MonthlyCharges=EXCLUDED.MonthlyCharges,
            TotalCharges=EXCLUDED.TotalCharges,
            Churn=EXCLUDED.Churn;
    """
    data=[tuple(x) for _, x in df.iterrows()]
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.executemany(insert_query,data)
                conn.commit()
                print("data inserted successfully")
                log_audit("customer_churn",len(data),"success")
    except Exception as e:
        print("Error inserting data,rolled back:", e)
        log_audit("customer_churn", 0, "Failed")
    finally:
        pass
    
if __name__ == "__main__":
    create_audit_table()
    df=pd.read_csv("Telco.csv")
    create_table_from_df(df,"customer_churn")
    table_creation()
    create_api_res_tab()
    add_constraints()
    insert_from_csv("Telco.csv")
