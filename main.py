import logging
from scripts.ingest import ingest_data
from scripts.transform import transform_data
from scripts.load import load_to_sqlite
from scripts.validate import validate_staging
from scripts.create_views import build_views
from scripts.features import generate_features

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("pipeline_execution.log"),
        logging.StreamHandler()
    ]
)

def run_full_pipeline():
    logging.info("=== Starting Data Engineering Pipeline ===")
    
    # 1. ETL Phase
    raw_df = ingest_data()
    cleaned_df = transform_data(raw_df)
    load_to_sqlite(cleaned_df)
    validate_staging()
    
    # 2. Analytics & Feature Layer
    build_views()
    generate_features()
    
    logging.info("=== Pipeline Execution Finished Successfully ===")

if __name__ == "__main__":
    run_full_pipeline()