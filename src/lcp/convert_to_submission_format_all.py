import argparse
import os

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        type=str,
    )
    parser.add_argument("--file_name", type=str)
    parser.add_argument("--save_dir", type=str)
    parser.add_argument("--save_file_name", type=str)
    args = parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)

    langs = [
        "catalan",
        "english",
        "filipino",
        "french",
        "german",
        "italian",
        "japanese",
        "portuguese",
        "sinhala",
        "spanish",
    ]

    results = {}
    for lang in langs:
        file_path = f"{args.dir}/{lang}/{args.file_name}"
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            results[row["index"]] = {
                x: row[x] for x in ["language", "sentence", "token", "pred"]
            }

    test_df = pd.read_table(
        "/home/hwichan/lcp/src/MLSP_Data/Data/Test/All/multilex_test_all_combined_lcp_unlabelled.tsv",
        names=("index", "language", "sentence", "token"),
    )

    assert len(test_df) == len(
        results
    ), f"Not match lengthes of test_df ({len(test_df)}) and results ({len(results)})"
    predicted_df = pd.DataFrame(
        columns=["index", "language", "sentence", "token", "pred"]
    )
    for _, row in test_df.iterrows():
        language = results[row["index"]]["language"]
        sentence = results[row["index"]]["sentence"]
        token = results[row["index"]]["token"]
        pred = results[row["index"]]["pred"]
        assert type(pred) is float
        predicted_df.loc[len(predicted_df)] = [
            row["index"],
            language,
            sentence,
            token,
            pred,
        ]

    assert list(test_df["index"].values) == list(predicted_df["index"].values)
    assert list(test_df["language"].values) == list(predicted_df["language"].values)
    assert list(test_df["token"].values) == list(predicted_df["token"].values)
    assert list(test_df["sentence"].values) == list(predicted_df["sentence"].values)

    predicted_df.to_csv(
        f"{args.save_dir}/{args.save_file_name}",
        header=False,
        index=False,
        sep="\t",
    )
