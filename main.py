"""
Main Pipeline Orchestrator
Author: Sanjay (Team Lead)
Description: Coordinates data ingestion, ETL transformation, database loading, quality checks, and analytical views.
"""
import logging
import sys
import config
from pathlib import Path
from scripts.ingest_data import ingest_raw_data
from scripts.transform import transform_raw_data
from scripts.load import load_to_sqlite
from scripts.validate import validate_staging_data
from scripts.create_views import create_analytical_views

# Configure dual logging (Console + Persistent File Log)
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format="%(asctime)s - [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(config.LOG_FILE)
    ]
)

def run_pipeline():
    logging.info("=== Starting Data Pipeline Execution ===")
    logging.info(f"Target Database: {config.DB_PATH}")
    
    # Step 1: Ingestion Boundary
    logging.info("[1/5] Ingesting raw dataset...")
    raw_data = ingest_raw_data(config.DATA_DIR)
    
    # Step 2: Transformation & Cleaning Boundary
    logging.info("[2/5] Running ETL cleaning routines...")
    transformed_data = transform_raw_data(raw_data)
    
    # Step 3: Database Storage Boundary
    logging.info("[3/5] Persisting data to SQL staging tables...")
    load_to_sqlite(transformed_data, config.DB_PATH)
    
    # Step 4: Quality & Dashboard Readiness
    logging.info("[4/5] Running data quality validations...")
    validation_passed = validate_staging_data(config.DB_PATH)
    
    # Step 5: Analytical SQL Views Boundary
    if validation_passed:
        logging.info("[5/5] Building analytical SQL views...")
        sql_file = Path("SQL/views.sql")
        create_analytical_views(config.DB_PATH, sql_file)
        logging.info("=== Pipeline Execution Finished Successfully ===")
    else:
        logging.error("=== Pipeline Execution Finished with Validation Errors ===")

if __name__ == "__main__":
    run_pipeline()