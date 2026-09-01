"""
ETL Data Transformation & Cleaning Engine
Author: Sanjay (Team Lead)
Description: Cleans, casts data types, and enriches raw ingested records.
"""
import logging

def transform_raw_data(raw_records):
    """
    Cleans raw CSV records, handles missing fields, and adds calculated metrics.
    """
    if not raw_records:
        logging.warning("No raw records provided for transformation.")
        return []

    cleaned_records = []
    
    for row in raw_records:
        try:
            # 1. Clean and cast data types
            order_id = int(row["order_id"])
            customer_name = row["customer_name"].strip()
            product = row["product"].strip()
            quantity = int(row["quantity"])
            unit_price = float(row["unit_price"])
            order_date = row["order_date"].strip()
            
            # 2. Derived field (Feature Engineering)
            total_amount = quantity * unit_price

            cleaned_record = {
                "order_id": order_id,
                "customer_name": customer_name,
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount,
                "order_date": order_date
            }
            cleaned_records.append(cleaned_record)

        except Exception as e:
            logging.error(f"Error processing row {row.get('order_id')}: {e}")

    logging.info(f"Successfully transformed {len(cleaned_records)} records.")
    return cleaned_records