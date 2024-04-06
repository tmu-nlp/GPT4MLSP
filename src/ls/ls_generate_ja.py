import argparse
import csv
import unicodedata

import openai
from ensemble import (
    assign_prediction_scores,
    deduplicate_predictions,
    get_highest_predictions,
)
from tqdm import tqdm


def gpt4_generation(
    APIKEY: str,
    system_content: str,
    input: str,
    deploy_name: str = "gpt-4-turbo-preview",
    max_tokens: int = 768,
    temperature: float = 0.7,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
    use_system_content: bool = True,
):
    openai.api_key = APIKEY

    if use_system_content:
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": input},
        ]
    else:
        print(use_system_content)
        messages = [{"role": "user", "content": input}]

    res = openai.ChatCompletion.create(
        model=deploy_name,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        n=10,
    )

    if res:
        return res["choices"]
    return None


def prompt_f(instruction: str, sentence: str, word: str):
    prompt = f"""
    {instruction}

    Sentence: {sentence}
    Word: {word}
    Alternative sentences: """
    return prompt


def extract_word(sentence, alter_sentence):
    """
    Extract alternative words from the generated sentences
    """
    alter_sentence = alter_sentence.split("**")
    if len(alter_sentence) == 3:
        alter_word = alter_sentence[1]
        return alter_word
    elif len(alter_sentence) == 1 and sentence[0] + sentence[1] == "**":
        # When the target word is at the beginning of a sentence, ** may not be output in the generated sentence.
        alter_word = alter_sentence[0].replace(sentence.split("**")[2], "")
        return alter_word

    return False


def check_format(sentence, word, alter_sentence, alter_word):
    """
    Check whether the non-alternative parts of the generated sentences have not changed.
    """
    if unicodedata.normalize(
        "NFKC", sentence.replace("**", "")
    ) in unicodedata.normalize(
        "NFKC", alter_sentence.replace(alter_word, word).replace("**", "")
    ):
        return True
    return False


if __name__ == "__main__":
    max_number_predictions = 10
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--none_file",
        required=True,
        help="The path of the file which you want to predict",
    )
    parser.add_argument(
        "--predictions_file",
        required=True,
        help="The path of the file which the prediction results will be output",
    )
    parser.add_argument(
        "--idx_start",
        help="The index of the instance for which you want to start predicting",
    )
    parser.add_argument(
        "--idx_end",
        help="The index of the instance for which you want to end predicting",
    )
    parser.add_argument(
        "--api_key",
        required=True,
    )

    args = parser.parse_args()
    APIKEY = args.api_key

    with open(args.none_file) as f:
        reader = csv.reader(f, delimiter="\t")
        contents = [row for row in reader]
    if args.idx_end is not None:
        print("end", args.idx_end)
        contents = contents[: int(args.idx_end)]
    if args.idx_start is not None:
        print("start", args.idx_start)
        contents = contents[int(args.idx_start) :]
    preds = list()

    instruction = "I will give you a Japanese sentence and a word in the 'Sentence' and 'Word' format. Think ten easier alternatives for the Word in the Sentence. Then, output sentences where you have replaced the Word with each alternative enclosed by '**'. \nYou must follow these three rules.\n1. Take into account the meaning of the Word in the Sentence.\n2. Alternatives must be easier to understand than the Word.\n3. Do not generate an explanation."
    print(instruction)

    with open(args.predictions_file, "a") as f_out:
        for now_content in tqdm(contents):
            sentence = now_content[0]
            word = now_content[1]
            # print(word)
            sentence = sentence.replace(word, f"**{word}**", 1)

            prompt = prompt_f(instruction=instruction, sentence=sentence, word=word)
            cnt_try = 0
            cnt_good_format = 0
            aggregated_predictions = list()

            while True:
                outputs = gpt4_generation(
                    APIKEY=APIKEY,
                    system_content="You are a helpful assistant.",
                    input=prompt,
                )

                for output in outputs:
                    output = output["message"]["content"]
                    alter_sentences = output.strip().split("\n")
                    alter_words = list()
                    # print(alter_sentences)
                    for alter_sentence in alter_sentences:
                        alter_word = extract_word(sentence, alter_sentence)
                        if alter_word:
                            if check_format(sentence, word, alter_sentence, alter_word):
                                alter_words.append(alter_word)

                    # print(f'Number of outputs meeting requirements：{len(alter_words)}')
                    if len(alter_words) >= 5:
                        cnt_good_format += 1
                        weighted_predictions = assign_prediction_scores(alter_words)
                        aggregated_predictions.extend(weighted_predictions)

                if cnt_good_format > 5:
                    break
                else:
                    cnt_try += 1
                    # print(sentence, word, cnt_try)
                    # print(alter_sentences)
                    if cnt_try == 5:
                        print("cnt_try is 5... Break")
                        break

            aggregated_predictions = deduplicate_predictions(aggregated_predictions)
            highest_scoring_predictions = get_highest_predictions(
                aggregated_predictions, max_number_predictions
            )

            highest_scoring_predictions.insert(0, sentence.replace("**", ""))
            highest_scoring_predictions.insert(1, word)
            preds.append(highest_scoring_predictions)
            pred = "\t".join(highest_scoring_predictions)
            f_out.write(f"{pred}\n")

    # with open(args.predictions_file, 'w') as f_out:
    #     writer = csv.writer(f_out, delimiter='\t')
    #     writer.writerows(preds)
