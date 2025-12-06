resource "google_artifact_registry_repository" "sales_data_learning_model_repo" {
  project       = var.project
  location      = var.location
  repository_id = var.repository_id
  format        = "DOCKER"
}
