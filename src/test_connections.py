
from src.database import get_postgres_connection, get_mongo_client


def main():
    # Test PostgreSQL
    conn = get_postgres_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT current_database();")
            print("PostgreSQL database:", cur.fetchone()[0])

            for table in (
                "customers",
                "products",
                "orders",
                "order_items",
                "payments",
            ):
                cur.execute(f"SELECT COUNT(*) FROM {table};")
                print(f"{table}: {cur.fetchone()[0]} rows")
    finally:
        conn.close()

    # Test MongoDB
    client = get_mongo_client()

    try:
        db = client["ecommerce_nosql"]

        print("\nMongoDB database:", db.name)
        print("Reviews:", db.reviews.count_documents({}))
        print("Activity sessions:", db.user_activity.count_documents({}))
    finally:
        client.close()


if __name__ == "__main__":
    main()
