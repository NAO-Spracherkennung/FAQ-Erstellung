import datetime
import json
import os
import zoneinfo

import dotenv

import Api
import scraper
import util


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


def create_faq(source_text):
    dotenv.load_dotenv()
    SECRET_OPENAI_API_KEY = os.getenv("SECRET_OPENAI_API_KEY")

    models = {}
    models["openai"] = {}
    models["openai"]["gpt4_turbo"] = {
        "name": "gpt-4-0125-preview",
        "max_tokens": 8192,  # Eigentlich 128000. Ist aber auf einem "normalen" Account auf 8192 beschränkt.
        "max_output_tokens": 4096,
    }
    models["openai"]["gpt4"] = {
        "name": "gpt-4",
        "max_tokens": 8192,
        "max_output_tokens": 4096,
    }
    models["openai"]["gpt35_turbo"] = {
        "name": "gpt-3.5-turbo",
        "max_tokens": 4096,
        "max_output_tokens": 4096,
    }

    source_md = json_to_md(source_text)

    model = models["openai"]["gpt4_turbo"]

    print("==================================")
    print(f"Erstelle FAQs mit {model['name']}")
    summary = Api.create_faq(
        api_key=SECRET_OPENAI_API_KEY,
        source_text=source_md,
        model=model,
    )
    sum_faq = 0
    for message in summary:
        sum_faq += len(message["faq"])
    print("==================================")
    print(f"{sum_faq} FAQs erstellt mit {model['name']}.")

    sum_tokens = 0
    for message in summary:
        sum_tokens += message["used_tokens"]
    print(f"Insgesamt verbrauchte Tokens: {sum_tokens}")

    timestr = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Berlin")).strftime(
        "%Y-%m-%d-%H-%M"
    )

    # Write calls to file
    os.makedirs("output", exist_ok=True)
    savepath = os.path.join("output", f"output-{model['name']}-{timestr}.json")
    with open(savepath, "w") as f:
        f.write(str(json.dumps(summary)))

    # write source text to file
    savepath = os.path.join("output", f"source-{model['name']}-{timestr}.json")
    with open(savepath, "w") as f:
        f.write(str(source_text))

    all_faq = []
    for message in summary:
        all_faq.extend(message["faq"])

    return all_faq


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
