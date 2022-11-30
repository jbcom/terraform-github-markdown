# ${title(replace(replace(title, "-", " "), "_", " "))}
%{ if description != null ~}

${description}
%{ endif ~}
%{ for section_data in sections ~}

## ${title(replace(replace(section_data["title"], "-", " "), "_", " "))}
%{ if section_data["description"] != null ~}

${section_data["description"]}
%{ endif ~}
%{ for snippet in section_data["snippets"] ~}

${file(chomp(snippet))}
%{ endfor ~}
%{ for cur_table, table_data in section_data["tables"] ~}
%{ if table_data["title"] != null ~}

### ${title(replace(replace(table_data["title"], "-", " "), "_", " "))}
%{ endif ~}
%{ if table_data["description"] != null ~}

${table_data["description"]}
%{ endif ~}

<table>
<tr>
%{ for table_header in table_metadata[section_data["title"]][cur_table]["headers"] ~}
<th>${title(replace(replace(table_header, "-", " "), "_", " "))}</th>
%{ endfor ~}
</tr>
%{ for cur_row in range(0, table_metadata[section_data["title"]][cur_table]["row_count"]) ~}
<tr>
%{ for column_data in table_data["columns"] ~}
<td>${try(chomp(column_data["rows"][cur_row]), "")}</td>
%{ endfor ~}
</tr>
%{ endfor ~}
</table>
%{ endfor ~}
%{ endfor ~}