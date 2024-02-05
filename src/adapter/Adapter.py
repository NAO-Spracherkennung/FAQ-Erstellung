import re


def form_chat_prompt(source_text):
    """Form chat prompt for LLMs."""
    return f"""
        AUFGABE:
        Dieser TEXT stammt von der Webseite der Hochschule für Wirtschaft und Recht Berlin.
        Erstelle aus diesem TEXT eine von Fragen und Antworten.
        Erstelle kurze Fragen und Antworten Antworten.
        Erstelle sehr viele Fragen und Antworten, über 30.
        Es ist wichtig, dass jede Information aus dem Text in den Fragen und Antworten dabei ist.
        Formatiere die Fragen und Antworten in der richtigen SYNTAX.
        
        SYNTAX:
        Q: Was ist Informatik?
        A: Informatik beschreibt Kernprozesse, die für das Funktionieren nahezu aller Bereiche des privaten, gesellschaftlichen und beruflichen Lebens entscheidend sind.
        Q: <Frage 2>
        A: <Antwort 2>
        ...
        
        TEXT:
        {source_text}
        """.strip()


def form_completion_prompt(source_text):
    """Formuliere einen Vervollständigungsaufforderung für LLMs zur Generierung mehrerer Frage-Antwort-Paare auf Deutsch."""
    return f"""
        Der folgende Text stammt von der Website der Hochschule für Wirtschaft und Recht Berlin.

        Quelltext:
        {source_text}
        
        Basierend auf dem Kontext des Quelltexts, generiere eine Liste mit mehreren kurzen Fragen und den entsprechenden kurzen Antworten.

        Das ist ein Beispiel für ein FAQ:
        Q: <Frage>
        A: <Antwort>

        Formatiere die FAQ in der richtigen Syntax mit Q und A.
        
        FAQ:
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
