import requests
from bs4 import BeautifulSoup
import json


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


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    }

    hauptseite = (
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/"
    )

    generalPage = requests.get(hauptseite, headers=headers)
    soupGeneral = BeautifulSoup(generalPage.text, "html.parser")
    main_content = soupGeneral.find("main")
    content_with_tags = main_content.find_all(
        ["h1", "h2", "h3", "h4", "h5", "h6", "p", "a", "link"], string=True
    )

    page = []

    page = build_content(content_with_tags)

    print(page)


if __name__ == "__main__":
    main()
