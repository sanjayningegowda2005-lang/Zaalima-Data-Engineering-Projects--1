import pandas as pd
import psycopg2
def connect_to_postgres():
    
    try:
        conn=psycopg2.connect(
            dbname="project",
            user="postgres",
            password="c##cse",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        return conn,cur
    except:
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
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()
table_creation()  
    
dataframe=pd.read_csv(r"C:\Users\abhik\Desktop\DATA\telco_churn.csv")
print(dataframe.info())


