data "utils_deep_merge_json" "table_data" {
  input = [
    for table_data in var.tables : jsonencode(table_data)
  ]

  append_list = true

  deep_copy_list = true
}

locals {
  raw_table_data = jsondecode(data.utils_deep_merge_json.table_data.output)

  table_data = {
    for table_name, table_data in local.raw_table_data : table_name => {
      columns = [
        for column_name in distinct(table_data["order"]) : {
          header = column_name
          rows   = table_data["columns"][column_name]
        }
      ]
    }
  }
}
