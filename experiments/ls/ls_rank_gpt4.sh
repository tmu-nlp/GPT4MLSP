ROOT=../..
SRC=$ROOT/src/ls
DATA=$ROOT/data/MLSP_Data/data
SAVE_DIR=$ROOT/predictions/ls

mkdir -p $SAVE_DIR/trial
lang=(English JapaneseCatalan German Spanish Filipino French Italian Portuguese Sinhala)
code=(en ja ca de es fil fr it pt si)
for ix in ${!lang[@]}
do
python $SRC/ls_rank_gpt4.py \
    --predictions_file $SAVE_DIR/trial/mlsp2024_${code[ix]}_trial_pred_vfinal.tsv" \
    --ranking_fil $SAVE_DIR/trial/mlsp2024_${code[ix]}_trial_pred_vfinal_rank_ease.tsv" \
    --top_n 3 \
    --mode "ease" \
    --lang= ${lang[ix]}

python $SRC/ls_rank_gpt4.py \
    --predictions_file $SAVE_DIR/trial/mlsp2024_${code[ix]}_trial_pred_vfinal.tsv \
    --ranking_file $SAVE_DIR/trial/mlsp2024_${code[ix]}_trial_pred_vfinal_rank_similarity.tsv \
    --top_n 3 \
    --mode "similarity" \
    --lang ${lang[ix]}
done
