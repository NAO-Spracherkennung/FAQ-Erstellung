import scraper
from Api import create_faq
import os
import pdfParser


def main():
    #Add links without a final slash
    website_urls = [
        "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/studieren-am-fachbereich/einschreibung-und-rueckmeldung",
        "https://www.hwr-berlin.de/studium/bewerbung/bewerbung-duales-studium/bewerbung-fb-duales-studium",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/duales-studium-im-profil",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/studieren-am-fachbereich/austauschprogramme",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/studieren-am-fachbereich/studienorganisation",
    ]

    pdf_urls = [
        "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/studieren-am-fachbereich/studienorganisation/",
    ]

    target_labels = [
        "Modulübersicht",
        "Rahmenstudien- und Prüfungsordnung der HWR Berlin",
    ]

    pdf_exist = os.path.isdir("pdf")
    json_exist = os.path.isdir("json")

    """Website"""
    if json_exist:
        for url in website_urls:
            label = scraper.get_last_segment_from_url(url)
            new_text = scraper.scrape_to_json(url)
            compare = scraper.compare_json("json", label, new_text)
            if not compare:
                scraper.save_json(new_text)
                #faq = create_faq(new_text)
    else:
        for url in website_urls:
            source_text = scraper.scrape_to_json(url)
            label = scraper.get_last_segment_from_url(url)
            scraper.save_json(source_text, label)
            faq = create_faq(source_text)

    """Pdf files"""
    pdf_text_content = []

    if pdf_exist:
        for url in pdf_urls:
            for label in target_labels:
                new_files = pdfParser.download_pdfs_with_label(url, label)
                for file in new_files:
                    compare = pdfParser.hash_pdf("pdf", label, file)
                    if not compare:
                        pdfParser.save_pdf(file, label)
                        pdf_text_content.append(
                            pdfParser.extract_text_from_pdf(file, label)
                        )
                    faq = create_faq(pdf_text_content)
    else:
        for url in pdf_urls:
            for label in target_labels:
                pdf_contents = pdfParser.download_pdfs_with_label(url, label)
                for pdf_content in pdf_contents:
                    pdf_text_content.append(
                        pdfParser.extract_text_from_pdf(pdf_content, label)
                    )
        faq = create_faq(pdf_text_content)


if __name__ == "__main__":
    main()
