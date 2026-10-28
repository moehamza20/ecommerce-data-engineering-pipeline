
-- Sample data for ecommerce_source
-- Run after source_schema.sql on a fresh database.
-- Expected counts: 12 customers, 8 products, 20 orders,
-- 25 order_items, and 20 payments.

INSERT INTO customers (customer_id, name, email, country, signup_date) VALUES
(1, 'Ahmed Hassan', 'ahmed@example.com', 'Egypt', '2025-01-10'),
(2, 'Mona Ali', 'mona@example.com', 'Egypt', '2025-01-15'),
(3, 'Omar Khaled', 'omar@example.com', 'Saudi Arabia', '2025-02-01'),
(4, 'Sara Mohamed', 'sara@example.com', 'UAE', '2025-02-10'),
(5, 'Youssef Adel', 'youssef@example.com', 'Egypt', '2025-02-18'),
(6, 'Nour Samir', 'nour@example.com', 'Jordan', '2025-03-02'),
(7, 'Karim Mostafa', 'karim@example.com', 'Egypt', '2025-03-11'),
(8, 'Farah Tarek', 'farah@example.com', 'UAE', '2025-03-20'),
(9, 'Hana Ibrahim', 'hana@example.com', 'Saudi Arabia', '2025-04-05'),
(10, 'Ali Mahmoud', 'ali@example.com', 'Egypt', '2025-04-12'),
(11, 'Laila Ashraf', 'laila@example.com', 'Jordan', '2025-05-01'),
(12, 'Ziad Amr', 'ziad@example.com', 'Egypt', '2025-05-09');

INSERT INTO products (product_id, name, category, price, stock) VALUES
(1, 'Wireless Mouse', 'Electronics', 25.00, 50),
(2, 'Mechanical Keyboard', 'Electronics', 40.00, 35),
(3, 'Notebook', 'Stationery', 15.00, 100),
(4, 'Office Chair', 'Furniture', 100.00, 12),
(5, 'Desk Lamp', 'Home', 60.00, 20),
(6, 'Headphones', 'Electronics', 80.00, 25),
(7, 'Water Bottle', 'Accessories', 30.00, 60),
(8, 'Monitor', 'Electronics', 120.00, 10);

INSERT INTO orders (order_id, customer_id, order_date, status) VALUES
(1, 1, '2025-06-01', 'Completed'),
(2, 2, '2025-06-02', 'Completed'),
(3, 3, '2025-06-03', 'Completed'),
(4, 4, '2025-06-04', 'Completed'),
(5, 5, '2025-06-05', 'Completed'),
(6, 6, '2025-06-06', 'Completed'),
(7, 7, '2025-06-07', 'Completed'),
(8, 8, '2025-06-08', 'Completed'),
(9, 9, '2025-06-09', 'Completed'),
(10, 10, '2025-06-10', 'Completed'),
(11, 11, '2025-06-11', 'Completed'),
(12, 12, '2025-06-12', 'Completed'),
(13, 1, '2025-06-13', 'Completed'),
(14, 2, '2025-06-14', 'Completed'),
(15, 3, '2025-06-15', 'Completed'),
(16, 4, '2025-06-16', 'Completed'),
(17, 5, '2025-06-17', 'Completed'),
(18, 6, '2025-06-18', 'Pending'),
(19, 7, '2025-06-19', 'Pending'),
(20, 8, '2025-06-20', 'Cancelled');

INSERT INTO order_items (order_item_id, order_id, product_id, quantity) VALUES
(1, 1, 1, 2),
(2, 1, 3, 1),
(3, 2, 2, 1),
(4, 2, 6, 1),
(5, 3, 4, 1),
(6, 3, 1, 1),
(7, 4, 5, 2),
(8, 4, 3, 2),
(9, 5, 8, 1),
(10, 5, 7, 1),
(11, 6, 1, 1),
(12, 7, 2, 2),
(13, 8, 3, 3),
(14, 9, 4, 1),
(15, 10, 5, 1),
(16, 11, 6, 1),
(17, 12, 7, 2),
(18, 13, 8, 1),
(19, 14, 1, 3),
(20, 15, 2, 1),
(21, 16, 3, 1),
(22, 17, 4, 2),
(23, 18, 5, 1),
(24, 19, 6, 2),
(25, 20, 7, 1);

INSERT INTO payments
(payment_id, order_id, payment_method, amount, payment_date, status) VALUES
(1, 1, 'Card', 65.00, '2025-06-01', 'Completed'),
(2, 2, 'Wallet', 120.00, '2025-06-02', 'Completed'),
(3, 3, 'Card', 125.00, '2025-06-03', 'Completed'),
(4, 4, 'Cash', 150.00, '2025-06-04', 'Completed'),
(5, 5, 'Card', 150.00, '2025-06-05', 'Completed'),
(6, 6, 'Wallet', 25.00, '2025-06-06', 'Completed'),
(7, 7, 'Card', 80.00, '2025-06-07', 'Completed'),
(8, 8, 'Cash', 45.00, '2025-06-08', 'Completed'),
(9, 9, 'Card', 100.00, '2025-06-09', 'Completed'),
(10, 10, 'Wallet', 60.00, '2025-06-10', 'Completed'),
(11, 11, 'Card', 80.00, '2025-06-11', 'Completed'),
(12, 12, 'Cash', 60.00, '2025-06-12', 'Completed'),
(13, 13, 'Card', 120.00, '2025-06-13', 'Completed'),
(14, 14, 'Wallet', 75.00, '2025-06-14', 'Completed'),
(15, 15, 'Card', 40.00, '2025-06-15', 'Completed'),
(16, 16, 'Cash', 15.00, '2025-06-16', 'Completed'),
(17, 17, 'Card', 200.00, '2025-06-17', 'Completed'),
(18, 18, 'Wallet', 60.00, '2025-06-18', 'Pending'),
(19, 19, 'Card', 160.00, '2025-06-19', 'Pending'),
(20, 20, 'Cash', 30.00, '2025-06-20', 'Cancelled');

-- Keep SERIAL sequences ready for future inserts after explicit IDs.
SELECT setval(pg_get_serial_sequence('customers', 'customer_id'), (SELECT MAX(customer_id) FROM customers));
SELECT setval(pg_get_serial_sequence('products', 'product_id'), (SELECT MAX(product_id) FROM products));
SELECT setval(pg_get_serial_sequence('orders', 'order_id'), (SELECT MAX(order_id) FROM orders));
SELECT setval(pg_get_serial_sequence('order_items', 'order_item_id'), (SELECT MAX(order_item_id) FROM order_items));
SELECT setval(pg_get_serial_sequence('payments', 'payment_id'), (SELECT MAX(payment_id) FROM payments));
