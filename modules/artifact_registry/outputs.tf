output "repository_id" {
  value = google_artifact_registry_repository.sales_data_learning_model_repo.repository_id
}

output "repository_url" {
  value = google_artifact_registry_repository.sales_data_learning_model_repo.id
}

output "dashboard_repository_id" {
  value = google_artifact_registry_repository.sales_data_dahboard_repo.repository_id
}

output "dashboard_repository_url" {
  value = google_artifact_registry_repository.sales_data_dahboard_repo.id
}
