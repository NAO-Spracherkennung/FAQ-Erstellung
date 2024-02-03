from dotenv import load_dotenv
import scraper


def formPrompt(source_text):
    return """
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
        """.format(
        source_text=source_text
    )


if __name__ == "__main__":
    source_text = scraper.main(
        "https://www.hwr-berlin.de/studium/studiengaenge/detail/61-informatik/"
    )

    source_md = scraper.json_to_md(source_text)

    splittext = split_md(source_md, 500)

    # write sourcetext to file
    with open("source_text.json", "w") as file:
        file.write(str(source_text))

    # write splittext to file
    with open("split_text.md", "w") as file:
        for i in splittext:
            file.write(i + "####################\n\n")
