import pandas as pd
from sqlalchemy import create_engine
import psycopg2
#postgreSQL connection
def get_sqlite_engine(db_path="DATAB"):
    engine = create_engine("sqlite:///%s" % db_path)
    return engine
def get_postgre_engine(user="postgres",password="Harsha%401131",host="localhost",port=5432,db_name="prg"):
    con_str="postgresql://%s:%s@%s:%s/%s" % (user,password,host,port,db_name)
    engine = create_engine(con_str)
    return engine
#test database connection
def test_connection(engine):
    try:
        with engine.connect() as conn:
            print("Connection successful")
    except Exception as e:
        print("Connection failed:", e)
#CREATION OF TABLE
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
        conn=psycopg2.connect(
            dbname="prg",
            user="postgres",
            password="Harsha@1131",
            host="localhost",
            port="5432"
        )
        cur=conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        cur.close()
        conn.close()
        print("Table created successfully")
    except Exception as e:
        print("Error creating table:", e)
#INDEX CREATION
def create_indexes():
    index_query = [
        "CREATE INDEX IF NOT EXISTS idx_customer_churn_customerID ON customer_churn (customerID);",
        "CREATE INDEX IF NOT EXISTS idx_customer_churn_contract ON customer_churn (Contract);",
        "CREATE INDEX IF NOT EXISTS idx_customer_churn_paymentmethod ON customer_churn (PaymentMethod);",
        "CREATE INDEX IF NOT EXISTS idx_customer_churn_churn ON customer_churn (Churn);"
    ]
    try:
        with psycopg2.connect(
            dbname="prg",
            user="postgres",
            password="Harsha@1131",
            host="localhost",
            port="5432"
        ) as conn:
            with conn.cursor() as cur:
                for query in index_query:
                    cur.execute(query)
                conn.commit()
                print("Indexes created successfully")
    except Exception as e:
        print("Error creating indexes:", e)

#insert exection logic
def insert_from_csv(csv_file):
      df=pd.read_csv(r"C:\Users\harsh\Downloads\archive\telco.csv")
      df=df.where(pd.notnull(df), None)
      insert_query = """
        INSERT INTO customer_churn (customerID, gender, SeniorCitizen,
        Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService,
        OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV,
        StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges,
        TotalCharges, Churn)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (customerID) DO NOTHING;
    """
      try:
          conn=psycopg2.connect(
              dbname="prg",
              user="postgres",
              password="Harsha@1131",
              host="localhost",
              port="5432"
          )
          cur=conn.cursor()
          data=[tuple(x) for index, x in df.iterrows()]
          cur.executemany(insert_query,data)
          conn.commit()
          print("Data inserted successfully")
          cur.close()
          conn.close()
      except Exception as e:
            print("Error inserting data:", e)
#execute table creation,verify DataBase
if __name__ == "__main__":
    sql_engine=get_sqlite_engine("mydb.sqlite")
    print("sql engine created:", sql_engine)
    test_connection(sql_engine)
    postgre_engine=get_postgre_engine()
    print("postgreSQL engine created:",postgre_engine)
    test_connection(postgre_engine)
    table_creation()
    create_indexes()
    insert_from_csv(r"C:\Users\harsh\Downloads\archive\telco.csv")




