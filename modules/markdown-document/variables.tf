variable "config" {
  type = object({
    title       = string
    description = optional(string)

    sections = list(object({
      title       = string
      description = optional(string)
      snippets    = optional(list(string), [])

      tables = optional(list(object({
        title       = optional(string)
        description = optional(string)

        columns = list(object({
          header = string
          rows   = list(string)
        }))
      })), [])
    }))
  })

  description = "Markdown document configuration"
}