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

models = {}
models["openai"] = {}
models["openai"]["gpt4_turbo"] = {
    "name": "gpt-4-0125-preview",
    "max_tokens": 16384,  # Eigentlich 128000. Kann aber teuer werden, deswegen 16384
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

source_text = scraper.scrape_to_json(
    "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/"
)
source_md = util.json_to_md(source_text)

model = models["openai"]["gpt35_turbo"]

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
sum_faq = len(summary[""])
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
