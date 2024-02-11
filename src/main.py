import scraper
from Api import create_faq

if __name__ == "__main__":
    source_text = scraper.scrape_to_json(
        "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/"
    )
    faq = create_faq(source_text)
