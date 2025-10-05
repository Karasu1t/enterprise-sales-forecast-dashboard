resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "${var.environment}_${var.id}_sales"
  friendly_name               = "test"
  location                    = "ASIA-NORTHEAST1"
  default_table_expiration_ms = 3600000

  access {
    role          = "OWNER"
    user_by_email = var.email
  }

  access {
    role          = "OWNER"
    user_by_email = var.email_mas
  }
}
