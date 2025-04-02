def dict_to_html(d):
    def process_dict(d, level=0):
        html = ""
        indent = "&nbsp;&nbsp;" * level
        for key, value in d.items():
            if isinstance(value, dict):
                html += f"<p>{indent}{key}:</p>"
                html += process_dict(value, level + 1)
            else:
                html += f"<p>{indent}{key}: {value}</p>"
        return html

    html_content = "<div>"
    html_content += process_dict(d)
    html_content += "</div>"
    return html_content

