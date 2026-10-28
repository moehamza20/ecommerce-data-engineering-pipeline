
# E-Commerce Data Engineering Pipeline

An end-to-end data engineering project that integrates relational and NoSQL data sources, processes data through a Python ETL pipeline, loads it into a PostgreSQL data warehouse, and presents business insights through an interactive Streamlit dashboard.

## Project Overview

This project simulates an e-commerce analytics environment by combining structured transactional data from PostgreSQL with customer reviews and user activity data from MongoDB.

The pipeline extracts, cleans, transforms, and loads the data into a dimensional data warehouse. Analytical SQL queries and an interactive dashboard are then used to explore sales performance, revenue trends, product performance, customer spending, inventory, and customer reviews.

## Technologies Used

- **Python** — ETL development and data processing
- **Pandas** — data cleaning, transformation, and manipulation
- **PostgreSQL** — relational source database and data warehouse
- **MongoDB** — NoSQL source data for reviews and user activity
- **SQL** — schema design, joins, aggregations, and analytical queries
- **Streamlit** — interactive analytics dashboard
- **Plotly** — data visualization
- **psycopg2** — PostgreSQL connectivity
- **PyMongo** — MongoDB connectivity
- **python-dotenv** — environment variable management
- **pytest** — automated testing

## Architecture

```text
PostgreSQL Source                MongoDB Source
(ecommerce_source)              (ecommerce_nosql)
        |                              |
        +--------------+---------------+
                       |
                 Python ETL
                       |
             +---------+---------+
             |                   |
          Extract             Transform
             |                   |
             +---------+---------+
                       |
                     Load
                       |
              PostgreSQL Warehouse
                 (ecommerce_dw)
                       |
              +--------+--------+
              |                 |
         SQL Analytics    Streamlit Dashboard
```

## Data Sources

### PostgreSQL

The relational source database contains five tables:

- `customers` — customer information
- `products` — product details, categories, prices, and stock
- `orders` — order dates and statuses
- `order_items` — products and quantities within orders
- `payments` — payment methods, amounts, dates, and statuses

### MongoDB

The NoSQL database contains two collections:

- `reviews` — customer ratings, comments, tags, and timestamps
- `user_activity` — customer sessions, nested actions, and device information

## ETL Pipeline

The Python ETL pipeline performs three main stages:

### 1. Extract

- Retrieves relational tables from PostgreSQL.
- Retrieves review and activity documents from MongoDB.
- Converts the extracted datasets into Pandas DataFrames.

### 2. Transform

- Cleans text fields and handles missing or invalid values.
- Removes duplicate records.
- Converts dates and numeric fields to appropriate types.
- Merges orders, order items, and products.
- Calculates sales line totals using quantity and unit price.
- Derives date attributes such as year, month, quarter, and date key.
- Flattens nested MongoDB activity documents and processes review tags.

### 3. Load

Loads the transformed data into `ecommerce_dw`, using a dimensional model consisting of:

**Dimension tables**

- `dim_customer`
- `dim_product`
- `dim_date`
- `dim_payment`

**Fact tables**

- `fact_sales`
- `fact_reviews`
- `fact_user_activity`

The sales fact table connects customers, products, dates, and payments using warehouse keys.

## SQL Analytics

The project includes at least 10 analytical SQL queries covering:

1. Total revenue from completed orders
2. Number of completed orders
3. Average order value
4. Monthly revenue
5. Revenue by product category
6. Top five products by revenue
7. Top five customers by spending
8. Payment distribution by method and status
9. Low-stock products
10. Average product review ratings

The queries demonstrate SQL aggregation, filtering, joins, grouping, sorting, and common table expressions (CTEs).

## Streamlit Dashboard

The interactive dashboard provides:

- Completed revenue
- Completed order count
- Average order value
- Number of purchasing customers
- Monthly revenue trend
- Revenue by product category
- Top five products
- Top five customers

Dashboard data is retrieved from the PostgreSQL warehouse. Query results are cached briefly to reduce repeated database requests.

## Project Structure

```text
Ecommerce Data plipeline project/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── database.py
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   ├── etl_pipeline.py
│   ├── validate.py
│   └── seed_mongodb.py
├── sql/
│   ├── schema.sql
│   └── analysis.sql
└── tests/
    └── test_pipeline.py
```

*Note: Adjust filenames in this tree if your actual project structure differs.*

## Setup and Installation

### Prerequisites

Install the following:

- Python 3.10 or later
- PostgreSQL
- MongoDB Community Server
- Git (optional, for version control)

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd "<your-project-folder>"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env` and update the values for your local environment.

The configuration should include:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce_source
POSTGRES_DW_DB=ecommerce_dw
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password

MONGO_URI=mongodb://localhost:27017/
```

Use your own database credentials. Never commit `.env` or expose database passwords in the repository.

### 5. Create and seed the source databases

Create the PostgreSQL source database named `ecommerce_source`.

Execute the SQL files in this order:

1. `sql/source_schema.sql`
2. `sql/source_seed.sql`

Create the MongoDB database `ecommerce_nosql` and populate the `reviews` and `user_activity` collections using the MongoDB seed script.

Ensure the MongoDB server is running before executing the script.

### 6. Create the data warehouse

Create a separate PostgreSQL database named `ecommerce_dw`.

Execute `sql/schema.sql` against `ecommerce_dw` to create the dimension and sales fact tables.

The ETL loader creates the additional review and activity warehouse tables if they do not already exist.

## Running the Project

Run commands from the project root.

### Execute the ETL pipeline

```bash
python -m src.etl_pipeline
```

The pipeline extracts the source data, transforms it, and reloads the warehouse.

### Validate warehouse data

```bash
python -m src.validate
```

This runs data-quality checks for sales records, sales totals, dimension references, and review ratings.

### Run automated tests

```bash
python -m pytest tests/test_pipeline.py -v
```

### Start the dashboard

```bash
python -m streamlit run app.py
```

Streamlit will provide a local URL for opening the dashboard in your browser.

### Execute analytical SQL

Open `sql/analysis.sql` in your PostgreSQL client and execute the queries against `ecommerce_dw`.

## Data Quality and Testing

The project includes automated checks for:

- Expected source record counts
- Expected transformed record counts
- Non-null sales amounts
- Correct sales line calculations
- Unique sales line identifiers
- Valid review ratings
- Missing dimension references in the warehouse

The ETL pipeline and warehouse validation script can be rerun to check the integrity of the loaded data.

## Key Learning Outcomes

- Integrating SQL and NoSQL data sources
- Building a Python-based ETL pipeline
- Cleaning and transforming structured and nested data
- Designing a dimensional data warehouse
- Writing analytical SQL queries for business reporting
- Developing an interactive dashboard
- Implementing data-quality checks and automated tests

## Future Improvements

- Add incremental ETL processing instead of full reloads.
- Introduce workflow orchestration with Apache Airflow.
- Add automated scheduling and pipeline monitoring.
- Containerize services using Docker.
- Deploy the dashboard and data infrastructure to the cloud.

## Author

**Mohamed Hamza**

Computer Science Graduate | Data Engineering
