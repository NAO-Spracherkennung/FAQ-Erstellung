import openai
import tiktoken

from .Adapter import faq_to_list, form_chat_prompt


def calculate_tokens(messages, max_tokens, factor):
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

    max_output_tokens = int(max_tokens - (num_tokens + num_tokens * 0.1))
    return num_tokens, max_output_tokens


def create_faq(api_key, source_texts, model, max_tokens=4096):
    """API Adapter for OpenAI's models.
    They each have a max token size of 4096.
    https://platform.openai.com/docs/introduction
    """

    # Create OpenAI API client
    client = openai.OpenAI(api_key=api_key)
    calls = []

    for source_text in source_texts:
        # Create Prompt
        messages = [
            {
                "role": "user",
                "content": form_chat_prompt(source_text),
            }
        ]

        # Count Input Tokens with 10% discount to make up for variations in tokenizers
        num_tokens, max_output_tokens = calculate_tokens(
            messages, max_tokens, factor=0.1
        )

        # Call API
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_output_tokens,
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
