variable "docs_dir" {
  type = string

  description = "Docs dir to generate an index for"
}

variable "markdown_files" {
  type = map(map(string))

  description = "Markdown files by directory, file name, and file contents"
}

variable "headings" {
  type = bool

  default = true

  description = "Whether to use headings"
}

variable "wikilinks" {
  type = bool

  default = false

  description = "Whether to use wikilinks format"
}

variable "index_file_template" {
  type = string

  description = "Index file template. Must contain $${index}"
}