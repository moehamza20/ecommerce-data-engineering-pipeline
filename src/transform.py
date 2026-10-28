
import pandas as pd


def clean_text_columns(df):
    """Remove leading/trailing whitespace from text columns."""
    df = df.copy()

    for column in df.select_dtypes(include=["object", "string"]).columns:
        df[column] = df[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

    return df


def transform_postgres_data(data):
    """Clean PostgreSQL tables and prepare enriched sales lines."""

    transformed = {}

    # 1. Clean text and remove duplicate rows.
    for table_name in [
        "customers",
        "products",
        "orders",
        "order_items",
        "payments",
    ]:
        df = clean_text_columns(data[table_name])
        df = df.drop_duplicates().copy()
        transformed[table_name] = df

    customers = transformed["customers"]
    products = transformed["products"]
    orders = transformed["orders"]
    order_items = transformed["order_items"]
    payments = transformed["payments"]

    # 2. Convert dates to datetime.
    customers["signup_date"] = pd.to_datetime(
        customers["signup_date"], errors="coerce"
    )
    orders["order_date"] = pd.to_datetime(
        orders["order_date"], errors="coerce"
    )
    payments["payment_date"] = pd.to_datetime(
        payments["payment_date"], errors="coerce"
    )

    # 3. Convert numeric fields and remove invalid records.
    products["price"] = pd.to_numeric(
        products["price"], errors="coerce"
    )
    products["stock"] = pd.to_numeric(
        products["stock"], errors="coerce"
    )
    order_items["quantity"] = pd.to_numeric(
        order_items["quantity"], errors="coerce"
    )
    payments["amount"] = pd.to_numeric(
        payments["amount"], errors="coerce"
    )

    customers = customers.dropna(
        subset=["customer_id", "email", "signup_date"]
    )
    products = products.dropna(
        subset=["product_id", "price", "stock"]
    )
    orders = orders.dropna(
        subset=["order_id", "customer_id", "order_date", "status"]
    )
    order_items = order_items.dropna(
        subset=["order_item_id", "order_id", "product_id", "quantity"]
    )
    payments = payments.dropna(
        subset=["payment_id", "order_id", "amount", "payment_date"]
    )

    products = products[
        (products["price"] >= 0) & (products["stock"] >= 0)
    ]
    order_items = order_items[order_items["quantity"] > 0]
    payments = payments[payments["amount"] >= 0]

    # Update cleaned datasets.
    transformed["customers"] = customers
    transformed["products"] = products
    transformed["orders"] = orders
    transformed["order_items"] = order_items
    transformed["payments"] = payments

    # 4. Join order items to orders and products.
    # Each output row represents one order line.
    sales = order_items.merge(
        orders[["order_id", "customer_id", "order_date", "status"]],
        on="order_id",
        how="inner",
        validate="many_to_one",
    )

    sales = sales.merge(
        products[["product_id", "name", "category", "price"]],
        on="product_id",
        how="inner",
        validate="many_to_one",
        suffixes=("", "_product"),
    )

    sales = sales.rename(
        columns={
            "name": "product_name",
            "price": "unit_price",
        }
    )

    # 5. Calculate line revenue from quantity and product price.
    sales["total_amount"] = (
        sales["quantity"] * sales["unit_price"]
    ).round(2)

    # 6. Derive calendar attributes for warehouse analytics.
    sales["year"] = sales["order_date"].dt.year
    sales["month"] = sales["order_date"].dt.month
    sales["quarter"] = sales["order_date"].dt.quarter
    sales["date_key"] = sales["order_date"].dt.strftime("%Y%m%d").astype(int)

    transformed["sales"] = sales

    print("\nPostgreSQL transformation complete.")
    print(f"Enriched sales lines: {len(sales)}")

    return transformed


def transform_mongodb_data(data):
    """Clean reviews and flatten nested user activity."""

    # 1. Reviews.
    reviews = clean_text_columns(data["reviews"])

# Convert list-valued tags into strings before deduplication.
    if "tags" in reviews.columns:
        reviews["tags"] = reviews["tags"].apply(
            lambda value: tuple(value)
            if isinstance(value, list)
            else value
        )

    reviews = reviews.drop_duplicates().copy()

    if "rating" in reviews.columns:
        reviews["rating"] = pd.to_numeric(
            reviews["rating"], errors="coerce"
        )
        reviews = reviews[
            reviews["rating"].between(1, 5)
        ].copy()

    if "created_at" in reviews.columns:
        reviews["created_at"] = pd.to_datetime(
            reviews["created_at"], errors="coerce", utc=True
        )

    # Convert the tags array into a readable string.
    if "tags" in reviews.columns:
        reviews["tags"] = reviews["tags"].apply(
            lambda value: ", ".join(map(str, value))
            if isinstance(value, list)
            else ""
        )

    # 2. Flatten activity: one row per action.
    activities = data["user_activity"].copy()

    if activities.empty:
        flat_activities = pd.DataFrame()
    else:
        activities = activities.explode(
            "actions", ignore_index=True
        )

        # Expand nested action objects into columns.
        action_details = pd.json_normalize(
            activities["actions"].tolist()
        ).add_prefix("action_")

        activities = activities.drop(
            columns=["actions"]
        ).reset_index(drop=True)

        flat_activities = pd.concat(
            [activities, action_details], axis=1
        )

        # Expand nested device objects into columns.
        if "device" in flat_activities.columns:
            device_details = pd.json_normalize(
                flat_activities["device"].tolist()
            ).add_prefix("device_")

            flat_activities = flat_activities.drop(
                columns=["device"]
            ).reset_index(drop=True)

            flat_activities = pd.concat(
                [flat_activities, device_details], axis=1
            )

        flat_activities = clean_text_columns(flat_activities)

    print("\nMongoDB transformation complete.")
    print(f"Clean reviews: {len(reviews)}")
    print(f"Flattened activity actions: {len(flat_activities)}")

    return {
        "reviews": reviews,
        "user_activity": flat_activities,
    }


def transform_all(data):
    """Transform all extracted datasets."""

    transformed = transform_postgres_data(data)
    transformed.update(transform_mongodb_data(data))

    return transformed


if __name__ == "__main__":
    from src.extract import extract_all

    raw_data = extract_all()
    transformed_data = transform_all(raw_data)

    print("\n--- Transformation Summary ---")

    for name, dataframe in transformed_data.items():
        print(f"{name}: {len(dataframe)} rows")

    print("\nTransformation completed successfully.")
