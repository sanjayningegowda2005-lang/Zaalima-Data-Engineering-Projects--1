import unittest
import os
import psycopg2
from dotenv import load_dotenv
import pathlib
#load env variable
env_path=pathlib.Path(__file__).resolve().parent/".env"
load_dotenv(dotenv_path=env_path)
def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
class TestDb(unittest.TestCase):
    def test_con_established(self):
        try:
            conn=get_connection()
            self.assertIsNotNone(conn)
            conn.close()
        except Exception as e:
            self.fail(f"Database connection failed: {e}")
    def test_customer_churn_table_exists(self):
        try:
            conn=get_connection()
            cursor=conn.cursor()
            cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='customer_churn');")
            exists=cursor.fetchone()[0]
            self.assertTrue(exists,"table does not exist")
            cursor.close()
            conn.close()
        except Exception as e:
            self.fail(f"Database query failed: {e}")
def test_drop_iftable_exists():
    try:
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute("Drop table if not exists customer_churn(customerID VARCHAR(50) PRIMARY KEY);")
        conn.commit()
        cursor.execute("DROP TABLE IF EXISTS customer_churn;")
        conn.commit()
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='customer_churn');")
        exists=cursor.fetchone()[0]
        self.assertFalse(exists,"table still exists")
        cursor.close()
        conn.close()
    except Exception as e:
        raise AssertionError(f"Failed to drop table: {e}")

if __name__=="__main__":
    unittest.main()
