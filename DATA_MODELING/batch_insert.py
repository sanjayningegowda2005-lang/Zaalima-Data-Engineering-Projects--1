import time
import pandas as pd
from sqlalchemy import URL, create_engine, text
from dotenv import load_dotenv
import os
import pathlib
#load env variable
env_path=pathlib.Path(__file__).resolve().parent/".env"
load_dotenv(dotenv_path=env_path, override=True)

def get_postgre_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    connection_url = URL.create(
        "postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=int(port),
        database=db_name,
    )
    return create_engine(connection_url)

def optimize_batch(csv_file="Telco.csv", table_name="customer_churn", chunksizes=None):
    if chunksizes is None:
        chunksizes = [500, 1000, 2000, 5000]

    csv_path = pathlib.Path(csv_file)
    if not csv_path.is_absolute() and not csv_path.exists():
        csv_path = pathlib.Path(__file__).resolve().parent / csv_path
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    df = pd.read_csv(csv_path, encoding="utf-8-sig")
    df.columns = (
        df.columns.astype(str)
        .str.replace("\ufeff", "", regex=False)
        .str.replace("ï»¿", "", regex=False)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    if "customerid" not in df.columns:
        raise ValueError(f"CSV is missing required customerID column: {list(df.columns)}")
    conflict_markers = df["customerid"].astype(str).str.match(r"^(<<<<<<<|=======|>>>>>>>)")
    if conflict_markers.any():
        raise ValueError("CSV contains unresolved Git conflict markers")
    df = df[df["customerid"].astype(str).str.strip().str.lower() != "customerid"]
    df = df.replace(r"^\s*$", pd.NA, regex=True)
    for column in ("seniorcitizen", "tenure", "monthlycharges", "totalcharges"):
        df[column] = pd.to_numeric(df[column], errors="coerce")
    engine = get_postgre_engine()
    staging_table = "_customer_churn_batch_staging"
    columns = list(df.columns)
    quoted_columns = ", ".join(f'"{column}"' for column in columns)
    select_expressions = {
        "seniorcitizen": '"seniorcitizen"::integer',
        "tenure": '"tenure"::integer',
        "monthlycharges": '"monthlycharges"::double precision',
        "totalcharges": '"totalcharges"::text',
    }
    select_columns = ", ".join(
        select_expressions.get(column, f'"{column}"') for column in columns
    )
    for size in chunksizes:
        start=time.time()
        df.to_sql(staging_table, engine, if_exists="replace", index=False, chunksize=size)
        with engine.begin() as connection:
            connection.execute(text(
                f'INSERT INTO "{table_name}" ({quoted_columns}) '
                f'SELECT {select_columns} FROM "{staging_table}" '
                "ON CONFLICT DO NOTHING"
            ))
            connection.execute(text(f'DROP TABLE "{staging_table}"'))
        end = time.time()
        print(f"Chunksize={size}: Inserted {len(df)} rows in {end - start:.2f} seconds")
if __name__=="__main__":
    optimize_batch("Telco.csv", "customer_churn", chunksizes=[500, 1000, 2000, 5000])

