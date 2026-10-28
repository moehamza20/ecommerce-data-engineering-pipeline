
from src.extract import extract_all
from src.transform import transform_all
from src.load import load_warehouse


def run_pipeline():
    print("=== ETL PIPELINE STARTED ===")

    print("\n[1/3] Extracting source data...")
    raw_data = extract_all()

    print("\n[2/3] Transforming data...")
    transformed_data = transform_all(raw_data)

    print("\n[3/3] Loading warehouse...")
    load_warehouse(transformed_data)

    print("\n=== ETL PIPELINE COMPLETED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_pipeline()
