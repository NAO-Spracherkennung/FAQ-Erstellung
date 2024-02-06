import datetime
import json
import os
import zoneinfo

import dotenv

import Api
import scraper
import util

dotenv.load_dotenv()
SECRET_OPENAI_API_KEY = os.getenv("SECRET_OPENAI_API_KEY")
SECRET_JURASSIC_API_KEY = os.getenv("SECRET_JURASSIC_API_KEY")


models = {}
models["openai"] = {}
models["openai"]["gpt4_turbo"] = {
    "name": "gpt-4-0125-preview",
    "max_tokens": 128000,
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

# Prepare source text
source_text = scraper.scrape_to_json(
    "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/"
)
source_md = util.json_to_md(source_text)
split_md = util.split_md(source_md, 500)

model = models["openai"]["gpt35_turbo"]

calls = Api.create_faq(
    api_key=SECRET_OPENAI_API_KEY,
    # source_texts=split_md,
    source_texts=[source_md],
    model=model,
)
sum = 0
for call in calls:
    sum += len(call["faq"])
print(f"{sum} FAQs erstellt mit {model}.")

timestr = datetime.datetime.now(tz=zoneinfo.ZoneInfo("Europe/Berlin")).strftime(
    "%Y-%m-%d-%H-%M"
)

# Write calls to file
os.makedirs("output", exist_ok=True)
savepath = os.path.join("output", f"output-{model['name']}-{timestr}.json")
with open(savepath, "w") as f:
    f.write(str(json.dumps(calls)))

# write source text to file
savepath = os.path.join("output", f"source-{model['name']}-{timestr}.json")
with open(savepath, "w") as f:
    f.write(str(source_text))
