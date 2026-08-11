-- View 1: Customer Tenure Binning
CREATE VIEW IF NOT EXISTS v_customer_tenure_segments AS
SELECT 
    customer_id,
    gender,
    contract,
    tenure_in_months,
    CASE 
        WHEN tenure_in_months <= 12 THEN '0-1 Years'
        WHEN tenure_in_months <= 24 THEN '1-2 Years'
        ELSE '2+ Years'
    END AS tenure_group,
    monthly_charge,
    customer_status
FROM stg_customer_churn;

-- View 2: High-Value Churned Customers
CREATE VIEW IF NOT EXISTS v_high_value_churn AS
SELECT 
    customer_id,
    contract,
    monthly_charge,
    total_charges,
    churn_reason
FROM stg_customer_churn
WHERE customer_status = 'Churned' 
  AND monthly_charge > 70.0;