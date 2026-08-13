"""
Centralized Pipeline Configuration
Author: Sanjay (Team Lead)
Description: Stores global file paths, database parameters, and system constants.
"""
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# File & Storage Directories
DATA_DIR = BASE_DIR / "Data"
SCRIPTS_DIR = BASE_DIR / "scripts"
SQL_DIR = BASE_DIR / "SQL"

# Database Configuration
DB_NAME = "pipeline_staging.db"
DB_PATH = BASE_DIR / DB_NAME
DB_CONNECTION_STRING = f"sqlite:///{DB_PATH}"

# System Logging Settings
LOG_FILE = BASE_DIR / "pipeline_execution.log"
LOG_LEVEL = "INFO"