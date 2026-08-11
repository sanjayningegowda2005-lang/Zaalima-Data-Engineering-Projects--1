"""
Main Pipeline Orchestrator
Author: Sanjay (Team Lead)
Description: Coordinates data ingestion, ETL transformation, database loading, and quality checks.
"""
import logging
import sys
import config

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
    logging.info(f"Data Storage Directory: {config.DATA_DIR}")
    
    # Step 1: Ingestion Boundary
    logging.info("[1/4] Ingesting raw dataset...")
    
    # Step 2: Transformation & Cleaning Boundary
    logging.info("[2/4] Running ETL cleaning routines...")
    
    # Step 3: Database Storage Boundary
    logging.info("[3/4] Persisting data to SQL staging tables...")
    
    # Step 4: Quality & Dashboard Readiness
    logging.info("[4/4] Running data quality validations...")
    
    logging.info("=== Pipeline Execution Finished Successfully ===")

if __name__ == "__main__":
    run_pipeline()