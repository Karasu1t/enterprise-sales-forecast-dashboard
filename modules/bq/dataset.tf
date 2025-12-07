resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "${var.environment}_${var.id}_sales"
  friendly_name               = "test"
  location                    = "ASIA-NORTHEAST1"

  access {
    role          = "OWNER"
    user_by_email = var.email
  }

  access {
    role          = "OWNER"
    user_by_email = var.email_mas
  }
}

resource "google_bigquery_table" "sales_raw" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "sales_raw"
  schema = jsonencode([
    { name = "date", type = "DATE", mode = "NULLABLE" },
    { name = "product_name", type = "STRING", mode = "NULLABLE" },
    { name = "quantity", type = "INT64", mode = "NULLABLE" },
    { name = "price", type = "INT64", mode = "NULLABLE" },
    { name = "sales", type = "INT64", mode = "NULLABLE" },
    { name = "weather", type = "STRING", mode = "NULLABLE" },
    { name = "holiday_flag", type = "INT64", mode = "NULLABLE" }
  ])
  time_partitioning {
    type  = "DAY"
    field = "date"
  }
  deletion_protection = false
}
