ROOT=../..
SRC=$ROOT/src/lcp
LANG=$1
DATA=$2
SPLIT=$3 # split of data file (i.e. test or trial)
NSHOT=$4

MODEL=gpt-4-0613
TEMP=0.7
RS=0
SAVE_DIR=$ROOT/predictions/lcp/$LANG
API_KEY=PLEASE_SET_OPENAI_AIPKEY
FEWSHOT_DATA=$ROOT/data/MLSP_Data/Data/Trial/All/multilex_trial_all_lcp.tsv

mkdir -p $SAVE_DIR

python $SRC/run_lcp.py \
    --model_name $MODEL \
    --api_key $API_KEY \
    --temperature $TEMP \
    --random_state $RS \
    --nshot $NSHOT \
    --split $SPLIT \
    --save_dir $SAVE_DIR \
    --lang $LANG \
    --data_path $DATA \
    --fewshot_data_path $FEWSHOT_DATA 