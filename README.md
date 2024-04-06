# MLSP2024

## How to use

### Environment

- Python version: 3.8.5

### Install libraries
`pip install -r requirements.txt`

### LCP
Please set OpenAI API Key [here](https://github.com/tmu-nlp/MLSP2024/blob/c3fcdcd3a8c5582ce5697301b8b3a937d358ae57/experiments/lcp/run.sh#L12)
```
cd experiments/lcp
bash run.sh [target language (e.x. english, japanese, etc.)] [path to tsv file] [split of the tsv file (i.e. test or trial)] [number of shots (e.x. 0, 3, etc.)]
```
The predictions will be saved under predictions/lcp/[target language].
