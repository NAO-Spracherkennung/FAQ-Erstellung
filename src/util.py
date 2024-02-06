def json_to_md(json, level=0):
    """
    Transforms a JSON object or list into a markdown string.
    Returns a markdown string.
    """
    md = ""
    for item in json:
        if isinstance(item, dict):
            md += f"{'#' * (level + 1)} {item['title']}\n\n"
            md += json_to_md(item["content"], level + 1)
        elif isinstance(item, str):
            md += f"{item}\n\n"
        elif isinstance(item, list):
            md += json_to_md(item, level + 1)

    return md
