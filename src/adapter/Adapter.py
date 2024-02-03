import re


def form_prompt(source_text):
    """Form prompt for LLMs."""
    return f"""
        TEXT: {source_text}

        AUFGABE:
        Erstelle aus diesem TEXT eine von Fragen und Antworten.
        Erstelle kurze Fragen und Antworten Antworten.
        Es ist wichtig, dass jede Information aus dem Text in den Fragen und Antworten dabei ist.
        Formatiere die Fragen und Antworten in der richtigen SYNTAX.
        
        SYNTAX:
        F1: Was ist Informatik?
        A1: Informatik beschreibt Kernprozesse, die für das Funktionieren nahezu aller Bereiche des privaten, gesellschaftlichen und beruflichen Lebens entscheidend sind.
        F2: <Frage 2>
        A2: <Antwort 2>
        ...
        """


def faq_to_list(faq_string):
    index = 1
    list = []
    while True:
        try:
            question = re.search(f"F{index}:(.*)", faq_string)
            question = question.group(1).strip()
            answer = re.search(f"A{index}:(.*)", faq_string)
            answer = answer.group(1).strip()
            list.append({"question": question, "answer": answer})
            index += 1
        except AttributeError:
            break
    return list


if __name__ == "__main__":
    string = """
SYNTAX:
        F1: Was ist Informatik?
        A1: Informatik beschreibt Kernprozesse, die für das Funktionieren nahezu aller Bereiche des privaten, gesellschaftlichen und beruflichen Lebens entscheidend sind.
        F2: <Frage 2>
        A2: <Antwort 2>
        ..."""
    print(faq_to_list(string))
