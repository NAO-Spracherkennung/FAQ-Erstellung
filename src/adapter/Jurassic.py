from ai21 import AI21Client
import requests

from .Adapter import form_completion_prompt, faq_to_list


def num_tokens_from_messages(prompt, max_tokens, api_key, factor):
    """Returns the number of tokens used by a list of messages."""
    url = "https://api.ai21.com/studio/v1/tokenize"

    payload = {"text": prompt}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    response = requests.post(url, json=payload, headers=headers)

    num_tokens = len(response.json()["tokens"])

    max_output_tokens = int(max_tokens - (num_tokens + num_tokens * factor))

    return num_tokens, max_output_tokens


def call_api(max_output_tokens, prompt, api_key, model):
    url = f"https://api.ai21.com/studio/v1/{model}/complete"

    payload = {
        "numResults": 1,
        "maxTokens": max_output_tokens,
        "prompt": prompt,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(url, json=payload, headers=headers)

    # Call API
    url = f"https://api.ai21.com/studio/v1/{model}/complete"

    payload = {
        "numResults": 1,
        "maxTokens": max_output_tokens,
        "prompt": prompt,
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.json()["completions"][0]["data"]["text"]


def create_faq(api_key, source_texts, model, max_tokens=2048):
    """API Adapter for GooseAI's models.
    They each have a max token size of 2048.
    https://platform.openai.com/docs/introduction
    """
    if model == "j2-light":
        max_tokens = 2048
    elif model == "j2-mid":
        max_tokens = 8152
    elif model == "j2-ultra":
        max_tokens = 8152

    calls = []

    for source_text in source_texts:
        prompt = form_completion_prompt(source_text)

        num_tokens, max_output_tokens = num_tokens_from_messages(
            prompt, max_tokens, api_key, factor=0.1
        )

        response_text = call_api(max_output_tokens, prompt, api_key, model)

        faq = faq_to_list(response_text)

        summary = {
            "input_tokens": num_tokens,
            "output_tokens": num_tokens_from_messages(
                response_text, max_tokens, api_key, factor=0.1
            ),
            "response": faq,
            "source_text": source_text,
        }
        calls.append(summary)

    return calls


if __name__ == "__main__":
    pass
