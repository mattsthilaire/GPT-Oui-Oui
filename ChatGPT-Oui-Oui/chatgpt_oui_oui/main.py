import argparse
import os

import openai


def main(**kwargs):
    """
    Main caller to create question output
    """

    org = os.getenv("OPENAI_ORG_NAME", False)
    api_key = os.getenv("OPENAI_API_KEY", False)

    if org and api_key:
        openai.organization = org
        openai.api_key = api_key

    else:
        raise ValueError(
            "Open AI org or api key missing. Please check env variables.")

    # default prompt for GPT
    prompt = """
    You are a computer assisted French tutor. A user will provide an article or transcription of
    a podcast in French. You are to create 5 multiple choice questions that ask questions about
    the text you receive. The quetions should vary in difficuly. You should ask questions
    that require context information, as well as questions that have simple one or two word answers.

    Each question will have 4 options to choose from: A, B, C, or D. After you list all the questions
    and answer choices, you will provide the answers, along with any less common French vocabulary
    words and their definition in English.
    """

    with open(kwargs["source_file"], "r") as f:
        article_text = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": article_text
            }],
        temperature=0,
        max_tokens=kwargs["max_tokens"]
    )

    questions_text = response["choices"][0]["message"]["content"]

    with open(kwargs["destination_file"], "w") as return_text:
        return_text.write(questions_text)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Generate questions to French Text via GPT")
    parser.add_argument(
        "-f", help="Files that contains the source text and then where to store GPT's response",
        nargs=2,
        dest="files",
        default=["article.txt", "questions.txt"])
    parser.add_argument(
        "-t",
        help="Number of max tokens GPT can generate",
        dest="max_tokens",
        default=8_000,
        type=int)
    args = parser.parse_args()

    main(source_file=args.files[0],
         destination_file=args.files[1],
         max_tokens=args.max_tokens)
