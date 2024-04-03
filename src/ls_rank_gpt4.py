
import csv
import openai
import argparse
from tqdm import tqdm
from ensemble import assign_prediction_scores, deduplicate_predictions, get_highest_predictions_4ranking

APIKEY = "PLEASE_SET_API_KEY"


def gpt4_generation(
    system_content: str,
    input: str, 
    deploy_name: str = "gpt-4-turbo-preview",
    max_tokens: int = 256,
    temperature: float = 0.7,
    frequency_penalty: float = 0,
    presence_penalty: float = 0,
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


def prompt_f_rank(instruction: str, sentence: str, word: str, alternatives: str):
    prompt = f"""
    {instruction}

    Sentence: {sentence}
    Word: {word}
    Alternatives: {alternatives}
    Sorted Alternatives: """
    return prompt


if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--predictions_file', required=True, help='The path of the file with prediction results')
    parser.add_argument('--ranking_file', required=True, help='The path of the file which the ranking results will be output')
    parser.add_argument('--top_n', default=3, help='The number of alternative words from the top that you want to re-rank for each instance')
    parser.add_argument('--lang', required=True, help='The language which you want to re-rank; for example, "English"')
    parser.add_argument('--mode', choices=["ease", "similarity"], required=True, help='What you rank based on. You can choose "ease" or "similarity".')
    parser.add_argument('--idx_start', help='The index of the instance for which you want to start re-ranking')
    parser.add_argument('--idx_end', help='The index of the instance for which you want to end re-ranking')

    args = parser.parse_args()

    with open(args.predictions_file) as f:
        reader = csv.reader(f, delimiter='\t')
        contents = [row for row in reader]

    if args.idx_end is not None:
        print('end', args.idx_end)
        contents = contents[:int(args.idx_end)]
    if args.idx_start is not None:
        print('start', args.idx_start)
        contents = contents[int(args.idx_start):]

    top_n = int(args.top_n)
    print('top_n', top_n)
    max_number_predictions = top_n
    mode_ranking = args.mode
    rank_preds = list()

    # -------全言語対象---------
    if args.lang == 'English':
        if mode_ranking == 'ease':
            instruction_rank = f"I will give you a sentence, a word and alternatives for the word in the 'Sentence', 'Word' and 'Alternatives' format. Arrange the Alternatives in order of their ease. Do not generate an explanation."
        elif mode_ranking == 'similarity':
            instruction_rank = f"I will give you a sentence, a word and alternatives for the word in the 'Sentence', 'Word' and 'Alternatives' format. Arrange the Alternatives in order of their semantic similarity to the Word, taking into account the meaning of the Words in the Sentence. Do not generate an explanation." # based on similarity
    else:
        if mode_ranking == 'ease':
            instruction_rank = f"I will give you a {args.lang} sentence, a word and alternatives for the word in the 'Sentence', 'Word' and 'Alternatives' format. Arrange the Alternatives in order of their ease. Do not generate an explanation." # based on ease
        elif mode_ranking == 'similarity':
            instruction_rank = f"I will give you a {args.lang} sentence, a word and alternatives for the word in the 'Sentence', 'Word' and 'Alternatives' format. Arrange the Alternatives in order of their semantic similarity to the Word, taking into account the meaning of the Words in the Sentence. Do not generate an explanation." # based on similarity
    print(instruction_rank)

    with open(args.ranking_file, 'a') as f_out:
        for now_content in tqdm(contents):
            sentence = now_content[0]
            word = now_content[1]
            preds_all = now_content[2:]
            preds = preds_all[:top_n]

            prompt_rank = prompt_f_rank(instruction=instruction_rank, sentence=sentence, word=word, alternatives=", ".join(preds))
           
            while True:
                outputs = gpt4_generation(
                    system_content="You are a helpful assistant.",
                    input=prompt_rank,
                )
                if outputs is not None:
                    break

            # ensemble
            aggregated_predictions = list()
            for output in outputs:
                output = output["message"]["content"].replace('、', ',')
                output = output.replace(', ', ',').split(',')
                weighted_predictions = assign_prediction_scores(output)
                aggregated_predictions.extend(weighted_predictions)
            aggregated_predictions = deduplicate_predictions(aggregated_predictions)
            highest_scoring_predictions = get_highest_predictions_4ranking(aggregated_predictions, max_number_predictions, preds)

            highest_scoring_predictions += preds_all[top_n:]
            highest_scoring_predictions.insert(0, sentence)
            highest_scoring_predictions.insert(1, word)
            rank_preds.append(highest_scoring_predictions)
            pred = '\t'.join(highest_scoring_predictions)
            f_out.write(f'{pred}\n')

    # with open(args.rankings_file, 'w') as f_out:
    #     writer = csv.writer(f_out, delimiter='\t')
    #     writer.writerows(rank_preds)