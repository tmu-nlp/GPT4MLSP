ROOT=../..
SRC=$ROOT/src/ls
DATA=$ROOT/data/MLSP_Data/data
SAVE_DIR=$ROOT/predictions/ls

mkdir -p $SAVE_DIR/test
python $SRC/ls_generate_ja.py \
    --none_file $DATA/Test/Japanese/multilex_test_ja_ls_unlabelled.tsv \
    --predictions_file $SAVE_DIR/test/mlsp2024_ja_test_pred_vfinlal.tsv
