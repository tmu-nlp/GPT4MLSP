lang=(English JapaneseCatalan German Spanish Filipino French Italian Portuguese Sinhala)
code=(en ja ca de es fil fr it pt si)
for ix in ${!lang[@]}
do
python ./../src/ls_rank_gpt4.py \
    --predictions_file="./../predictions/trial/mlsp2024_${code[ix]}_trial_pred_vfinal.tsv" \
    --ranking_file="./../predictions/trial/mlsp2024_${code[ix]}_trial_pred_vfinal_rank_ease.tsv" \
    --top_n=3 \
    --mode="ease" \
    --lang="${lang[ix]}"

python ./../src/ls_rank_gpt4.py \
    --predictions_file="./../predictions/trial/mlsp2024_${code[ix]}_trial_pred_vfinal.tsv" \
    --ranking_file="./../predictions/trial/mlsp2024_${code[ix]}_trial_pred_vfinal_rank_similarity.tsv" \
    --top_n=3 \
    --mode="similarity" \
    --lang="${lang[ix]}"

done
