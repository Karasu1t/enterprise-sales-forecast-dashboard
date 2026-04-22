terraform {
  backend "gcs" {
    # Bucket is supplied at init time (see backend.hcl.example). Do not commit real bucket names.
    prefix = "terraform/state"
  }
}
