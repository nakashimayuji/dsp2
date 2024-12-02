SELECT SUM(products.price * orders.quantity) AS total_sales
FROM orders
JOIN products ON orders.product_id = products.product_id
JOIN customers ON orders.customer_id = customers.customer_id
WHERE customers.gender = 'Female'
  AND customers.age >= 20
  AND orders.order_date BETWEEN '2024-01-01' AND '2024-03-31';