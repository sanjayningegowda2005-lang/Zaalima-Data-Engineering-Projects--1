from audit_log import create_audit_table
from DATAB import table_creation, create_api_res_tab, insert_from_csv, insert_mock
from ingest_data import load_schema, push_to_database, load_incremental, fetch_api_data, clean_dataframe, benchmark_ingestion, get_connection
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

if __name__ == "__main__":
    # Setup
    create_audit_table()
    table_creation()
    create_api_res_tab()

    # Schema validation + ingestion
    schema = load_schema()
    push_to_database(BASE_DIR / "Telco.csv", schema)

    # Incremental loading
    conn = get_connection()
    new_records = load_incremental(BASE_DIR / "mock_data.csv", conn, "customer_churn")
    if not new_records.empty:
        insert_mock(df=new_records)
    conn.close()

    # API ingestion
    api_df = fetch_api_data("https://jsonplaceholder.typicode.com/posts")
    api_df = clean_dataframe(api_df)
    print(f"API ingestion fetched {len(api_df)} records")

    # Benchmark
    benchmark_ingestion(BASE_DIR / "Telco.csv")
