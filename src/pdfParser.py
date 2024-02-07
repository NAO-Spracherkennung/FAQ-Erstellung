import requests
import fitz
import tempfile
import os
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def download_pdf(url):
    """
    Send get request to download the pdf file

    Return response content if download was success
    Otherwise returns none

    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        return None


def download_pdfs_with_label(url, target_label):
    """
    Extracts the content from a pdf file.
    Returns an array with page content.

    """
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    main_tag = soup.find("main")

    if main_tag:
        all_a_tags = main_tag.find_all("a", href=True)

        pdf_links = [
            a["href"]
            for a in all_a_tags
            if a["href"].endswith(".pdf") and a.text.strip() == target_label
        ]

        pdf_contents = []

        for pdf_link in pdf_links:
            link_http = "http://www.hwr-berlin.de" + pdf_link
            pdf_content = download_pdf(link_http)
            if pdf_content:
                os.makedirs("data", exist_ok=True)
                path = os.path.join("data", f"{target_label}.pdf")
                with open(path, "wb") as file:
                    file.write(pdf_content)
                pdf_contents.append(pdf_content)

        return pdf_contents
    else:
        print("Der <main>-Tag wurde nicht gefunden.")
        return None


def extract_text_from_pdf(pdf_file, target_label):
    """
    Simplifies the extraction of text from pdf file.
    Returns an array with pdf file content.

    """
    if pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_file)

        pdf_path = temp_file.name

        with fitz.open(pdf_path) as doc:
            page_count = len(doc)
            text_content = []

            for page_number in range(page_count):
                page = doc[page_number]
                text_content.append(page.get_text())
                content = build_content(text_content, target_label)
        return content
    else:
        return None


def build_content(pdfcontent, filename):
    """
    Transform pdf content into a simple form
    Returns an array with page content
    """
    content = {}

    content["title"] = filename
    content["content"] = pdfcontent

    return content


def pdf_parser(urls, target_labels):

    pdf_text_content = []

    for url in urls:
        for target_label in target_labels:
            pdf_contents = download_pdfs_with_label(url, target_label)
            for pdf_content in pdf_contents:
                pdf_text_content.append(
                    extract_text_from_pdf(pdf_content, target_label)
                )
    return pdf_text_content


def main():
    urls = [
        "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/studieren-am-fachbereich/studienorganisation/",
    ]

    target_labels = [
        "Modulübersicht",
        "Rahmenstudien- und Prüfungsordnung der HWR Berlin",
    ]
    content = pdf_parser(urls, target_labels)
    print(content)


if __name__ == "__main__":
    main()
