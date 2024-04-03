lang=(English Catalan German Spanish Filipino French Italian Portuguese Sinhala)
code=(en ca de es fil fr it pt si)
for ix in ${!lang[@]}
do
python ./../src/ls_generate.py \
    --none_file="./../tools/MLSP_Data/Data/Trial/${lang[ix]}/multilex_trial_${code[ix]}_ls.tsv" \
    --predictions_file="./../predictions/trial/mlsp2024_${code[ix]}_trial_pred_vfinal.tsv" \
    --lang="${lang[ix]}"
done
