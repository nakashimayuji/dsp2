SELECT customers.customer_name, SUM(products.price * orders.quantity) AS total_purchase
FROM orders
JOIN products ON orders.product_id = products.product_id
JOIN customers ON orders.customer_id = customers.customer_id
WHERE orders.order_date BETWEEN '2025-01-01' AND '2025-06-30'
GROUP BY customers.customer_name
ORDER BY total_purchase DESC
LIMIT 3;