
from src.database import get_mongo_client


def seed_mongodb():
    client = get_mongo_client()

    try:
        db = client["ecommerce_nosql"]

        # Reset only this project's collections.
        for name in ["reviews", "user_activity"]:
            if name in db.list_collection_names():
                db[name].delete_many({})
            else:
                db.create_collection(name)

        reviews = [
            {
                "customer_id": 1,
                "product_id": 101,
                "rating": 5,
                "comment": "Excellent mouse",
                "tags": ["quality", "value"],
                "created_at": "2026-01-06",
            },
            {
                "customer_id": 1,
                "product_id": 102,
                "rating": 4,
                "comment": "Good keyboard",
                "tags": ["quality"],
                "created_at": "2026-01-07",
            },
            {
                "customer_id": 2,
                "product_id": 104,
                "rating": 5,
                "comment": "Very comfortable",
                "tags": ["comfort", "quality"],
                "created_at": "2026-01-14",
            },
            {
                "customer_id": 3,
                "product_id": 106,
                "rating": 4,
                "comment": "Works very well",
                "tags": ["useful"],
                "created_at": "2026-01-22",
            },
            {
                "customer_id": 4,
                "product_id": 102,
                "rating": 3,
                "comment": "Good but noisy",
                "tags": ["mixed"],
                "created_at": "2026-02-12",
            },
            {
                "customer_id": 6,
                "product_id": 104,
                "rating": 5,
                "comment": "Great shoes",
                "tags": ["comfort"],
                "created_at": "2026-03-05",
            },
            {
                "customer_id": 8,
                "product_id": 105,
                "rating": 4,
                "comment": "Nice fabric",
                "tags": ["quality"],
                "created_at": "2026-03-24",
            },
            {
                "customer_id": 9,
                "product_id": 103,
                "rating": 2,
                "comment": "Could be better",
                "tags": ["mixed"],
                "created_at": "2026-04-03",
            },
            {
                "customer_id": 10,
                "product_id": 106,
                "rating": 5,
                "comment": "Excellent coffee maker",
                "tags": ["quality", "value"],
                "created_at": "2026-04-11",
            },
            {
                "customer_id": 12,
                "product_id": 108,
                "rating": 4,
                "comment": "Useful bottle",
                "tags": ["value"],
                "created_at": "2026-05-23",
            },
            {
                "customer_id": 1,
                "product_id": 101,
                "rating": 4,
                "comment": "Still working well",
                "tags": ["durability"],
                "created_at": "2026-07-20",
            },
        ]

        activities = [
            {
                "customer_id": 1,
                "session_id": "SES001",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 101,
                        "timestamp": "2026-01-05 09:00",
                    },
                    {
                        "type": "add_to_cart",
                        "product_id": 101,
                        "timestamp": "2026-01-05 09:05",
                    },
                    {
                        "type": "purchase",
                        "product_id": 101,
                        "timestamp": "2026-01-05 09:10",
                    },
                ],
                "device": {"type": "mobile", "os": "Android"},
            },
            {
                "customer_id": 2,
                "session_id": "SES002",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 104,
                        "timestamp": "2026-01-12 10:00",
                    },
                    {
                        "type": "purchase",
                        "product_id": 104,
                        "timestamp": "2026-01-12 10:15",
                    },
                ],
                "device": {"type": "desktop", "os": "Windows"},
            },
            {
                "customer_id": 3,
                "session_id": "SES003",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 106,
                        "timestamp": "2026-01-20 12:00",
                    },
                    {
                        "type": "add_to_cart",
                        "product_id": 106,
                        "timestamp": "2026-01-20 12:10",
                    },
                ],
                "device": {"type": "tablet", "os": "Android"},
            },
            {
                "customer_id": 4,
                "session_id": "SES004",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 102,
                        "timestamp": "2026-02-10 14:00",
                    }
                ],
                "device": {"type": "mobile", "os": "iOS"},
            },
            {
                "customer_id": 6,
                "session_id": "SES005",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 104,
                        "timestamp": "2026-03-03 16:00",
                    },
                    {
                        "type": "add_to_cart",
                        "product_id": 104,
                        "timestamp": "2026-03-03 16:05",
                    },
                    {
                        "type": "purchase",
                        "product_id": 104,
                        "timestamp": "2026-03-03 16:10",
                    },
                ],
                "device": {"type": "desktop", "os": "macOS"},
            },
            {
                "customer_id": 8,
                "session_id": "SES006",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 105,
                        "timestamp": "2026-03-22 11:00",
                    },
                    {
                        "type": "add_to_cart",
                        "product_id": 105,
                        "timestamp": "2026-03-22 11:03",
                    },
                ],
                "device": {"type": "mobile", "os": "Android"},
            },
            {
                "customer_id": 10,
                "session_id": "SES007",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 106,
                        "timestamp": "2026-04-09 13:00",
                    },
                    {
                        "type": "purchase",
                        "product_id": 106,
                        "timestamp": "2026-04-09 13:20",
                    },
                ],
                "device": {"type": "desktop", "os": "Windows"},
            },
            {
                "customer_id": 12,
                "session_id": "SES008",
                "actions": [
                    {
                        "type": "view_product",
                        "product_id": 108,
                        "timestamp": "2026-05-21 18:00",
                    }
                ],
                "device": {"type": "mobile", "os": "iOS"},
            },
        ]

        if reviews:
            db.reviews.insert_many(reviews)

        if activities:
            db.user_activity.insert_many(activities)

        db.reviews.create_index(
            [("customer_id", 1), ("product_id", 1)]
        )
        db.user_activity.create_index("customer_id")

        print("MongoDB seed completed successfully.")
        print("Reviews:", db.reviews.count_documents({}))
        print("Activity sessions:", db.user_activity.count_documents({}))

    finally:
        client.close()


if __name__ == "__main__":
    seed_mongodb()