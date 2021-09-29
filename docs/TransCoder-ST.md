# Leveraging Automated Unit Tests for Unsupervised Code Translation

![Model](https://dl.fbaipublicfiles.com/transcoder/schemas/unittests_schema.jpg)
This ReadMe gives precise steps to reproduce the results presented in "Leveraging Automated Unit Tests for Unsupervised Code Translation".

## Create self-training dataset
The scripts creating the offline and online data for self-training are in 
[test_generation](../codegen_sources/test_generation).

First, follow the instructions of the CodeGen repository to create a function-level monolingual dataset for java:
- Follow the [BigQuery instructions](googlebigquery.md) and download raw java data
- run `preprocess.py`
```bash
python -m codegen_sources.preprocessing.preprocess 
<DATASET_PATH>                                      # folder containing raw data i.e json.gz
--langs java                                        # languages to prepocess
--mode=monolingual_functions                        # dataset mode
--local=False                                       # Run on your local machine if True. If False run on a cluster (requires submitit setup)
--bpe_mode=fast_bpe 
--train_splits=NGPU                                 # nb of splits for training data - corresponds to the number of GPU you have
```

Then download the TransCoder and DOBF models that they made available and run `create_self_training_dataset.sh` to create the online and offline self-training datasets (from the root of this repository):
```bash
JAVA_FUNC_DATASET=<PATH_TO_THE_JAVA_DATASET>
MODELS_PATH=<PATH_TO_YOUR_MODELS>
OUTPUT_DIRECTORY=<OUTPUT_PATH>
# Download models
cd $MODELS_PATH
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/translator_transcoder_size_from_DOBF.pth
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/TransCoder_model_1.pth 

# Create data (it will take a while)
bash codegen_sources/test_generation/create_self_training_dataset.sh $JAVA_FUNC_DATASET $MODELS_PATH $OUTPUT_DIRECTORY
```

Your files for online training will be created in `${OUTPUT_DIRECTORY}/online_ST_files/`.

## Train a model
```bash
ONLINE_ST_FILES=${OUTPUT_DIRECTORY}/online_ST_files/
DUMP_PATH=<DUMP_PATH>
MODEL_TO_RELOAD='${MODELS_PATH}/TransCoder_model_1.pth'
python codegen_sources/model/train.py \
## General parameters
--dump_path $DUMP_PATH \
--exp_name online_st \
--data_path $ONLINE_ST_FILES \
--unit_tests_path "${ONLINE_ST_FILES}/translated_tests.json"

## Model parameter 
--encoder_only false \
--n_layers 0 \
--n_layers_decoder 6 \
--n_layers_encoder 6 \
--emb_dim 1024 \
--n_heads 8 \
--dropout '0.1' \
--lgs 'cpp_sa-java_sa-python_sa' \
--max_vocab 64000 \
--max_len 512 \
--reload_model '${MODEL_TO_RELOAD},${MODEL_TO_RELOAD}' \

## Optimization parameters
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.00003,weight_decay=0.01' \
--amp 2 \
--fp16 true \
--max_batch_size 128 \
--tokens_per_batch 4000 \
--epoch_size 2500 \
--max_epoch 10000000 \
--clip_grad_norm 1 \
--stopping_criterion 'valid_java_sa-python_sa_mt_comp_acc,25' \
--validation_metrics 'valid_java_sa-python_sa_mt_comp_acc,valid_java_sa-cpp_sa_mt_comp_acc,valid_python_sa-java_sa_mt_comp_acc,valid_python_sa-cpp_sa_mt_comp_acc,valid_cpp_sa-java_sa_mt_comp_acc,valid_cpp_sa-python_sa_mt_comp_acc' \
--has_sentence_ids 'valid|para,test|para,self_training|java_sa' \

## Evaluation parameters
--eval_bleu true \
--eval_computation true \
--generate_hypothesis true \
--eval_st false \
--eval_only false \

## self-training parameters
--st_steps 'java_sa-python_sa|cpp_sa' \
--st_beam_size 20 \
--lambda_st 1 \
--robin_cache false \
--st_sample_size 200 \
--st_limit_tokens_per_batch true \
--st_remove_proba '0.3' \
--st_sample_cache_ratio '0.5' \
--cache_init_path "${ONLINE_ST_FILES}/initial_cache/" \
--cache_warmup 500 
```

# Evaluate pre-trained models
simply replace the variable`MODEL_TO_RELOAD` with the path to your model in the command above and add `--eval_only True`.
Here are the best checkpoints for each direction:

CPP -> Java: [Online_ST_CPP_Java.pth](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/online_st_models/Online_ST_CPP_Java.pth)

CPP -> Python: [Online_ST_CPP_Python.pth](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/online_st_models/Online_ST_CPP_Python.pth)

Java -> CPP: [Online_ST_Java_CPP.pth](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/online_st_models/Online_ST_Java_CPP.pth)

Java -> Python: [Online_ST_Java_Python.pth](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/online_st_models/Online_ST_Java_Python.pth)

Python -> CPP: [Online_ST_Python_CPP.pth](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/online_st_models/Online_ST_Python_CPP.pth)

Python -> Java: [Online_ST_Python_Java.pth](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/online_st_models/Online_ST_Python_Java.pth)

