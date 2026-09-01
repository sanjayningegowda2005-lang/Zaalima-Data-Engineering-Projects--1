-- Query 1: Overall Churn & Status Breakdown
SELECT 
    customer_status,
    COUNT(customer_id) AS total_customers,
    ROUND(COUNT(customer_id) * 100.0 / (SELECT COUNT(*) FROM stg_customer_churn), 2) AS percentage
FROM stg_customer_churn
GROUP BY customer_status;

-- Query 2: Churn Rate by Contract Type
SELECT 
    contract,
    COUNT(customer_id) AS total_customers,
    SUM(CASE WHEN customer_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN customer_status = 'Churned' THEN 1 ELSE 0 END) * 100.0 / COUNT(customer_id), 2) AS churn_rate_pct
FROM stg_customer_churn
GROUP BY contract;

-- Query 3: Top 5 Reasons for Churn & Lost Revenue
SELECT 
    churn_reason,
    COUNT(customer_id) AS churned_count,
    ROUND(SUM(total_charges), 2) AS total_revenue_lost
FROM stg_customer_churn
WHERE customer_status = 'Churned'
GROUP BY churn_reason
ORDER BY churned_count DESC
LIMIT 5;