-- Total revenue
SELECT SUM(amount) AS total_revenue FROM sales;

-- Sales by product
SELECT p.name, SUM(s.amount) as total_sales
FROM sales s
JOIN products p ON s.product_id = p.id
GROUP BY p.name
ORDER BY total_sales DESC;

-- Sales by region
SELECT st.region, SUM(s.amount) as total_sales
FROM sales s
JOIN stores st ON s.store_id = st.id
GROUP BY st.region
ORDER BY total_sales DESC;