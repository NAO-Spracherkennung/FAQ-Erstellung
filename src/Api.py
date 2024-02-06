import re
import openai
import tiktoken


def form_chat_prompt_first(source_text):
    """Form chat prompt for LLMs."""
    return f"""
AUFGABE:
Dieser TEXT stammt von der Webseite der Hochschule für Wirtschaft und Recht Berlin.
Erstelle aus diesem TEXT eine von Fragen und Antworten.
Erstelle kurze Fragen und Antworten Antworten.
Erstelle sehr viele Fragen und Antworten, über 30.
Es ist wichtig, dass jede Information aus dem Text in den Fragen und Antworten dabei ist.

Formatiere die Fragen und Antworten in der richtigen Syntax, z.B.:
Q: Was ist Informatik?
A: Informatik beschreibt Kernprozesse, die für das Funktionieren nahezu aller Bereiche des privaten, gesellschaftlichen und beruflichen Lebens entscheidend sind.
Q: Was ist die Bachelorarbeit?
A: Die Bachelorarbeit stellt für den Studierenden die Hauptarbeit und ein Leistungsnachweis an der HWR dar. Sie wird bewertet.

TEXT:
{source_text}
    """.strip()


def form_chat_prompt_followup():
    """Form chat prompt for LLMs."""
    return f"""
Erstelle weitere Fragen und Antworten zu diesem Text.
Beachte, dass die Fragen und Antworten bereits erstellt wurden und du nur weitere hinzufügen sollst.
Die Fragen und Antworten sollen einfach und kurz sein.
Erstelle sehr viele Fragen und Antworten, über 30.

Formatiere die Fragen und Antworten in der richtigen Syntax, z.B.:
Q: Was ist Informatik?
A: Informatik beschreibt Kernprozesse, die für das Funktionieren nahezu aller Bereiche des privaten, gesellschaftlichen und beruflichen Lebens entscheidend sind.
Q: Was ist die Bachelorarbeit?
A: Die Bachelorarbeit stellt für den Studierenden die Hauptarbeit und ein Leistungsnachweis an der HWR dar. Sie wird bewertet.
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


def calculate_tokens(messages, overall_max_tokens: int, output_max_tokens: int):
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

    overall_max_tokens -= int(num_tokens * 1.1)

    if overall_max_tokens < output_max_tokens:
        output_max_tokens = overall_max_tokens

    return num_tokens, output_max_tokens


def create_faq(api_key, source_texts, model):
    """API Adapter for OpenAI's models.
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
                "content": form_chat_prompt_first(source_text),
            }
        ]

        # Count Input Tokens with 10% discount to make up for variations in tokenizers
        num_tokens, max_output_tokens = calculate_tokens(
            messages, model["max_tokens"], model["max_output_tokens"]
        )
        print(f"Input tokens: {num_tokens}")
        print(f"Max Output tokens: {max_output_tokens}")

        # Call API first time
        response = client.chat.completions.create(
            model=model["name"],
            messages=messages,
            max_tokens=max_output_tokens,
        )

        faq = faq_to_list(response.choices[0].message.content)

        # Create Followup Prompt
        messages = [
            {
                "role": "user",
                "content": form_chat_prompt_first(source_text),
            },
            {
                "role": "assistant",
                "content": response.choices[0].message.content,
            },
            {
                "role": "user",
                "content": form_chat_prompt_followup(),
            },
        ]

        # Count Input Tokens with 10% discount to make up for variations in tokenizers
        num_tokens, max_output_tokens = calculate_tokens(
            messages, model["max_tokens"], model["max_output_tokens"]
        )
        print(f"Input tokens: {num_tokens}")
        print(f"Max Output tokens: {max_output_tokens}")

        # Call API first time
        response = client.chat.completions.create(
            model=model["name"],
            messages=messages,
            max_tokens=max_output_tokens,
        )

        faq.extend(faq_to_list(response.choices[0].message.content))

        summary = {
            "input_tokens": num_tokens,
            "output_tokens": response.usage.total_tokens - num_tokens,
            "response": response.choices[0].message.content,
            "faq": faq,
            "source_text": source_text,
        }
        calls.append(summary)

    return calls
