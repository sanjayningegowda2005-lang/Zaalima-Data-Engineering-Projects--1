import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def generate_features(db_path="telecom_staging.db"):
    conn = sqlite3.connect(db_path)
    
    logging.info("Reading data from SQL views...")
    df = pd.read_sql_query("SELECT * FROM v_customer_tenure_segments", conn)
    
    # 1. Feature: Monthly spend ratio relative to tenure
    df['monthly_spend_ratio'] = df['monthly_charge'] / (df['tenure_in_months'] + 1)
    
    # 2. Feature: High-risk customer flag (New customer paying high rate)
    df['is_high_risk'] = ((df['tenure_in_months'] <= 12) & (df['monthly_charge'] > 70.0)).astype(int)
    
    # Save transformed features into staging database
    df.to_sql("stg_customer_features", conn, if_exists="replace", index=False)
    conn.close()
    
    logging.info(f"Successfully generated features for {len(df)} records in 'stg_customer_features'.")

if __name__ == "__main__":
    generate_features()