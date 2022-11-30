data "external" "merge" {
  program = ["python", "${path.module}/bin/generate-index.py"]

  query = {
    docs_dir       = var.docs_dir
    markdown_files = jsonencode(var.markdown_files)
    headings       = var.headings
    wikilinks      = var.wikilinks
  }
}

locals {
  index_data = jsondecode(base64decode(data.external.merge.result["index"]))
}