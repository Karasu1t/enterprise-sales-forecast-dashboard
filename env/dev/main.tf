# Storage
module "storage" {
  source      = "../../modules/storage"
  id          = var.id
  project     = var.project
  environment = var.environment
}

# bq
module "bq" {
  source      = "../../modules/bq"
  id          = var.id
  environment = var.environment
  project     = var.project
  email       = var.email
  email_mas   = var.email_mas
}

# Function
module "function" {
  source         = "../../modules/functions"
  id             = var.id
  project        = var.project
  environment    = var.environment
  gcp_region     = var.gcp_region
  email          = var.email
  dataset        = module.bq.dataset
  source_bucket  = module.storage.import_script
  trigger_bucket = module.storage.salesdata
}

# Artifact Registry
module "artifactregistry" {
  source        = "../../modules/artifact_registry"
  project       = var.project
  location      = var.gcp_region
  repository_id = "sales-data-learning-model-repo"
  dashboard_id  = "sales-data-learning-model-repo"
}

# Dataform
# Note:
# Dataform repository is provisioned via Terraform, but queries, models, and SQLX files inside the repository should be managed separately with Git version control.
# This ensures reproducibility and collaborative development for your ETL logic.
# Destroying the Terraform resource will also delete all queries/models in the Dataform repository.
# Example: Manage your Dataform SQLX files in a separate Git repository and push/pull to Dataform as needed.
