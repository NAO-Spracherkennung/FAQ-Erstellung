import requests
import fitz
import tempfile
import os
from bs4 import BeautifulSoup
import hashlib
from io import BytesIO


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


def save_pdf(content, target_label):
    os.makedirs("pdf", exist_ok=True)
    path = os.path.join("pdf", f"{target_label}.pdf")
    with open(path, "wb") as file:
        file.write(content)


def hash_pdf(folder_path, label, new_file):
    """
    Checks whether pdf file already exists and compares the old and new pdf files using hash
    Returns True if files are equal
    Returns False if files are not equal or or there was no pdf file yet

    """
    current_directory = os.getcwd()
    full_path = os.path.join(current_directory, folder_path)
    file_path = os.path.join(full_path, label + ".pdf")

    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            h1 = hashlib.sha256(file.read()).hexdigest()
            
        h2 = hashlib.sha256(new_file).hexdigest()
        if h1 == h2:
            return True  
        else:
            return False  
    else:
        return False  
