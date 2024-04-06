ROOT=../..
SRC=$ROOT/src/ls
DATA=$ROOT/data/MLSP_Data/Data
SAVE_DIR=$ROOT/predictions/ls
API_KEY=PLEASE_SET_OPENAI_AIPKEY

mkdir -p $SAVE_DIR/trial
lang=(English Catalan German Spanish Filipino French Italian Portuguese Sinhala)
code=(en ca de es fil fr it pt si)
for ix in ${!lang[@]}
do
python $SRC/ls_generate.py \
    --none_file  $DATA/Trial/${lang[ix]}/multilex_trial_${code[ix]}_ls.tsv \
    --predictions_file $SAVE_DIR/trial/mlsp2024_${code[ix]}_trial_pred_vfinal.tsv \
    --lang ${lang[ix]} \
    --api_key $API_KEY
done
