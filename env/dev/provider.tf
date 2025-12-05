terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.36.1"
    }
  }
}

provider "google" {
  project     = var.project
  region      = var.gcp_region
  zone        = var.gcp_zone
  credentials = var.credentials != null ? var.credentials : null
}
