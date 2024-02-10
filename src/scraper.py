import requests
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def get_header_level(element):
    """
    Simplifies the extraction of the header level of an HTML header tag.

    Returns 0 if not a header element.
    Returns 1,2,3... equal to the header level

    """
    tag_name = element.name
    header_level = 0

    if tag_name and tag_name.startswith("h"):
        header_level = int(tag_name[1])

    return header_level


def build_content(html_elements):
    """

    Extracts the content from a web page and transforms it into a simple form.
    Returns an array with page content.

    """
    content = []
    prev_header_level = 999

    for element in html_elements:
        if get_header_level(element) != 0:
            break
        content.append(element.get_text(strip=True))

    for element in html_elements:
        header_level = get_header_level(element)
        if header_level <= prev_header_level and header_level > 0:
            if header_level < prev_header_level:
                prev_header_level = header_level
            header = {}
            header["title"] = element.get_text(strip=True)
            header["content"] = build_content(get_children(html_elements, element))
            content.append(header)

    return content


def get_children(html_elements, header_element):
    """

    Simplifies the extraction of the children of an HTML header tag.
    Returns array with header children.

    """

    children = []

    main_header_level = get_header_level(header_element)

    record = False

    for element in html_elements:
        if header_element == element:
            record = True
            continue
        if record:
            header_level = get_header_level(element)
            if header_level <= main_header_level and header_level != 0:
                break
            children.append(element)

    return children


def scrape_to_json(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    main_content = soup.find("main")
    content_with_tags = main_content.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "link"], string=True
    )

    page = []
    page = build_content(content_with_tags)

    return page


def get_last_segment_from_url(url):
    """
    Extracts the last section from the URL to be used as a filename later

    """
    parsed_url = urlparse(url)
    path_segments = parsed_url.path.split("/")
    last_segment = path_segments[-1]
    return last_segment


def save_json(text, target_label):
    """
    Saves extracted text as a json file

    """
    os.makedirs("json", exist_ok=True)
    path = os.path.join("json", f"{target_label}.json")
    with open(path, "w", encoding="utf-8") as file:
        json.dump(text, file, ensure_ascii=False, indent=4)


def compare_json(folder_path, label, new_json):
    """
    Checks whether json object already exists and compares the old and new json objects
    Returns True if json objects are equal
    Returns False if json objects are not equal or or there was no json object yet

    """
    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, folder_path)
    file_path = os.path.join(full_path, label + ".json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            existing_json_obj = json.load(file)

        if existing_json_obj == new_json:
            return True
        else:
            return False
    else:
        return False
