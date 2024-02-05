import datetime
import os
import zoneinfo

import dotenv

import adapter.Jurassic
import adapter.Openai
import scraper
import util

dotenv.load_dotenv()
SECRET_OPENAI_API_KEY = os.getenv("SECRET_OPENAI_API_KEY")
SECRET_COHERE_API_KEY = os.getenv("SECRET_COHERE_API_KEY")
SECRET_JURASSIC_API_KEY = os.getenv("SECRET_JURASSIC_API_KEY")


models = {}
models["openai"] = {}
models["openai"]["gpt4_turbo"] = "gpt-4-0125-preview"
models["openai"]["gpt4"] = "gpt-4"
models["openai"]["gpt35_turbo"] = "gpt-3.5-turbo-0125"
models["jurassic"] = {}
models["jurassic"]["j2_light"] = "j2-light"
models["jurassic"]["j2_mid"] = "j2-mid"
models["jurassic"]["j2_ultra"] = "j2-ultra"

# Prepare source text
source_text = scraper.scrape_to_json(
    "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/"
)
source_md = util.json_to_md(source_text)
split_md = util.split_md(source_md, 500)

model = models["openai"]["gpt35_turbo"]

calls = adapter.Openai.create_faq(
    api_key=SECRET_OPENAI_API_KEY,
    source_texts=split_md,
    model=model,
)
sum = 0
for call in calls:
    sum += len(call["response"])
print(f"{sum} FAQ erstellt mit {model}.")

model = models["jurassic"]["j2_ultra"]

calls = adapter.Jurassic.create_faq(
    api_key=SECRET_JURASSIC_API_KEY,
    source_texts=split_md,
    model=model,
)
sum = 0
for call in calls:
    sum += len(call["response"])
print(f"{sum} FAQ erstellt mit {model}.")

timestr = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Berlin")).strftime(
    "%Y-%m-%d-%H-%M"
)

# Write calls to file
os.makedirs("output", exist_ok=True)
savepath = os.path.join("output", f"output-{model}-{timestr}.json")
with open(savepath, "w", encoding="utf-8") as f:
    f.write(str(calls))

# write source text to file
savepath = os.path.join("output", f"source-{model}-{timestr}.json")
with open(savepath, "w", encoding="utf-8") as f:
    f.write(str(source_text))
