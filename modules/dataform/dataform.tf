# Dataform
resource "google_dataform_repository" "etl" {
  provider        = google-beta
  project         = var.project
  region          = var.region
  name            = var.repository_name
  display_name    = var.display_name
  deletion_policy = "FORCE"
}
