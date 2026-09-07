import pandas as pd
import psycopg2
def connect_to_postgres():
    
    try:
        conn=psycopg2.connect(
            dbname="prg",
            user="postgres",
            password="Harsha@1131",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        return conn,cur
    except Exception as e:
        print("error connection:",e)
        return None,None

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
            MultipleLines VARCHAR(20),
            InternetService VARCHAR(20),
            OnlineSecurity VARCHAR(20),
            OnlineBackup VARCHAR(20),
            DeviceProtection VARCHAR(20),
            TechSupport VARCHAR(20),
            StreamingTV VARCHAR(20),
            StreamingMovies VARCHAR(20),
            Contract VARCHAR(20),
            PaperlessBilling VARCHAR(10),
            PaymentMethod VARCHAR(50),
            MonthlyCharges FLOAT,
            TotalCharges VARCHAR(20),
            Churn VARCHAR(10)
        );
        """
    conn, cur = connect_to_postgres()
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
table_creation()  
def insert_from_csv(csv_file):
    df=pd.read_csv(r"C:\Users\harsh\Downloads\archive\telco.csv")
    df=df.where(pd.notnull(df), None)

    insert_query="""
    INSERT INTO customer_churn(
    customerID,gender,SeniorCitizen,Partner,Dependents,
    tenure,PhoneService,MultipleLines,InternetService,
    OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,
    StreamingTV,StreamingMovies,Contract,PaperlessBilling,
    PaymentMethod,MonthlyCharges,TotalCharges,Churn)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    conn,cur=connect_to_postgres()
    try:
        data= [tuple(x) for x in df.to_numpy()]
        cur.executemany(insert_query,data)
        conn.commit()
        print("Data inserted successfully")
    except Exception as e:
        print("Error inserting data:",e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()
if __name__=="__main__":
    table_creation()
    insert_from_csv(r"C:\Users\harsh\Downloads\archive\telco.csv")

    



