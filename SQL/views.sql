-- Indexes for query optimization
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON staging_orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_order_date ON staging_orders(order_date);

-- Analytical Views
CREATE VIEW IF NOT EXISTS view_product_revenue AS
SELECT 
    product_name,
    SUM(quantity * unit_price) AS total_revenue,
    SUM(quantity) AS total_quantity_sold
FROM staging_orders
GROUP BY product_name;

CREATE VIEW IF NOT EXISTS view_customer_summary AS
SELECT 
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(quantity * unit_price) AS total_spend
FROM staging_orders
GROUP BY customer_id;