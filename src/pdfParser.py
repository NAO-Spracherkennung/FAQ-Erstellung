import requests
import fitz
import tempfile

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


def extract_text_from_pdf(pdf_file):
    """
    Simplifies the extraction of text from pdf file.
    Returns an array with pdf file content.

    """
    if pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_file)

        pdf_path = temp_file.name

        doc = fitz.open(pdf_path)
        page_count = len(doc)
        text_content = []

        for page_number in range(page_count):
            page = doc[page_number]
            text_content.append(page.get_text())

        doc.close()
        return text_content
    else:
        return None


def main():
    url = "https://www.hwr-berlin.de/fileadmin/portal/Dokumente/HWR-Berlin/Mitteilungsbl%C3%A4tter/2023/Mitteilungsblatt_11-2023_ZHV_Konsoliderte_Fassung_nach_f%C3%BCnfter_%C3%84nderung_RStud-Pr%C3%BCfO_d_e.pdf"
    pdf = download_pdf(url)

    pdf_text_content = extract_text_from_pdf(pdf)

    print(pdf_text_content)


if __name__ == "__main__":
    main()
