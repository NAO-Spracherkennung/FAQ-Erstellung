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


def split_md(markdown, n):
    # Split the markdown string into lines
    lines = markdown.split("\n")

    # Initialize variables to keep track of the current chunk and the list of chunks
    current_chunk = []
    chunks = []

    # Loop through each line in the markdown
    for line in lines:
        # Check if the line is a header or if the current chunk exceeds the limit
        if (
            line.startswith("#")
            and sum(len(l) + 1 for l in current_chunk) + len(line) > n
        ):
            # If there's already content in the current chunk, start a new chunk
            if current_chunk:
                chunks.append("\n".join(current_chunk))
                current_chunk = []

        # Add the current line to the chunk
        current_chunk.append(line)

        # Check if the current line is a header and its length exceeds n, then split immediately
        if line.startswith("#") and len(line) > n:
            chunks.append("\n".join(current_chunk))
            current_chunk = []

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks
