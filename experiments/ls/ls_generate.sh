ROOT=../..
SRC=$ROOT/src/ls
DATA=$ROOT/data/MLSP_Data/data
SAVE_DIR=$ROOT/predictions/ls

mkdir -p $SAVE_DIR/trial
lang=(English Catalan German Spanish Filipino French Italian Portuguese Sinhala)
code=(en ca de es fil fr it pt si)
for ix in ${!lang[@]}
do
python $SRC/ls_generate.py \
    --none_file  $DATA/Trial/${lang[ix]}/multilex_trial_${code[ix]}_ls.tsv \
    --predictions_file $SAVE_DIR/trial/mlsp2024_${code[ix]}_trial_pred_vfinal.tsv \
    --lang ${lang[ix]}
done
