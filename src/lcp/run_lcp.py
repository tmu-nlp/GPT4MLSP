import argparse
import copy
import time
from typing import Any, Dict, List

import openai
import pandas as pd
from geval.meta_eval_summeval import parse_output
from instructions import (
    instruction_for_lcp,
    instruction_for_lcp_with_lang,
    instruction_for_lcp_with_role,
    instruction_for_lcp_with_role_lang,
)
from scipy.stats import kendalltau, pearsonr, spearmanr
from sklearn.metrics import mean_squared_error
from tqdm import tqdm

BEST_INSTRUCTION_PER_LANG = {
    "catalan": "base",
    "english": "base_role",
    "filipino": "base_lang",
    "french": "base_role_lang",
    "german": "base",
    "italian": "base_lang",
    "japanese": "base",
    "portuguese": "base_role",
    "sinhala": "base",
    "spanish": "base_lang",
}


def _geval_for_lcp(
    instruction: str,
    sentence: str,
    token: str,
    model: str,
    lang: str = None,
    api_key: str = None,
    temperature: float = 0.7,
) -> List[str]:
    openai.api_key = api_key
    prompt = instruction.replace("{{sentence}}", sentence).replace("{{token}}", token)
    if lang:
        prompt = prompt.replace("{{lang}}", lang)

    _response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": prompt}],
        temperature=temperature,
        max_tokens=5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        # logprobs=40,
        n=20,
    )
    all_responses = [
        _response["choices"][i]["message"]["content"]
        for i in range(len(_response["choices"]))
    ]
    return all_responses


def geval_for_lcp(
    instruction: str,
    test_df: pd.core.frame.DataFrame,
    complexity_mapper: Dict[Any, Any] = False,
    do_print_pred: bool = False,
    model: str = "gpt-4-0613",
    api_key: str = None,
    time_sleep: float = 2.0,
    do_parse: bool = True,
    temperature: float = 0.7,
    use_easiness: bool = False,
    use_lang: bool = False,
) -> pd.core.frame.DataFrame:

    if "pred" not in test_df:
        test_df["pred"] = ["None" for _ in range(len(test_df))]
        test_df["all_pred"] = ["None" for _ in range(len(test_df))]
    gold_complexities = []
    predicted_complexities = test_df["pred"].values
    predicted_all_complexities = test_df["all_pred"].values

    for i, (_, instance) in tqdm(enumerate(test_df.iterrows()), total=len(test_df)):
        if "complexity" in instance:
            gold_complexity = instance["complexity"]
            gold_complexities.append(gold_complexity)
        if instance["pred"] != "None":
            continue
        sentence = instance["sentence"]
        token = instance["token"]

        try:
            all_responses = _geval_for_lcp(
                instruction=instruction,
                sentence=sentence,
                token=token,
                lang=instance["language"] if use_lang else None,
                model=model,
                api_key=api_key,
                temperature=temperature,
            )
        except Exception as e:
            print("Error occurred")
            print(e)
            test_df["pred"] = predicted_complexities
            test_df["all_pred"] = predicted_all_complexities
            return test_df

        if do_parse:
            all_complexties = [parse_output(res) for res in all_responses]
        else:
            all_complexties = all_responses

        # print(all_complexties)
        predicted_all_complexities[i] = all_complexties
        if complexity_mapper:
            all_complexties = [
                complexity_mapper[x] for x in all_complexties if x in complexity_mapper
            ]

        all_complexties = [x for x in all_complexties if 0.0 <= x <= 1.0]

        if use_easiness:
            all_complexties = [1 - x for x in all_complexties]
            complexity = sum(all_complexties) / len(all_complexties)
        else:
            complexity = sum(all_complexties) / len(all_complexties)
        predicted_complexities[i] = complexity
        if do_print_pred:
            print("Sentence:", sentence)
            print("Token:", token)
            print("Gold:", gold_complexity)
            print("Pred:", complexity)
            print("-----------------------------------------------")
        time.sleep(time_sleep)

    test_df["pred"] = predicted_complexities
    test_df["all_pred"] = predicted_all_complexities
    if len(gold_complexities) > 0:
        print(
            calculate_correlation(
                pred_score=predicted_complexities, human_score=gold_complexities
            )
        )
    return test_df


def calculate_correlation(
    pred_score: List[float], human_score: List[float]
) -> Dict[str, float]:
    assert len(pred_score) == len(human_score)
    corr = {}
    corr["pearson"] = pearsonr(pred_score, human_score)[0]
    corr["spearman"] = spearmanr(pred_score, human_score)[0]
    corr["kendalltau"] = kendalltau(pred_score, human_score)[0]
    corr["mse"] = mean_squared_error(human_score, pred_score)
    return corr


