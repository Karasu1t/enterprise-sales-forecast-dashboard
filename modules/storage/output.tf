
output "salesdata" {
  value = google_storage_bucket.salesdata.name
}

output "import_script" {
  value = google_storage_bucket.import_script.name
}
