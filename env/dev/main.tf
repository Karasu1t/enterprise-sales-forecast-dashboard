# Storage
module "storage" {
  source      = "../../modules/storage"
  id          = local.id
  project     = local.project
  environment = local.environment
}

# Dataform
module "dataform" {
  source          = "../../modules/dataform"
  region          = local.gcp_region
  project         = local.project
  display_name    = local.display_name
  repository_name = local.repository_name
}

# # bq
# module "bq" {
#   source = "../../modules/bq"
#   email  = local.email
# }

# # Artifact Registry
# module "artifactregistry" {
#   source      = "../../modules/artifactregistry"
#   project     = local.project
#   environment = local.environment
#   gcp_region  = local.gcp_region
# }

# # CLoud Composer
# module "composer" {
#   source      = "../../modules/composer"
#   id          = local.id
#   project     = local.project
#   environment = local.environment
#   gcp_region  = local.gcp_region
#   sa          = local.sa
# }
