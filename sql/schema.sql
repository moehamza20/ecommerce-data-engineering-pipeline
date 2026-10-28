
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id INT UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    country VARCHAR(60),
    signup_date DATE
);

CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id INT UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    category VARCHAR(80),
    price NUMERIC(10, 2),
    stock INT
);

CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    quarter INT NOT NULL,
    day INT NOT NULL
);

CREATE TABLE dim_payment (
    payment_key SERIAL PRIMARY KEY,
    payment_id INT UNIQUE NOT NULL,
    order_id INT NOT NULL,
    payment_method VARCHAR(30),
    payment_status VARCHAR(30),
    amount NUMERIC(10, 2),
    payment_date DATE
);

CREATE TABLE fact_sales (
    sales_key BIGSERIAL PRIMARY KEY,
    order_item_id INT UNIQUE NOT NULL,
    order_id INT NOT NULL,
    customer_key INT NOT NULL REFERENCES dim_customer(customer_key),
    product_key INT NOT NULL REFERENCES dim_product(product_key),
    date_key INT NOT NULL REFERENCES dim_date(date_key),
    payment_key INT REFERENCES dim_payment(payment_key),
    quantity INT NOT NULL,
    unit_price NUMERIC(10, 2) NOT NULL,
    total_amount NUMERIC(12, 2) NOT NULL,
    order_status VARCHAR(30) NOT NULL
);

CREATE INDEX idx_fact_sales_order
    ON fact_sales(order_id);

CREATE INDEX idx_fact_sales_date
    ON fact_sales(date_key);

CREATE INDEX idx_fact_sales_customer
    ON fact_sales(customer_key);

CREATE INDEX idx_fact_sales_product
    ON fact_sales(product_key);
