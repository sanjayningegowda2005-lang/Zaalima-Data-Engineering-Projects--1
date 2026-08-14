import os
import pandas as pd
from sqlalchemy import create_engine


def get_database_connection():
    """Create and return a database connection."""
    
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        return None

    return create_engine(database_url)


def fetch_data(query):
    """Execute a SQL query and return the result as a DataFrame."""
    
    engine = get_database_connection()

    if engine is None:
        return pd.DataFrame()

    return pd.read_sql(query, engine)