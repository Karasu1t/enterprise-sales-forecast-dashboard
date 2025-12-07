# train.py
# This script trains a RandomForestRegressor model for sales quantity prediction using time-series cross-validation.
# - Loads data from a CSV file (default: data.csv) or a BigQuery table
# - Drops unnecessary columns
# - Uses all columns except 'quantity' and 'date' as features
# - Performs 5-fold TimeSeriesSplit cross-validation
# - Prints average RMSE and R2 across folds
# - Saves the final model to a file (default: model.joblib)

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, r2_score
import argparse
import joblib
import os
from google.cloud import storage
import numpy as np

# Set data path and output path via command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--model_path", type=str, default="model.joblib")
parser.add_argument(
    "--bq_table",
    type=str,
    default=None,
    help="BigQuery table in format project.dataset.table",
)
parser.add_argument(
    "--project_id", type=str, default=None, help="GCP project ID for BigQuery"
)
args = parser.parse_args()


# Load data
if args.bq_table:
    print(f"Loading data from BigQuery table: {args.bq_table}")
    if not args.project_id:
        raise ValueError("--project_id is required when using --bq_table")
    df = pd.read_gbq(
        f"SELECT * FROM `{args.bq_table}`",
        project_id=args.project_id,
        location="asia-northeast1",
    )
else:
    print(f"Loading data from {args.data_path}")
    df = pd.read_csv(args.data_path, encoding="utf-8")

# Required features: date→year, month, day, is_cup_ramen, is_pet_bottle_tea, is_chocolate
for col in ["is_cup_ramen", "is_pet_bottle_tea", "is_chocolate"]:
    if col not in df.columns:
        raise ValueError(f"{col} column is required in the data.")

# Convert date to datetime and extract year, month, day as features
df["date"] = pd.to_datetime(df["date"])
df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day

# Feature list: required (year, month, day, is_XXXX) + optional (if present: price, sales, weather, holiday_flag, weather_flag)
feature_cols = [
    "year",
    "month",
    "day",
    "is_cup_ramen",
    "is_pet_bottle_tea",
    "is_chocolate",
]
optional_cols = ["price", "sales", "weather", "holiday_flag", "weather_flag"]
for col in optional_cols:
    if col in df.columns:
        feature_cols.append(col)


# Define features and target
X = df[feature_cols]
y = df["quantity"]

# Train and evaluate with time-series cross-validation
ts_cv = TimeSeriesSplit(n_splits=5)
rmse_list = []
r2_list = []
for train_idx, test_idx in ts_cv.split(X):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    rmse_list.append(mean_squared_error(y_test, y_pred, squared=False))
    r2_list.append(r2_score(y_test, y_pred))

# print(f"Average RMSE: {sum(rmse_list)/len(rmse_list):.2f}")
# print(f"Average R2: {sum(r2_list)/len(r2_list):.2f}")

# Save the model trained on the last fold
local_model_path = "model.joblib"
joblib.dump(model, local_model_path)
print(f"Model saved locally to {local_model_path}")

if args.model_path.startswith("gs://"):
    print(f"Uploading model to GCS: {args.model_path}")
    bucket_name = args.model_path.replace("gs://", "").split("/")[0]
    blob_name = "/".join(args.model_path.replace("gs://", "").split("/")[1:])
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_model_path)
    print(f"Model uploaded to GCS: {args.model_path}")
else:
    joblib.dump(model, args.model_path)
    print(f"Model saved to {args.model_path}")
