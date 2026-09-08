import time
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import pathlib
#load env variable
env_path=pathlib.Path(__file__).resolve().parent/".env"
load_dotenv(dotenv_path=env_path)

def get_postgre_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    con_str = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    engine = create_engine(con_str)
    return engine

def optimize_batch(csv_file="Telco.csv", table_name="customer_churn", chunksizes=None):
    if chunksizes is None:
        chunksizes = [500, 1000, 2000, 5000]

    csv_path = pathlib.Path(csv_file)
    if not csv_path.is_absolute() and not csv_path.exists():
        csv_path = pathlib.Path(__file__).resolve().parent / csv_path
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    engine = get_postgre_engine()
    for size in chunksizes:
        start=time.time()
        df.to_sql(
            table_name,
            engine,
            if_exists="append",
            index=False,
            chunksize=size
        )
        end = time.time()
        print(f"Chunksize={size}: Inserted {len(df)} rows in {end - start:.2f} seconds")
if __name__=="__main__":
    optimize_batch("Telco.csv", "customer_churn", chunksizes=[500, 1000, 2000, 5000])

