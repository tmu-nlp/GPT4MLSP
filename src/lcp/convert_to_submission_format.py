import argparse
import os

import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--result_path",
        type=str,
    )
    parser.add_argument(
        "--base_path",
        type=str,
    )
    parser.add_argument("--save_dir", type=str)
    parser.add_argument("--save_file_name", type=str)
    args = parser.parse_args()

    os.makedirs(args.save_dir, exist_ok=True)
    result_df = pd.read_csv(args.result_path).drop(["all_pred"], axis=1)
    test_df = pd.read_table(
        args.base_path, names=("index", "language", "sentence", "token")
    )

    assert len(test_df) == len(
        result_df
    ), f"Not match lengthes of test_df ({len(test_df)}) and results ({len(result_df)})"
    assert list(test_df["index"].values) == list(result_df["index"].values)
    assert list(test_df["language"].values) == list(result_df["language"].values)
    assert list(test_df["token"].values) == list(result_df["token"].values)
    assert list(test_df["sentence"].values) == list(result_df["sentence"].values)

    result_df.to_csv(
        f"{args.save_dir}/{args.save_file_name}",
        header=False,
        index=False,
        sep="\t",
    )
