import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
def add_constraints():
    # alter_table_query = """
    # ALTER TABLE customer_churn
    # ALTER COLUMN gender SET NOT NULL,
    # ALTER COLUMN SeniorCitizen SET NOT NULL,
    # ALTER COLUMN tenure SET NOT NULL,
    # ALTER COLUMN InternetService SET NOT NULL,
    # ALTER COLUMN Contract SET NOT NULL,
    # ALTER COLUMN MonthlyCharges SET NOT NULL,
    # ALTER COLUMN churn SET NOT NULL,
    # """
    try:
        conn=psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASS"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur=conn.cursor()

        # Make sure SeniorCitizen is always provided
        cur.execute("""
            ALTER TABLE customer_churn
            ALTER COLUMN SeniorCitizen SET NOT NULL;
        """)
        # Gender must be Male or Female
        cur.execute("ALTER TABLE customer_churn DROP CONSTRAINT IF EXISTS chk_gender;")
        cur.execute("""
            ALTER TABLE customer_churn
            ADD CONSTRAINT chk_gender CHECK (gender IN ('Male','Female'));
        """)

        # Churn must be Yes or No
        cur.execute("ALTER TABLE customer_churn DROP CONSTRAINT IF EXISTS chk_churn;")
        cur.execute("""
            ALTER TABLE customer_churn
            ADD CONSTRAINT chk_churn CHECK (Churn IN ('Yes','No'));
        """)

        # MonthlyCharges must be non-negative
        cur.execute("ALTER TABLE customer_churn DROP CONSTRAINT IF EXISTS chk_monthlycharges;")
        cur.execute("""
            ALTER TABLE customer_churn
            ADD CONSTRAINT chk_monthlycharges CHECK (MonthlyCharges::float >= 0);
        """)

        # TotalCharges must be non-negative
        cur.execute("ALTER TABLE customer_churn DROP CONSTRAINT IF EXISTS chk_totalcharges;")
        cur.execute("""
            ALTER TABLE customer_churn
            ADD CONSTRAINT chk_totalcharges CHECK (TotalCharges::float >= 0);
        """)

        # CustomerID must be unique
        cur.execute("ALTER TABLE customer_churn DROP CONSTRAINT IF EXISTS unique_customer;")
        cur.execute("""
            ALTER TABLE customer_churn
            ADD CONSTRAINT unique_customer UNIQUE (customerID);
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Constraints added successfully.")
    except Exception as e:
        print("Error adding constraints:", e)

