import datetime
import os
import zoneinfo

import dotenv

import scraper
import util
from adapter import create_faq

# Load environment variables
dotenv.load_dotenv()
SECRET_OPENAI_API_KEY = os.getenv("SECRET_OPENAI_API_KEY")

# Define models
models = {}
models["openai"] = {}
models["openai"]["gpt4_turbo"] = "gpt-4-0125-preview"
models["openai"]["gpt4"] = "gpt-4"
models["openai"]["gpt35_turbo"] = "gpt-3.5-turbo-0125"

# Prepare source text
source_text = scraper.scrape_to_json(
    "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/"
)
source_md = util.json_to_md(source_text)
split_md = util.split_md(source_md, 500)


model = models["openai"]["gpt35_turbo"]

calls = create_faq(
    api_key=SECRET_OPENAI_API_KEY,
    source_texts=split_md,
    model=model,
)

timestr = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Berlin")).strftime(
    "%Y-%m-%d-%H-%M"
)


# Write calls to file
savepath = os.path.join("output", f"output-{model}-{timestr}.json")
with open(savepath, "w", encoding="utf-8") as f:
    f.write(str(calls))

# write source text to file
savepath = os.path.join("output", f"source-{model}-{timestr}.json")
with open(savepath, "w", encoding="utf-8") as f:
    f.write(str(source_text))
