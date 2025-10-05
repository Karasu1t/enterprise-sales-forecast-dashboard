resource "google_cloudfunctions_function" "etl_function" {
  name                  = "${var.environment}-${var.id}-etl-function"
  runtime               = "python310"
  entry_point           = "etl_handler"
  region                = var.gcp_region
  project               = var.project
  source_archive_bucket = var.source_bucket
  source_archive_object = var.script
  available_memory_mb   = 512
  environment_variables = {
    DATASET  = var.dataset
    TABLE_ID = "${var.dataset}.sales_raw"
  }
  service_account_email = google_service_account.etl_sa.email

  event_trigger {
    event_type = "google.storage.object.finalize"
    resource   = var.trigger_bucket
    # optional: object name prefix filter (e.g. "raw_data/")
    # failure_policy { retry = true }
  }
}

resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = var.project
  region         = var.gcp_region
  cloud_function = google_cloudfunctions_function.etl_function.name
  role           = "roles/cloudfunctions.invoker"
  member         = "serviceAccount:${var.email}"
}

resource "google_service_account" "etl_sa" {
  project      = var.project
  account_id   = "etl-function-sa"
  display_name = "Service Account for ETL Function"
}

resource "google_project_iam_member" "function_storage" {
  project = var.project
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.etl_sa.email}"
}

resource "google_project_iam_member" "function_bigquery" {
  project = var.project
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.etl_sa.email}"
}

resource "google_project_iam_member" "function_bigquery_jobuser" {
  project = var.project
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.etl_sa.email}"
}
