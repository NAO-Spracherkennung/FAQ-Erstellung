import os
import json


def main(filename_start: str, dir):
    # List to hold all accumulated FAQs
    all_faqs = []

    # Iterate over all files in the current directory
    for filename in os.listdir(dir):
        # Check if "output-gpt-3.5-turbo" is in the filename
        if filename_start in filename:
            # Construct the full path to the file
            filepath = os.path.join(dir, filename)

            try:
                # Open and read the file
                with open(filepath, "r") as file:
                    # Parse the JSON content
                    content = json.load(file)

                    # Check if the expected keys exist and accumulate FAQs
                    for faq_list in content:
                        all_faqs.extend(faq_list["faq"])

            except Exception as e:
                print(f"Error reading or parsing {filename}: {e}")

    return all_faqs


def convert_unicode_escape(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = convert_unicode_escape(value)
        return obj
    elif isinstance(obj, list):
        return [convert_unicode_escape(item) for item in obj]
    elif isinstance(obj, str):
        return obj.encode("utf-8").decode("unicode-escape")

    else:
        return obj


if __name__ == "__main__":
    dir = os.path.join(os.path.join("sample"))
    # all_faqs = convert_unicode_escape(main("output-gpt-3.5-turbo", dir))
    all_faqs = main("output-gpt-3.5-turbo", dir)
    with open("all_faqs_gpt-3.5-turbo.json", "w", encoding="utf-8") as file:
        json.dump(all_faqs, file, ensure_ascii=False)

    all_faqs = main("output-gpt-4-2024", dir)
    with open("all_faqs_gpt-4.json", "w", encoding="utf-8") as file:
        json.dump(all_faqs, file, ensure_ascii=False)

    all_faqs = main("output-gpt-4-0125", dir)
    with open("all_faqs_gpt-4-turbo.json", "w", encoding="utf-8") as file:
        json.dump(all_faqs, file, ensure_ascii=False)
