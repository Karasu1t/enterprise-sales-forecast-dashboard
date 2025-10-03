variable "project" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
}

variable "repository_name" {
  description = "Dataform repository name"
  type        = string
}

variable "display_name" {
  description = "Display name for Dataform repository"
  type        = string
  default     = "Dataform Repository"
}