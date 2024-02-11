import scraper
from Api import create_faq

def main():
    urls = [
        "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/studieren-am-fachbereich/einschreibung-und-rueckmeldung",
        "https://www.hwr-berlin.de/studium/bewerbung/bewerbung-duales-studium/bewerbung-fb-duales-studium",
        "https://www.hwr-berlin.de/hwr-berlin/fachbereiche-und-bps/fb-2-duales-studium/duales-studium-im-profil"
    ]
    data_exist = os.path.isdir("data")
    json_exist = os.path.isdir("json")
    
    """Website"""
    if json_exist: 
        for url in urls: 
            label = scraper.get_last_segment_from_url(url)
            new_text = scraper.scrape_to_json(url) 
            compare = scraper.compare_json("json", label, new_text)
            print(compare)
            if not compare: 
                #werden weiter fragen erstellt
                faq = create_faq(new_text)
    else:
        for url in urls: 
            source_text = scraper.scrape_to_json(url)
            label = scraper.get_last_segment_from_url(url)
            scraper.save_json(source_text,label)
            faq = create_faq(source_text)


if __name__ == "__main__":
    main()
