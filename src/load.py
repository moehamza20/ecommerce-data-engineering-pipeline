
import json
import pandas as pd
from psycopg2.extras import execute_values, Json

from src.database import get_warehouse_connection


def clean_value(value):
    """Convert Pandas values into PostgreSQL-compatible values."""

    if value is None:
        return None

    if isinstance(value, (dict, list)):
        return Json(value)

    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    if hasattr(value, "item"):
        value = value.item()

    if pd.isna(value):
        return None

    return value


def insert_rows(cursor, query, rows):
    """Insert rows efficiently when there is data to load."""

    if rows:
        execute_values(cursor, query, rows)


def load_warehouse(data):
    """Load transformed data into the PostgreSQL warehouse."""

    conn = get_warehouse_connection()

    try:
        with conn:
            with conn.cursor() as cur:

                # Supporting tables for MongoDB data.
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS fact_reviews (
                        review_key BIGSERIAL PRIMARY KEY,
                        customer_id INT,
                        product_id INT,
                        rating INT,
                        comment TEXT,
                        tags TEXT,
                        created_at TIMESTAMPTZ
                    );

                    CREATE TABLE IF NOT EXISTS fact_user_activity (
                        activity_key BIGSERIAL PRIMARY KEY,
                        customer_id INT,
                        session_id TEXT,
                        action_data JSONB,
                        device_data JSONB
                    );
                """)

                # Clear old data in dependency-safe order.
                cur.execute("""
                    TRUNCATE TABLE
                        fact_sales,
                        dim_payment,
                        dim_date,
                        dim_product,
                        dim_customer,
                        fact_reviews,
                        fact_user_activity
                    RESTART IDENTITY CASCADE;
                """)

                # 1. Load customer dimension.
                customers = data["customers"]

                rows = [
                    tuple(clean_value(row[col]) for col in [
                        "customer_id", "name", "email",
                        "country", "signup_date"
                    ])
                    for _, row in customers.iterrows()
                ]

                insert_rows(cur, """
                    INSERT INTO dim_customer
                    (customer_id, name, email, country, signup_date)
                    VALUES %s
                """, rows)

                # 2. Load product dimension.
                products = data["products"]

                rows = [
                    tuple(clean_value(row[col]) for col in [
                        "product_id", "name", "category", "price", "stock"
                    ])
                    for _, row in products.iterrows()
                ]

                insert_rows(cur, """
                    INSERT INTO dim_product
                    (product_id, name, category, price, stock)
                    VALUES %s
                """, rows)

                # 3. Build and load date dimension.
                sales = data["sales"]
                unique_dates = sales["order_date"].dropna().unique()

                rows = []
                for value in unique_dates:
                    date = pd.Timestamp(value).date()
                    rows.append((
                        int(date.strftime("%Y%m%d")),
                        date,
                        date.year,
                        date.month,
                        (date.month - 1) // 3 + 1,
                        date.day,
                    ))

                insert_rows(cur, """
                    INSERT INTO dim_date
                    (date_key, full_date, year, month, quarter, day)
                    VALUES %s
                """, rows)

                # 4. Load payment dimension.
                payments = data["payments"]

                rows = [
                    tuple(clean_value(row[col]) for col in [
                        "payment_id", "order_id", "payment_method",
                        "status", "amount", "payment_date"
                    ])
                    for _, row in payments.iterrows()
                ]

                insert_rows(cur, """
                    INSERT INTO dim_payment
                    (payment_id, order_id, payment_method,
                     payment_status, amount, payment_date)
                    VALUES %s
                """, rows)

                # 5. Retrieve warehouse surrogate keys.
                cur.execute("""
                    SELECT customer_id, customer_key
                    FROM dim_customer
                """)
                customer_keys = dict(cur.fetchall())

                cur.execute("""
                    SELECT product_id, product_key
                    FROM dim_product
                """)
                product_keys = dict(cur.fetchall())

                cur.execute("""
                    SELECT date_key, date_key
                    FROM dim_date
                """)
                date_keys = dict(cur.fetchall())

                # Select one representative payment per order.
                # Prefer successful payments, then the latest date.
                cur.execute("""
                    SELECT DISTINCT ON (order_id)
                        order_id, payment_key
                    FROM dim_payment
                    ORDER BY
                        order_id,
                        (payment_status = 'successful') DESC,
                        payment_date DESC,
                        payment_key DESC
                """)
                payment_keys = dict(cur.fetchall())

                # 6. Load sales fact table: one row per order item.
                rows = []

                for _, row in sales.iterrows():
                    customer_id = int(row["customer_id"])
                    product_id = int(row["product_id"])
                    date_key = int(row["date_key"])
                    order_id = int(row["order_id"])

                    if (
                        customer_id not in customer_keys
                        or product_id not in product_keys
                        or date_key not in date_keys
                    ):
                        continue

                    rows.append((
                        int(row["order_item_id"]),
                        order_id,
                        customer_keys[customer_id],
                        product_keys[product_id],
                        date_keys[date_key],
                        payment_keys.get(order_id),
                        int(row["quantity"]),
                        clean_value(row["unit_price"]),
                        clean_value(row["total_amount"]),
                        str(row["status"]),
                    ))

                insert_rows(cur, """
                    INSERT INTO fact_sales
                    (order_item_id, order_id, customer_key, product_key,
                     date_key, payment_key, quantity, unit_price,
                     total_amount, order_status)
                    VALUES %s
                """, rows)

                # 7. Load MongoDB reviews.
                reviews = data["reviews"]
                rows = []

                for _, row in reviews.iterrows():
                    rows.append((
                        clean_value(row.get("customer_id")),
                        clean_value(row.get("product_id")),
                        clean_value(row.get("rating")),
                        clean_value(row.get("comment")),
                        clean_value(row.get("tags")),
                        clean_value(row.get("created_at")),
                    ))

                insert_rows(cur, """
                    INSERT INTO fact_reviews
                    (customer_id, product_id, rating, comment,
                     tags, created_at)
                    VALUES %s
                """, rows)

                # 8. Load flattened user activity.
                activities = data["user_activity"]
                rows = []

                for _, row in activities.iterrows():
                    action_data = {
                        col.removeprefix("action_"): clean_value(value)
                        for col, value in row.items()
                        if col.startswith("action_")
                    }

                    device_data = {
                        col.removeprefix("device_"): clean_value(value)
                        for col, value in row.items()
                        if col.startswith("device_")
                    }

                    rows.append((
                        clean_value(row.get("customer_id")),
                        clean_value(row.get("session_id")),
                        Json(action_data),
                        Json(device_data),
                    ))

                insert_rows(cur, """
                    INSERT INTO fact_user_activity
                    (customer_id, session_id, action_data, device_data)
                    VALUES %s
                """, rows)

        print("\nWarehouse load completed successfully.")

        # Verify loaded row counts.
        with conn.cursor() as cur:
            for table in [
                "dim_customer",
                "dim_product",
                "dim_date",
                "dim_payment",
                "fact_sales",
                "fact_reviews",
                "fact_user_activity",
            ]:
                cur.execute(f"SELECT COUNT(*) FROM {table}")
                print(f"{table}: {cur.fetchone()[0]} rows")

    finally:
        conn.close()


if __name__ == "__main__":
    from src.extract import extract_all
    from src.transform import transform_all

    raw_data = extract_all()
    transformed_data = transform_all(raw_data)
    load_warehouse(transformed_data)
