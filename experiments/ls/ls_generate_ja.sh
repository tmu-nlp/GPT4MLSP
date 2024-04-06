ROOT=../..
SRC=$ROOT/src/ls
DATA=$ROOT/data/MLSP_Data/Data
SAVE_DIR=$ROOT/predictions/ls
API_KEY=PLEASE_SET_OPENAI_AIPKEY

mkdir -p $SAVE_DIR/test
python $SRC/ls_generate_ja.py \
    --none_file $DATA/Trial/Japanese/multilex_trial_ja_ls.tsv \
    --predictions_file $SAVE_DIR/trial/mlsp2024_ja_trial_pred_vfinlal.tsv \
    --api_key $API_KEY
