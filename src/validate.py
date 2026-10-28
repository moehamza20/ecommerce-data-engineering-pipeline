
from src.database import get_warehouse_connection


def validate_warehouse():
    """Run basic data-quality checks against the warehouse."""

    checks = {
        "fact_sales is not empty": """
            SELECT COUNT(*) FROM fact_sales
        """,
        "No null sales amounts": """
            SELECT COUNT(*) FROM fact_sales
            WHERE total_amount IS NULL
        """,
        "Sales totals are calculated correctly": """
            SELECT COUNT(*) FROM fact_sales
            WHERE total_amount <> quantity * unit_price
        """,
        "No missing customer references": """
            SELECT COUNT(*)
            FROM fact_sales fs
            LEFT JOIN dim_customer dc
                ON fs.customer_key = dc.customer_key
            WHERE dc.customer_key IS NULL
        """,
        "No missing product references": """
            SELECT COUNT(*)
            FROM fact_sales fs
            LEFT JOIN dim_product dp
                ON fs.product_key = dp.product_key
            WHERE dp.product_key IS NULL
        """,
        "No missing date references": """
            SELECT COUNT(*)
            FROM fact_sales fs
            LEFT JOIN dim_date dd
                ON fs.date_key = dd.date_key
            WHERE dd.date_key IS NULL
        """,
        "Review ratings are valid": """
            SELECT COUNT(*) FROM fact_reviews
            WHERE rating IS NOT NULL
              AND (rating < 1 OR rating > 5)
        """,
    }

    conn = get_warehouse_connection()

    try:
        with conn.cursor() as cursor:
            failed_checks = []

            for name, query in checks.items():
                cursor.execute(query)
                result = cursor.fetchone()[0]

                if name == "fact_sales is not empty":
                    passed = result > 0
                else:
                    passed = result == 0

                status = "PASS" if passed else "FAIL"
                print(f"[{status}] {name} (result: {result})")

                if not passed:
                    failed_checks.append(name)

        if failed_checks:
            raise RuntimeError(
                f"Warehouse validation failed: {failed_checks}"
            )

        print("\nAll warehouse validation checks passed.")

    finally:
        conn.close()


if __name__ == "__main__":
    validate_warehouse()
