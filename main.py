import logging
from scripts.ingest import ingest_data
from scripts.transform import transform_data
from scripts.load import load_to_sqlite
from scripts.validate import validate_staging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_pipeline():
    logging.info("=== Starting Data Pipeline Execution ===")
    
    # Step 1: Ingestion
    raw_df = ingest_data()
    
    # Step 2: Transformation
    cleaned_df = transform_data(raw_df)
    
    # Step 3: Database Storage Boundary
    load_to_sqlite(cleaned_df)
    
    # Step 4: Quality & Dashboard Readiness Validation
    validate_staging()
    
    logging.info("=== Pipeline Execution Finished Successfully ===")

if __name__ == "__main__":
    run_pipeline()