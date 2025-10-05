# Storage
module "storage" {
  source      = "../../modules/storage"
  id          = local.id
  project     = local.project
  environment = local.environment
}

# bq
module "bq" {
  source      = "../../modules/bq"
  id          = local.id
  environment = local.environment
  project     = local.project
  email       = local.email
  email_mas   = local.email_mas
}

# Function
module "function" {
  source         = "../../modules/functions"
  id             = local.id
  project        = local.project
  environment    = local.environment
  gcp_region     = local.gcp_region
  email          = local.email
  dataset        = module.bq.dataset
  source_bucket  = module.storage.import_script
  trigger_bucket = module.storage.salesdata
  script         = "function.zip"
}

# # Artifact Registry
# module "artifactregistry" {
#   source      = "../../modules/artifactregistry"
#   project     = local.project
#   environment = local.environment
#   gcp_region  = local.gcp_region
# }

# Dataform
# Note:
# Dataform repository is provisioned via Terraform, but queries, models, and SQLX files inside the repository should be managed separately with Git version control.
# This ensures reproducibility and collaborative development for your ETL logic.
# Destroying the Terraform resource will also delete all queries/models in the Dataform repository.
# Example: Manage your Dataform SQLX files in a separate Git repository and push/pull to Dataform as needed.
