from google.cloud import storage, bigquery
import pandas as pd

import io
import os


def etl_handler(data, context):
    # Read CSV from GCS (triggered by upload event)
    bucket_name = data["bucket"]
    file_name = data["name"]
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    content = blob.download_as_bytes()

    # Convert to pandas DataFrame
    df = pd.read_csv(io.BytesIO(content))
    # Convert Japanese column names to English
    col_map = {
        "日付": "date",
        "商品名": "product_name",
        "個数": "quantity",
        "商品価格": "price",
        "売上": "sales",
        "天気": "weather",
        "祝日フラグ": "holiday_flag",
    }
    df.rename(columns=col_map, inplace=True)

    # Data type conversion
    df["date"] = pd.to_datetime(df["date"]).dt.date
    df["product_name"] = df["product_name"].astype(str)
    df["quantity"] = df["quantity"].astype("Int64")
    df["price"] = df["price"].astype("Int64")
    df["sales"] = df["sales"].astype("Int64")
    df["weather"] = df["weather"].astype(str)

    # Load only new records to BigQuery (partitioned table)
    bq_client = bigquery.Client()
    table_id = os.environ.get("TABLE_ID")
    if not table_id:
        raise ValueError("TABLE_ID environment variable is not set")

    # Get existing primary keys (date, product_name) from BigQuery (skip if table does not exist)
    try:
        query = f"""
            SELECT date, product_name
            FROM `{table_id}`
            WHERE date IN UNNEST(@dates)
        """
        job_config_query = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ArrayQueryParameter(
                    "dates", "DATE", df["date"].unique().tolist()
                )
            ]
        )
        existing = bq_client.query(query, job_config=job_config_query).to_dataframe()
    except NotFound:
        existing = pd.DataFrame()  # Table does not exist yet

    # Extract only new records (difference)
    if not existing.empty:
        df = df.merge(existing, on=["date", "product_name"], how="left", indicator=True)
        df = df[df["_merge"] == "left_only"].drop(columns=["_merge"])

    # Insert only new records to BigQuery
    if not df.empty:
        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_APPEND",
            schema=[
                bigquery.SchemaField("date", "DATE"),
                bigquery.SchemaField("product_name", "STRING"),
                bigquery.SchemaField("quantity", "INT64"),
                bigquery.SchemaField("price", "INT64"),
                bigquery.SchemaField("sales", "INT64"),
                bigquery.SchemaField("weather", "STRING"),
            ],
            time_partitioning=bigquery.TimePartitioning(
                type_=bigquery.TimePartitioningType.DAY, field="date"
            ),
            source_format=(
                bigquery.SourceFormat.PARQUET
                if blob.name.endswith(".parquet")
                else bigquery.SourceFormat.CSV
            ),
        )
        job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()

    return "ETL complete and only new records loaded", 200
