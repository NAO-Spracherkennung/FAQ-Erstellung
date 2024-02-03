import openai
import tiktoken
from dotenv import load_dotenv

import scraper

from .Adapter import form_prompt, faq_to_list


def num_tokens_from_messages(messages):
    """Returns the number of tokens used by a list of messages."""
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = 0
    for message in messages:
        num_tokens += (
            4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        )
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


def create_faq(api_key, source_texts, model, max_tokens=4096):
    """API Adapter for OpenAI's GPT-3.5 Turbo, GPT-4, and GPT-4 Turbo.
    https://platform.openai.com/docs/introduction"""

    # Create OpenAI API client
    client = openai.OpenAI(api_key=api_key)
    calls = []

    for source_text in source_texts:
        # Create Prompt
        prompt = form_prompt(source_text)
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        # Count Input Tokens with 10% discount to make up for variations in tokenizers
        num_tokens = num_tokens_from_messages(messages)
        max_output_tokens = int(max_tokens - (num_tokens + num_tokens * 0.1))

        print("Number of tokens: ", num_tokens)
        print("Max output tokens: ", max_output_tokens)

        # Call API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=1,
            max_tokens=max_output_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )

        faq = faq_to_list(response.choices[0].message.content)

        summary = {
            "input_tokens": num_tokens,
            "output_tokens": response.usage.total_tokens - num_tokens,
            "response": faq,
            "source_text": source_text,
        }
        calls.append(summary)

    return calls


if __name__ == "__main__":
    load_dotenv()

    source_text = scraper.scrape_to_json(
        "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/"
    )

    source_md = scraper.json_to_md(source_text)

    response = create_faq("", source_text, "gpt-4-0125-preview")
    print(response.choices[0].message.content)
