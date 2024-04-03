import openai
import csv
import argparse
from tqdm import tqdm
from ensemble import assign_prediction_scores, deduplicate_predictions, get_highest_predictions


APIKEY = "PLEASE_SET_API_KEY"

def gpt4_generation(
    system_content: str,
    input: str, 
    deploy_name: str = "gpt-4-turbo-preview",
    max_tokens: int = 256,
    temperature: float = 0.7,
    frequency_penalty: float = 0.5,
    presence_penalty: float = 0.3,
    use_system_content: bool = True,
):
    openai.api_key = APIKEY

    if use_system_content:
        messages = [{"role": "system", "content": system_content}, {"role": "user", "content": input}]
    else:
        print(use_system_content)
        messages = [{"role": "user", "content": input}]
    try:
        res = openai.ChatCompletion.create(
            model=deploy_name,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            n=10
        )
    except:
        print("OPENAI_ERROR")
        return None

    if res:
        return res["choices"]
    return None


def prompt_f(instruction: str, sentence: str, word: str):
    prompt = f"""
    {instruction}

    Sentence: {sentence}
    Word: {word}
    Alternatives: """
    return prompt


if __name__=="__main__":
    max_number_predictions = 10
    parser = argparse.ArgumentParser()

    parser.add_argument('--none_file', required=True, help='The path of the file which you want to predict')
    parser.add_argument('--predictions_file', required=True, help='The path of the file which the prediction results will be output')
    parser.add_argument('--lang', required=True, help='The language which you want to predict; for example, "English"')
    parser.add_argument('--idx_start', help='The index of the instance for which you want to start predicting')
    parser.add_argument('--idx_end', help='The index of the instance for which you want to end predicting')

    args = parser.parse_args()
    
    with open(args.none_file) as f:
        reader = csv.reader(f, delimiter='\t')
        contents = [row for row in reader]
    if args.idx_end is not None:
        print('end', args.idx_end)
        contents = contents[:int(args.idx_end)]
    if args.idx_start is not None:
        print('start', args.idx_start)
        contents = contents[int(args.idx_start):]
    preds = list()

    if args.lang == 'English':
        instruction = f"I will give you a sentence and a word in the 'Sentence' and 'Word' format. List ten alternatives for the Word that are easier to understand, separated by ','. \nYou must follow these four rules.\n1. Take into account the meaning of the Word in the Sentence.\n2. Alternatives must be easier to understand than the Word.\n3. Each alternative consists of one word.\n4. Do not generate an explanation."
    else:
        instruction = f"I will give you a {args.lang} sentence and a word in the 'Sentence' and 'Word' format. List ten alternatives for the Word that are easier to understand, separated by ','. \nYou must follow these four rules.\n1. Take into account the meaning of the Word in the Sentence.\n2. Alternatives must be easier to understand than the Word.\n3. Each alternative consists of one word.\n4. Do not generate an explanation."
    print(instruction)

    with open(args.predictions_file, 'a') as f_out:
        for now_content in tqdm(contents):
            sentence = now_content[0]
            word = now_content[1]
            prompt = prompt_f(instruction=instruction, sentence=sentence, word=word)
            while True:
                outputs = gpt4_generation(
                    system_content="You are a helpful assistant.",
                    input=prompt,
                )
                if outputs is not None:
                    break

            # ensemble
            aggregated_predictions = list()
            for output in outputs:
                output = output["message"]["content"].replace(', ', ',').split(',')
                weighted_predictions = assign_prediction_scores(output)
                aggregated_predictions.extend(weighted_predictions)
            aggregated_predictions = deduplicate_predictions(aggregated_predictions)
            highest_scoring_predictions = get_highest_predictions(aggregated_predictions, max_number_predictions)

            highest_scoring_predictions.insert(0, sentence)
            highest_scoring_predictions.insert(1, word)
            preds.append(highest_scoring_predictions)
            pred = '\t'.join(highest_scoring_predictions)
            f_out.write(f'{pred}\n')

    # with open(args.predictions_file, 'w') as f_out:
    #     writer = csv.writer(f_out, delimiter='\t')
    #     writer.writerows(preds)
