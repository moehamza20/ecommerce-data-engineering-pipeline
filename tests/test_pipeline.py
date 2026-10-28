
from src.extract import extract_all
from src.transform import transform_all


def test_source_data_counts():
    data = extract_all()

    assert len(data["customers"]) == 12
    assert len(data["products"]) == 8
    assert len(data["orders"]) == 20
    assert len(data["order_items"]) == 25
    assert len(data["payments"]) == 20
    assert len(data["reviews"]) == 11
    assert len(data["user_activity"]) == 8


def test_transformed_data_quality():
    raw_data = extract_all()
    data = transform_all(raw_data)

    assert len(data["sales"]) == 25
    assert len(data["reviews"]) == 11
    assert len(data["user_activity"]) == 16

    assert data["sales"]["total_amount"].notna().all()
    assert (data["sales"]["total_amount"] >= 0).all()
    assert data["sales"]["order_item_id"].is_unique

    assert data["reviews"]["rating"].dropna().between(1, 5).all()
