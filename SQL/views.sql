-- Analytical View 1: Revenue & Units Sold by Product
CREATE VIEW IF NOT EXISTS view_product_revenue AS
SELECT 
    product,
    SUM(quantity) AS total_units_sold,
    SUM(total_amount) AS total_revenue,
    ROUND(AVG(unit_price), 2) AS avg_unit_price
FROM staging_orders
GROUP BY product;

-- Analytical View 2: Customer Spend & Order Summary
CREATE VIEW IF NOT EXISTS view_customer_summary AS
SELECT 
    customer_name,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_spent
FROM staging_orders
GROUP BY customer_name;