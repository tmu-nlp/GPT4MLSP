# The code for TMU-HIT system submitted to [MLSP Shared Task at BEA 2024](https://sites.google.com/view/mlsp-sharedtask-2024/home)

## How to use

### Environment

- Python version: 3.8.5

### Install libraries
`pip install -r requirements.txt`

### LCP
Please set OpenAI API Key [here](https://github.com/tmu-nlp/MLSP2024/blob/c3fcdcd3a8c5582ce5697301b8b3a937d358ae57/experiments/lcp/run.sh#L12).
```
cd experiments/lcp
bash run.sh [target language (e.g., english, japanese, etc.)] [path to tsv file] [split of the tsv file (i.e. test or trial)] [number of shots (e.g., 0, 3, etc.)]
```
The predictions will be saved under predictions/lcp/[target language].

### LS
#### Substitute Generation
Please set OpenAI API Key [here](https://github.com/tmu-nlp/GPT4MLSP/blob/main/experiments/ls/ls_generate.sh#L5).
```
cd experiments/ls
bash ls_generate.sh
```

For Japanese, Please set OpenAI API Key [here](https://github.com/tmu-nlp/GPT4MLSP/blob/main/experiments/ls/ls_generate_ja.sh#L5).
```
cd experiments/ls
bash ls_generate_ja.sh
```

#### Substitute Ranking
Please set OpenAI API Key [here](https://github.com/tmu-nlp/GPT4MLSP/blob/main/experiments/ls/ls_rank_gpt4.sh#L5).
```
cd experiments/ls
bash ls_rank_gpt4.sh
```
