import re
import time
import openai
import tiktoken


def form_chat_prompt_first(source_text):
    """Form chat prompt for LLMs to create Q&A based on provided text."""
    return f"""
AUFGABE:
Basierend auf dem folgenden TEXT von der Webseite der Hochschule für Wirtschaft und Recht Berlin, erstelle eine umfangreiche Liste von Fragen und Antworten.
Ziel ist es präzise und kurze Fragen und Antworten zu formulieren, die jede Information aus dem Text abdecken.
Stelle sicher, dass die Antworten direkt und eindeutig aus dem Text abgeleitet werden können.

Beispiel für das Format:
Q: Was ist Informatik?
A: Informatik ist das Studium der automatisierten Datenverarbeitung und umfasst die Entwicklung von Software und Systemen.

TEXT:
{source_text}
    """.strip()


def form_chat_prompt_followup():
    """Form chat prompt for LLMs to expand existing Q&A list with new content."""
    return f"""
Basierend auf dem bereits diskutierten Text, erstelle zusätzliche Fragen und Antworten.
Überprüfe die bisher erstellten Inhalte, um Wiederholungen zu vermeiden und sicherzustellen, dass alle Aspekte des Textes abgedeckt sind.
Die neuen Fragen und Antworten sollen einfach, kurz und präzise sein.

Beispiel für das Format:
Q: Welche Rolle spielt die Bachelorarbeit im Studium?
A: Die Bachelorarbeit ist ein wesentlicher Bestandteil des Abschlusses und dient als umfassender Leistungsnachweis.

Denke daran, neue Perspektiven oder Informationen hinzuzufügen, die in der ersten Runde möglicherweise übersehen wurden.
""".strip()


def faq_to_list(faq_string):
    faq_list = []

    # Split the string into segments starting with "Q:"
    segments = re.split(r"(Q:)", faq_string)

    # Iterate through the segments, skipping the first one and stepping by 2 to get every "Q:" segment
    for i in range(1, len(segments), 2):
        if i + 1 < len(segments):
            # Combine the "Q:" marker with the following segment to form the full question segment
            question_segment = segments[i] + segments[i + 1]

            # Find the start of the answer marked by "A:"
            answer_start = re.search(r"A:", question_segment)

            if answer_start:
                # Extract the question text, removing "Q:" from the start
                question = question_segment[2 : answer_start.start()].strip()

                # Extract the answer text, starting after "A:"
                answer = question_segment[answer_start.start() + 2 :].strip()

                # Append the question-answer pair to the list
                faq_list.append({"question": question, "answer": answer})

    return faq_list


def calculate_tokens(messages, max_context_tokens: int, max_response_tokens: int):
    """Returns the number of tokens used by a list of messages."""
    encoding = tiktoken.get_encoding("cl100k_base")
    current_context_tokens = 0
    for message in messages:
        current_context_tokens += (
            4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        )
        for key, value in message.items():
            current_context_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                current_context_tokens += (
                    -1
                )  # role is always required and always 1 token
    current_context_tokens += 2  # every reply is primed with <im_start>assistant

    available_tokens = int(max_context_tokens - current_context_tokens * 1.1)
    response_tokens = available_tokens

    if available_tokens < 0:
        response_tokens = 0

    if available_tokens > max_response_tokens:
        response_tokens = max_response_tokens

    elif available_tokens < max_response_tokens:
        response_tokens = available_tokens

    return current_context_tokens, response_tokens


def call_api(client: openai.OpenAI, model, messages, max_output_tokens):
    response = None
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_output_tokens,
        )
    except openai.RateLimitError as e:
        while True:
            print("...API Ratenlimit erreicht. Warte 10 Sekunden...")
            time.sleep(10)
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    max_tokens=max_output_tokens,
                )
                break
            except openai.RateLimitError as e:
                continue
    return {"role": "assistant", "content": response.choices[0].message.content}


def create_faq(api_key, source_text, model):
    """API Adapter for OpenAI's models.
    https://platform.openai.com/docs/introduction
    """
    summary = []

    client = openai.OpenAI(api_key=api_key)
    messages = [
        {
            "role": "user",
            "content": form_chat_prompt_first(source_text),
        }
    ]

    index = 1
    print("==================================")
    while (
        calculate_tokens(messages, model["max_tokens"], model["max_output_tokens"])[1]
        > 50
    ):
        # while the output can be larger than 50 tokens, e.g. one long FAQ

        print(f"{index}. Durchlauf:")
        index += 1

        num_tokens, max_output_tokens = calculate_tokens(
            messages, model["max_tokens"], model["max_output_tokens"]
        )
        print(f"Tokens im Kontext: {num_tokens}")
        print(f"Freie Tokens im Kontext: {model['max_tokens'] - num_tokens}")
        print(f"Freie Tokens für Antwort: {max_output_tokens}")

        response_message = call_api(client, model["name"], messages, max_output_tokens)

        messages.extend([response_message])

        print(
            f"Tokens in Antwort: {calculate_tokens([messages[-1]], model['max_tokens'], model['max_output_tokens'])[0]}"
        )

        neue_faq = faq_to_list(messages[-1]["content"])
        print(f"Neue FAQs: {len(neue_faq)}")

        used_tokens = calculate_tokens(
            messages, model["max_tokens"], model["max_output_tokens"]
        )[0]

        messages.extend(
            [
                {
                    "role": "user",
                    "content": form_chat_prompt_followup(),
                },
            ]
        )

        summary.append(
            {
                "faq": neue_faq,
                "used_tokens": used_tokens,
            }
        )

        print("----------------------------------")

    return summary
