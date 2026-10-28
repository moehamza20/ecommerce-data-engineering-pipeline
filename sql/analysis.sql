
-- 1. Total revenue from completed orders
SELECT ROUND(SUM(total_amount), 2) AS total_revenue
FROM fact_sales
WHERE order_status = 'completed';


-- 2. Number of completed orders
SELECT COUNT(DISTINCT order_id) AS completed_orders
FROM fact_sales
WHERE order_status = 'completed';


-- 3. Average order value (AOV)
WITH order_totals AS (
    SELECT
        order_id,
        SUM(total_amount) AS order_total
    FROM fact_sales
    WHERE order_status = 'completed'
    GROUP BY order_id
)
SELECT ROUND(AVG(order_total), 2) AS average_order_value
FROM order_totals;


-- 4. Monthly revenue
SELECT
    d.year,
    d.month,
    ROUND(SUM(fs.total_amount), 2) AS monthly_revenue
FROM fact_sales fs
JOIN dim_date d
    ON fs.date_key = d.date_key
WHERE fs.order_status = 'completed'
GROUP BY d.year, d.month
ORDER BY d.year, d.month;


-- 5. Revenue by product category
SELECT
    p.category,
    ROUND(SUM(fs.total_amount), 2) AS category_revenue
FROM fact_sales fs
JOIN dim_product p
    ON fs.product_key = p.product_key
WHERE fs.order_status = 'completed'
GROUP BY p.category
ORDER BY category_revenue DESC;


-- 6. Top 5 products by completed-order revenue
SELECT
    p.name AS product_name,
    SUM(fs.quantity) AS units_sold,
    ROUND(SUM(fs.total_amount), 2) AS revenue
FROM fact_sales fs
JOIN dim_product p
    ON fs.product_key = p.product_key
WHERE fs.order_status = 'completed'
GROUP BY p.product_key, p.name
ORDER BY revenue DESC
LIMIT 5;


-- 7. Top 5 customers by completed-order spending
SELECT
    c.customer_id,
    c.name AS customer_name,
    ROUND(SUM(fs.total_amount), 2) AS total_spent
FROM fact_sales fs
JOIN dim_customer c
    ON fs.customer_key = c.customer_key
WHERE fs.order_status = 'completed'
GROUP BY c.customer_key, c.customer_id, c.name
ORDER BY total_spent DESC
LIMIT 5;


-- 8. Payment distribution by method and status
SELECT
    payment_method,
    payment_status,
    COUNT(*) AS payment_count,
    ROUND(SUM(amount), 2) AS total_payment_amount
FROM dim_payment
GROUP BY payment_method, payment_status
ORDER BY payment_count DESC;


-- 9. Products with low stock (5 or fewer units)
SELECT
    name AS product_name,
    category,
    stock
FROM dim_product
WHERE stock <= 5
ORDER BY stock ASC, name;


-- 10. Average customer rating for each product
SELECT
    p.product_id,
    p.name AS product_name,
    ROUND(AVG(r.rating), 2) AS average_rating,
    COUNT(r.rating) AS number_of_reviews
FROM dim_product p
LEFT JOIN fact_reviews r
    ON p.product_id = r.product_id
GROUP BY p.product_id, p.name
ORDER BY average_rating DESC NULLS LAST, number_of_reviews DESC;