def construct_nshot_instruction(
    n: int, df: pd.core.frame.DataFrame, instruction: str, random_state: int = 0
):
    prompt = copy.deepcopy(instruction)
    df = df.sample(n=n, random_state=random_state)
    demos = []
    for i in range(n):
        sent, token, complexity = (
            df.iloc[i]["sentence"],
            df.iloc[i]["token"],
            df.iloc[i]["complexity"],
        )
        demos.append(sent)
        prompt = (
            prompt.replace("{{sentence}}", sent).replace("{{token}}", token).strip()
        )
        prompt += f" {str(round(complexity, 3)).strip()}"
        prompt += """

Sentence: '{{sentence}}'

Word: '{{token}}'

Complexity:
"""

    return prompt, demos


def run(
    test_df: pd.core.frame.DataFrame,
    fewshot_df: pd.core.frame.DataFrame,
    instruction_name: str,
    model: str = "gpt-4-0613",
    api_key: str = None,
    time_sleep: float = 1.0,
    temperature: float = 0.7,
    random_state: int = 0,
    nshot: int = 0,
) -> pd.core.frame.DataFrame:
    INSTRUCTION_MAPPER = {
        "base": instruction_for_lcp,
        "base_lang": instruction_for_lcp_with_lang,
        "base_role": instruction_for_lcp_with_role,
        "base_role_lang": instruction_for_lcp_with_role_lang,
    }
    instruction = INSTRUCTION_MAPPER[instruction_name]
    lang = test_df["language"].values[0]
    use_lang = False
    if "lang" in instruction_name:
        use_lang = True

    if nshot > 0:
        lang_fewshot_df = fewshot_df[fewshot_df["language"] == lang]
        instruction, demos = construct_nshot_instruction(
            n=nshot,
            df=copy.deepcopy(lang_fewshot_df),
            instruction=copy.deepcopy(instruction),
            random_state=random_state,
        )

    print(f"Evaluation on {lang}")
    print("Hyperparameters")
    print("instruction_name:", instruction_name)
    print("temperature:", temperature)
    print("nshot:", nshot)
    print()
    print("Instruction")
    print(instruction)
    print()
    predicted_test_df = geval_for_lcp(
        instruction=instruction,
        test_df=copy.deepcopy(test_df),
        complexity_mapper=None,
        do_print_pred=False,
        model=model,
        api_key=api_key,
        time_sleep=time_sleep,
        do_parse=True,
        temperature=temperature,
        use_lang=use_lang,
    )

    while "None" in predicted_test_df["pred"].values:
        predicted_test_df = geval_for_lcp(
            instruction=instruction,
            test_df=copy.deepcopy(predicted_test_df),
            complexity_mapper=None,
            do_print_pred=False,
            model=model,
            api_key=api_key,
            time_sleep=time_sleep,
            do_parse=True,
            temperature=temperature,
            use_lang=use_lang,
        )

    if "complexity" in predicted_test_df:
        print(
            calculate_correlation(
                pred_score=predicted_test_df["pred"].values,
                human_score=predicted_test_df["complexity"].values,
            )
        )
    return predicted_test_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_name",
        type=str,
        default="gpt-4-0613",
    )
    parser.add_argument("--api_key", type=str)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--random_state", type=int, default=0)
    parser.add_argument("--nshot", type=int, default=0)
    parser.add_argument("--split", type=str)
    parser.add_argument("--save_dir", type=str)
    parser.add_argument("--lang", type=str)
    parser.add_argument("--data_path", type=str)
    parser.add_argument("--fewshot_data_path", type=str)
    args = parser.parse_args()

    save_path = f"{args.save_dir}/{args.model_name}.{args.split}.{args.temperature}.{args.nshot}-shot.csv"

    if args.split == "test":
        test_df = pd.read_table(
            args.data_path, names=("index", "language", "sentence", "token")
        )
    else:
        test_df = pd.read_table(
            args.data_path,
            names=("index", "language", "sentence", "token", "complexity"),
        )

    fewshot_df = pd.read_table(
        args.fewshot_data_path,
        names=("index", "language", "sentence", "token", "complexity"),
    )
    results = run(
        test_df=test_df,
        fewshot_df=fewshot_df,
        instruction_name=BEST_INSTRUCTION_PER_LANG[args.lang],
        model=args.model_name,
        api_key=args.api_key,
        time_sleep=1.0,
        temperature=args.temperature,
        random_state=args.random_state,
        nshot=args.nshot,
    )
    results.to_csv(save_path, index=False)
