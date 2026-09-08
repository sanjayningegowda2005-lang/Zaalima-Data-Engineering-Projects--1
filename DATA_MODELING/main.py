import pathlib
from .DATAB import table_creation
from .ingest_data import load_schema, push_to_database
BASE_DIR = pathlib.Path(__file__).resolve().parent

def run_pipeline():
    schema = load_schema(BASE_DIR / "schema.json")
    if schema is None:
        return
    table_creation()
    push_to_database(BASE_DIR / "Telco.csv", schema)
if __name__ == "__main__":
    run_pipeline()
