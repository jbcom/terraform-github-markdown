locals {
  table_metadata = {
    for section_data in var.config.sections : section_data["title"] => {
      for idx, table_data in section_data["tables"] : idx => {
        headers = [
          for column_data in table_data["columns"] : column_data["header"]
        ]

        row_count = max([
          for column_data in table_data["columns"] : length(column_data["rows"])
        ]...)
      }
    }
  }

  markdown_document = templatefile("${path.module}/templates/README.md", merge(var.config, {
    table_metadata = local.table_metadata
  }))
}
