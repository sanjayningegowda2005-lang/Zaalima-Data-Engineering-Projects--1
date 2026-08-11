import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    logging.info("Starting data transformation...")
    
    # 1. Standardize column names (lowercase, replace spaces/special chars with underscores)
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_')
        .str.replace('[^a-zA-Z0-9_]', '', regex=True)
    )
    
    # 2. Handle missing values in categorical fields
    if 'churn_reason' in df.columns:
        df['churn_reason'] = df['churn_reason'].fillna('Not Churned')
        
    # 3. Strip whitespace from string columns
    str_cols = df.select_dtypes(include=['object']).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    logging.info(f"Transformation complete. Columns standardized: {list(df.columns[:5])}...")
    return df

if __name__ == "__main__":
    from ingest import ingest_data
    
    raw_df = ingest_data()
    cleaned_df = transform_data(raw_df)
    print(cleaned_df[['customer_id', 'churn_reason']].head())