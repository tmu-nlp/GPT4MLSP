from collections import defaultdict
import csv

def assign_prediction_scores(predictions, start_weight: float = 5.0, decrease: float = 0.5):
    # originate from https://github.com/dennlinger/TSAR-2022-Shared-Task/blob/main/context_predictor.py
    """
    The result of   predictions - len(predictions) * decrease   should equal 0.
    :param predictions:
    :param start_weight:
    :param decrease:
    :return:
    """
    weighted_predictions = []
    for idx, prediction in enumerate(predictions):
        weighted_predictions.append((prediction, start_weight - idx * decrease))

    return weighted_predictions


def deduplicate_predictions(predictions):
    # originate from https://github.com/dennlinger/TSAR-2022-Shared-Task/blob/main/context_predictor.py
    """
    Slightly less efficient deduplication method that preserves "ranking order" by appearance.
    :param predictions: List of predictions
    :return: Filtered list of predictions that no longer contains duplicates.
    """
    merged = defaultdict(float)
    for prediction, score in predictions:
        merged[prediction] += score

    return merged


def get_highest_predictions(predictions, number_predictions):
    # originate from https://github.com/dennlinger/TSAR-2022-Shared-Task/blob/main/context_predictor.py
    return [prediction for prediction, _ in sorted(predictions.items(), key=lambda item: item[1], reverse=True)][:number_predictions]


def get_highest_predictions_4ranking(ranked_predictions, number_predictions, predictions):
    new_ranked_predictions = list()
    
    for ranked_prediction, _ in sorted(ranked_predictions.items(), key=lambda item: item[1], reverse=True):
        if ranked_prediction in predictions:
            # Add only words included before ranking
            new_ranked_predictions.append(ranked_prediction)

    for prediction in predictions:
        if prediction not in new_ranked_predictions:
            # Add words that are included before ranking but not included after ranking
            new_ranked_predictions.append(prediction)

    return new_ranked_predictions[:number_predictions]


def load_data(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        contents = [line.strip().split('\t') for line in lines]
        return contents


if __name__=="__main__":
    max_number_predictions = 10
    lang_id = "en"
    pred_files = [
        f"./../predictions/trial/mlsp2024_{lang_id}_trial_pred_vfinal_rank_ease.tsv",
        f"./../predictions/trial/mlsp2024_{lang_id}_trial_pred_vfinal_rank_similarity.tsv",
    ]
    output_file_name = f"./../predictions/trial/mlsp2024_{lang_id}_trial_pred_vfinal_rank_ensemble.tsv"
    pred_datas = [None for _ in range(len(pred_files))]
    pred_ensemble = list()
    for i, pred_file in enumerate(pred_files):
        pred_data = load_data(pred_file)
        pred_datas[i] = pred_data

    for idx in range(len(pred_datas[0])):
        aggregated_predictions = list()
        for pred_data in pred_datas:
            weighted_predictions = assign_prediction_scores(pred_data[idx][2:])
            aggregated_predictions.extend(weighted_predictions)

        aggregated_predictions = deduplicate_predictions(aggregated_predictions)
        highest_scoring_predictions = get_highest_predictions(aggregated_predictions, max_number_predictions)

        highest_scoring_predictions.insert(0, pred_datas[0][idx][0])
        highest_scoring_predictions.insert(1, pred_datas[0][idx][1])
        pred_ensemble.append(highest_scoring_predictions)

    with open(output_file_name, 'w') as f_out:
        for pred in pred_ensemble:
            pred = '\t'.join(pred)
            f_out.write(f'{pred}\n')

    # with open(output_file_name, 'w') as f_out:
    #     writer = csv.writer(f_out, delimiter='\t')
    #     writer.writerows(pred_ensemble)

