
import pandas as pd

from src.database import get_postgres_connection, get_mongo_client


def extract_postgres_data():
    """Extract the five source tables from PostgreSQL."""

    queries = {
        "customers": "SELECT * FROM customers",
        "products": "SELECT * FROM products",
        "orders": "SELECT * FROM orders",
        "order_items": "SELECT * FROM order_items",
        "payments": "SELECT * FROM payments",
    }

    conn = get_postgres_connection()

    try:
        data = {}

        for table_name, query in queries.items():
            data[table_name] = pd.read_sql_query(query, conn)
            print(
                f"PostgreSQL | {table_name}: "
                f"{len(data[table_name])} rows"
            )

        return data

    finally:
        conn.close()


def extract_mongodb_data():
    """Extract reviews and user activity from MongoDB."""

    client = get_mongo_client()

    try:
        db = client["ecommerce_nosql"]

        reviews = list(db.reviews.find({}, {"_id": 0}))
        activities = list(db.user_activity.find({}, {"_id": 0}))

        data = {
            "reviews": pd.DataFrame(reviews),
            "user_activity": pd.DataFrame(activities),
        }

        print(f"MongoDB | reviews: {len(reviews)} documents")
        print(f"MongoDB | user_activity: {len(activities)} documents")

        return data

    finally:
        client.close()


def extract_all():
    """Extract all datasets from both source databases."""

    data = extract_postgres_data()
    data.update(extract_mongodb_data())

    return data


if __name__ == "__main__":
    extracted_data = extract_all()

    print("\n--- Extraction Summary ---")

    for name, dataframe in extracted_data.items():
        print(f"{name}: {len(dataframe)} rows")

    print("\nExtraction completed successfully.")
