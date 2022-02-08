
# DOBF

Pytorch original implementation of [DOBF: A Deobfuscation Pre-Training Objective for Programming Languages](https://arxiv.org/pdf/2102.07492.pdf)
![Model](https://dl.fbaipublicfiles.com/transcoder/images/schema_deobfuscation.png)

## Release

### Pre-trained Models 

We provide DOBF models with the same architecture and BPE model as codeBERT and graphCodeBERT and RoBERTa (to be comparable on downstream tasks).

- [MLM](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/mlm_roberta_size.pth)
- [DOBF init scratch](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/dobf_init_scratch.pth)
- [DOBF model](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/dobf.pth)
- [DOBF+DAE model](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/dobf_plus_denoising.pth)

In command line:
```angular2html
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/mlm_roberta_size.pth
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/dobf_init_scratch.pth
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/dobf.pth
wget https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/dobf_plus_denoising.pth
```

You can use this script on a file containing source code to obfuscate all its identifiers and then deobfuscate them
```
python -m codegen_sources.model.deobfuscate --lang python  --model_path <model_path> --beam_size 1 < my_python_file.py
```




## Training

### Dataset
#### Overview
The data you need:
- Monolingual dataset for MLM ([see](transcoder.md#overview))
- Obfuscation dataset for DOBF
- Monolingual functions and parallel validation and test sets for TransCoder ([see](transcoder.md#overview))

#### Get Obfuscation Dataset

To get the obfuscation data for DOBF:
```
python -m codegen_sources.preprocessing.preprocess 
<DATASET_PATH>                                                          # folder containing raw data i.e json.gz
--langs java python                                                     # languages to prepocess
--mode obfuscation                                                      # dataset mode
--local True                                                            # Run on your local machine if True. If False run on a cluster (requires submitit setup)
--bpe_mode fast_bpe
--fastbpe_code_path <BPE_PATH>                                          # This can either be the bpe codes we provide in data/bpe/cpp-java-python/codes or codes learnt from monolingual dataset mode
--train_splits NGPU                                                     # nb of splits for training data - corresponds to the number of GPU you have
```

Note that is your data is small enough to fit on a single GPU, then NGPU=1 and loading this single split on all GPU is the normal thing to do. Note also that if you run you training on multiple machine, each with NGPU GPUS, splitting in NGPU is fine as well. You will just have to precise ``` --split_data_accross_gpu local ``` in your training parameters. In our case, we add 4 machines of 8 GPU each, we set NPU=8 and ``` --split_data_accross_gpu local ```. 

Note that you cannot learn bpe codes on obfuscated data, so you can either use the bpe codes we provide, or learn BPE codes running the monolingual pipeline.

Note that if you can also use roberta_bpe instead of fast_bpe. The bpe of roberta doesn't require to learn BPE codes.


### Train
#### MLM
Train a MLM Model:
Train a MLM Model:
```
python train.py 

## main parameters
--exp_name mlm \
--dump_path '<YOUR_DUMP_PATH>' \ 

## data / objectives
--data_path '<DATA_PATH>' \ 
--split_data_accross_gpu local \
--mlm_steps 'java,python' \
--add_eof_to_stream true \
--word_mask_keep_rand '0.8,0.1,0.1' \
--word_pred '0.15' \


## model
--encoder_only true \
--n_layers 12  \
--emb_dim 768  \
--n_heads 12  \
--lgs 'java-python' \
--max_vocab 64000 \
--gelu_activation true\
--roberta_mode true 

#optimization
--amp 2  \
--fp16 true  \
--batch_size 32 \
--bptt 512 \
--epoch_size 100000 \
--max_epoch 100000 \
--split_data_accross_gpu global \
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.0001,weight_decay=0.01' \
--save_periodic 0 \
--validation_metrics _valid_mlm_ppl \
--stopping_criterion '_valid_mlm_ppl,10' 
```

#### DOBF
Then to train with the deobfuscation and denoising auto-encoding objectives on top of it:
```
python train.py 

## main parameters
--exp_name deobfuscation \
--dump_path '<YOUR_DUMP_PATH>' \

## data / objectives
--data_path '<DATA_PATH>' \
--split_data_accross_gpu local \
--do_steps 'python_obfuscated-python_dictionary,java_obfuscated-java_dictionary' \
--obf_proba '0.5' \
--ae_steps 'python_obfuscated,java_obfuscated' \
--mask_length poisson \
--word_shuffle 3  \
--word_dropout '0.1' \
--word_blank '0.3' \

## model
--encoder_only False \
--n_layers 0  \
--n_layers_encoder 12  \
--n_layers_decoder 6 \
--emb_dim 768  \
--n_heads 12  \
--lgs 'python_dictionary-python_obfuscated-java_dictionary-java_obfuscated' \
--max_vocab 64000 \
--gelu_activation true \
--roberta_mode true \ 
 
## model reloading
--reload_model '<PATH_TO_MLM_MODEL>,' \
--lgs_mapping 'python_dictionary:python,python_obfuscated:python,java_dictionary:java,java_obfuscated:java' \

## optimization
--amp 2  \
--fp16 true  \
--tokens_per_batch 3000  \
--group_by_size true \
--max_batch_size 128 \
--max_len 2000 \
--epoch_size 50000  \
--max_epoch 10000000  \
--split_data_accross_gpu global \
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.0001,weight_decay=0.01' \
--eval_bleu true \
--eval_subtoken_score true \
--save_periodic 10 \
--validation_metrics 'valid_obf_proba_#obf_proba_mt_subtoken_F1' \
--stopping_criterion 'valid_obf_proba_#obf_proba_mt_subtoken_F1,10'

 ```
 
 Note that if you want to train from DOBF from scratch, set:
 ```
--reload_model ''
```
If you want to train with deobfuscation objective only and not DAE set:
```
--ae_step ''
```
 
#### TransCoder
To train transcoder from a pretrained model (MLM or DOBF - for DOBF [see]):
 
``` 
python train.py   

## main parameters
--exp_name transcoder \
--dump_path '<YOUR_DUMP_PATH>' \ 

## data / objectives
--data_path '<DATA_PATH>' \
--split_data_accross_gpu local \
--bt_steps 'python_sa-java_sa-python_sa,java_sa-python_sa-java_sa'  \
--ae_steps 'python_sa,java_sa'  \
--lambda_ae '0:1,30000:0.1,100000:0'  \ 
--word_shuffle 3  \
--word_dropout '0.1' \ 
--word_blank '0.3'  \

## model  
--encoder_only False \
--n_layers 0  \
--n_layers_encoder 12  \
--n_layers_decoder 6 \
--emb_dim 768  \
--n_heads 12  \
--lgs 'java_sa-python_sa'  \
--max_vocab 64000 \
--gelu_activation true \
--roberta_mode true   \ 

## model reloading
--reload_model '<PATH_TO_DOBF_MODEL>,'  \
--lgs_mapping 'java_sa:java_obfuscated,python_sa:python_obfuscated'  \

## optimization
--amp 2  \
--fp16 true  \
--tokens_per_batch 3000  \
--group_by_size true \
--max_batch_size 128 \
--epoch_size 50000  \
--max_epoch 10000000  \
--split_data_accross_gpu global \
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.0001,weight_decay=0.01' \
--eval_bleu true \
--eval_computation true \
--has_sentence_ids "valid|para,test|para" \
--generate_hypothesis true \
--save_periodic 1 \
--validation_metrics 'valid_python_sa-java_sa_mt_comp_acc'  
```

### Train in multi GPU
To train a model in multi GPU replace `python train.py` with:

```
export NGPU=2; python -m torch.distributed.launch --nproc_per_node=$NGPU train.py
```

### Evaluate on CodeXGLUE
We evaluated each of our models and each baselines with the learning rates 5e-6, 1e-5, 2.5e-5, 5e-5 and 1e-4 and selected the best learning rate on the validation set.
We did not include the datasets in this repository. You can download them either by following the instructions on the ReadMe for each task or on the [CodeXGlue repository](https://github.com/microsoft/CodeXGLUE).
To evaluate codeBERT baseline:
- Clone detection
```angular2html
cd CodeXGLUE/Code-Code/Clone-detection-BigCloneBench/code; bash run_baseline_codebert.sh $lr 2>&1 | tee logs/baseline_codebert_lr$lr.log
```
- NL code search
```
cd CodeXGLUE/Text-Code/NL-code-search-Adv/runs; bash run_baseline_codebert.sh $lr 2>&1 | tee logs/baseline_codebert_lr$lr.log`
```
- Python code summarization
```
cd CodeXGLUE/Code-Text/code-to-text/runs; bash run_baseline_codebert.sh $lr 2>&1 | tee logs/baseline_codebert_lr$lr.log
```
- Java code summarization
```
cd CodeXGLUE/Code-Text/code-to-text/code; bash run_baseline_codebert.sh $lr 2>&1 | tee logs/baseline_codebert_lr$lr.log
```

To evaluate the graphCodeBERT baseline, simply replace `run_baseline_codebert.sh` with `run_baseline_graphcodebert.sh`.

To evaluate one of our models, for instance DOBF+DAE:
- Clone detection
```angular2html
cd CodeXGLUE/Code-Code/Clone-detection-BigCloneBench/code; bash run_xlm_general.sh PATH_TO_REPO/pre_trained_models/dobf_plus_denoising.pth 12 05 roberta_java dobf_plus_denoising $lr 2>&1 | tee logs/dobf_plus_denoising_roberta_java_05_12_lr$lr.log
```
- NL code search
```
cd CodeXGLUE/Text-Code/NL-code-search-Adv/runs; bash run_xlm_general.sh PATH_TO_REPO/pre_trained_models/dobf_plus_denoising.pth 12 05 roberta_python dobf_plus_denoising $lr 2>&1 | tee logs/dobf_plus_denoising_roberta_python_05_12_lr$lr.log
```
- Python code summarization
```
cd CodeXGLUE/Code-Text/code-to-text/runs; bash run_xlm_general.sh PATH_TO_REPO/pre_trained_models/dobf_plus_denoising.pth 12 05 roberta_python dobf_plus_denoising $lr 2>&1 | tee logs/dobf_plus_denoising_roberta_python_05_12_lr$lr.log
```
- Java code summarization
```
cd CodeXGLUE/Code-Text/code-to-text/code; bash run_xlm_general.sh PATH_TO_REPO/pre_trained_models/dobf_plus_denoising.pth 12 05 roberta_java dobf_plus_denoising $lr 2>&1 | tee logs/dobf_plus_denoising_roberta_java_05_12_lr$lr.log
```

To evaluate another model, simply replace "dobf_plus_denoising" with the name of another model.

### Run on other downstream tasks
We created the `modeling_xlm.py` and `tokenization_xlm.py` using interfaces similar to those of huggingfaces to make it easy to load our models and train them on downstream tasks.

Here is an example loading a pretrained model `model.pth` and getting the encoding of a code snippet:  
```
from codegen_sources.wrappers.models import ModelPython, ModelConfig
from codegen_sources.wrappers.tokenizer import PythonTokenizer
import torch
model_path = 'model.pth'
config = ModelConfig.from_pretrained(model_path)
encoder = ModelPython.from_pretrained(model_path, config=config) # loading model
tokenizer = PythonTokenizer.from_pretrained(model_path) # loading tokenizer

code = """def factorial(n):
  res = 0
  for i in range(1, n+1):
    res *= i
  return res
"""

tokens = tokenizer.tokenize(factorial)
ids = torch.tensor([tokenizer.convert_tokens_to_ids(tokens)], dtype=torch.long)

encoded_code = encoder(input_ids=ids, attention_mask=ids.ne(1))
```


## References
This repository contains code that was used to train and evaluate DOBF models. Our paper was published on arxiv:

[1] B. Roziere*, M.A. Lachaux*, M. Szafraniec , G. Lample [DOBF: A Deobfuscation Pre-Training Objective for Programming Languages](https://arxiv.org/abs/2102.07492).

\* Equal Contribution

```
@article{roziere2021dobf,
  title={DOBF: A Deobfuscation Pre-Training Objective for Programming Languages},
  author={Roziere, Baptiste and Lachaux, Marie-Anne and Szafraniec, Marc and Lample, Guillaume},
  journal={arXiv preprint arXiv:2102.07492},
  year={2021}
}
```
