output "index" {
  value = templatefile(var.index_file_template, {
    index = local.index_data
  })

  description = "Generated index data"
}