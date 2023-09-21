# TransCoder-IR

Pytorch original implementation of [Code Translation with Compiler Representations](https://arxiv.org/pdf/2207.03578.pdf)

## Release

### Pre-trained Models 

We provide checkpoints for every translation task:
- [cpp to java](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_cpp_java.pth)
- [cpp to rust](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_cpp_rust.pth)
- [cpp to go](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_cpp_go.pth)
- [go to cpp](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_go_cpp.pth)
- [go to java](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_go_java.pth)
- [go to rust](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_go_rust.pth)
- [java to cpp](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_java_cpp.pth)
- [java to go](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_java_go.pth)
- [java to rust](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_java_rust.pth)
- [rust to cpp](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_rust_cpp.pth)
- [rust to go](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_rust_go.pth)
- [rust to java](https://dl.fbaipublicfiles.com/transcoder/pre_trained_models/IR_project/IR_rust_java.pth)

You can use this script to translate a function between any pair of languages in ["cpp", "go", "java", "rust"].
```
python -m codegen_sources.model.translate --src_lang rust --tgt_lang cpp --model_path <model_path> --beam_size 1 < my_rust_func_to_translate.rs
```
## Training

### Dataset
#### Overview
The data you need:
- Monolingual dataset for MLM ([see](transcoder.md#overview))
- Obfuscation dataset for DOBF
- Monolingual functions and parallel validation and test sets for TransCoder ([see](transcoder.md#overview))

#### Compile Code to IR

Each different language needs different tools to be compiled into LLVM Intermediate Representations. These are only needed for training. 
If you want to give it a try, you will need to update `codegen_sources/external_paths.py` with the paths to the following binaries:

- For all languages:
  - [LLVM v13.0.0](https://github.com/llvm/llvm-project/releases/tag/llvmorg-13.0.0-rc2)
- For Java:
  - [JDK](https://docs.oracle.com/cd/E19182-01/820-7851/inst_cli_jdk_javahome_t/)
  - [JLang](https://polyglot-compiler.github.io/JLang/user-manual.html#installation)
  - [LLVM v5.0.1](https://prereleases.llvm.org/5.0.1/) (JLang is only compatible with this version)
- For Go:
  - [Gollvm](https://go.googlesource.com/gollvm/)
- For Rust:
  - [cargo](https://doc.rust-lang.org/cargo/getting-started/installation.html)

#### Get IR Dataset

To get the IR data to train the models:
```
export BPE_PATH="data/cpp-go-java-rust/codes"            # Replace with your own if needed

python -m codegen_sources.preprocessing.preprocess 
<DATASET_PATH>                                    # folder containing raw data i.e json.gz
--langs cpp rust java go                          # languages to prepocess
--mode ir_functions                               # dataset mode
--local True                                      # Run on your local machine if True. If False run on a cluster (requires submitit setup)
--bpe_mode fast
--fastbpe_code_path $BPE_PATH                    # This can either be the bpe codes we provide in data/cpp-go-java-rust/codes or codes learnt from monolingual dataset mode
--train_splits $NGPU                               # nb of splits for training data - corresponds to the number of GPU you have
```

Note that is your data is small enough to fit on a single GPU, then NGPU=1 and loading this single split on all GPU is the normal thing to do. Note also that if you run you training on multiple machine, each with NGPU GPUS, splitting in NGPU is fine as well. You will just have to precise ``` --split_data_accross_gpu local ``` in your training parameters. In our case, we add 4 machines of 8 GPU each, we set NPU=8 and ``` --split_data_accross_gpu local ```.
Note that you cannot learn bpe codes on obfuscated data, so you can either use the bpe codes we provide, or learn BPE codes running the monolingual pipeline.

#### Get Parallel Test and Validation Data
Download the data: [transcoder_test_set.zip](https://dl.fbaipublicfiles.com/transcoder/test_set/TransCoder-IR_eval_data.zip) and add the .pth files to your training data folder. 

### Train
#### MLM, TLM
Pre-train an encoder:
The DATASET_PATH should contain monolingual data at file level (see [transcoder.md](transcoder.md)) and parallel code-IR files. 
```shell
export DUMP_PATH=<PATH_TO_DUMP_LOGS_AND_MODELS>
export DATASET_PATH=<PATH_TO_DATASET_CREATED_ABOVE>
export EXP_NAME=<ARBITRARY_NAME_YOU_CHOOSE_FOR_YOUR_EXPERIMENT>

python codegen_sources/model/train.py
# General
--dump_path '$DUMP_PATH' \
--data_path '$DATASET_PATH' \
--exp_name $EXP_NAME \
--lgs 'java-cpp-rust-go-ir' \

# Objective
--mlm_steps 'java,cpp,rust,go,ir,cpp-ir,java-ir,go-ir,rust-ir' \
--word_pred '0.15' \
--word_mask_keep_rand '0.8,0.1,0.1' \

# Model
--encoder_only false \
--n_layers 0 \
--n_layers_decoder 6 \
--n_layers_encoder 6 \
--emb_dim 1024 \
--bptt 256 \
--n_heads 8 \
--max_vocab 64000 \
--dropout '0.1' \

# Optimization
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.0003,weight_decay=0.01' \
--max_len 2000 \
--max_batch_size 128 \
--tokens_per_batch 2000 \
--clip_grad_norm 1 \
--epoch_size 100000 \
--max_epoch 10000000 \
--batch_size 16 \
--amp 2 \
--fp16 true \

# Validation
--stopping_criterion '_valid_mlm_ppl,50' \
--validation_metrics _valid_mlm_ppl
```

#### Full model training
Then to train with the deobfuscation and denoising auto-encoding objectives on top of it:

```shell
export DUMP_PATH=<PATH_TO_DUMP_LOGS_AND_MODELS>
export DATASET_PATH=<PATH_TO_DATASET_CREATED_ABOVE>
export EXP_NAME=<ARBITRARY_NAME_YOU_CHOOSE_FOR_YOUR_EXPERIMENT>

python codegen_sources/model/train.py \
# General
--dump_path '$DUMP_PATH' \
--data_path '$DATASET_PATH' \
--exp_name $EXP_NAME \
--lgs 'cpp_sa-go_sa-java_sa-rust_sa-ir_sa' \

# Reloading
--reload_model '$MLM_CHECKPOINT,$MLM_CHECKPOINT' \
--lgs_mapping 'cpp_sa:cpp,rust_sa:rust,java_sa:java,go_sa:go,ir_sa:ir' \
--reload_encoder_for_decoder true \


# Optimization
--optimizer 'adam_inverse_sqrt,warmup_updates=10000,lr=0.0003,weight_decay=0.01' \
--batch_size 32 \
--max_batch_size 128 \
--tokens_per_batch 3000 \
--eval_tokens_per_batch 20000 \
--epoch_size 50000 \
--max_epoch 10000000 \
--lambda_mlm 1 \
--lambda_clm 1 \
--lambda_ae '0:1,30000:0.1,100000:0' \
--lambda_mt '0:1,30000:0.1,100000:0' \
--lambda_bt 1 \
--amp 2 \
--fp16 true \

# Training steps
--ae_steps 'cpp_sa,java_sa,go_sa,rust_sa' \
--bt_steps 'cpp_sa-go_sa-cpp_sa,cpp_sa-java_sa-cpp_sa,cpp_sa-rust_sa-cpp_sa,go_sa-cpp_sa-go_sa,go_sa-java_sa-go_sa,go_sa-rust_sa-go_sa,java_sa-cpp_sa-java_sa,java_sa-go_sa-java_sa,java_sa-rust_sa-java_sa,rust_sa-cpp_sa-rust_sa,rust_sa-go_sa-rust_sa,rust_sa-java_sa-rust_sa' \
--tae_steps 'cpp_sa-ir_sa,java_sa-ir_sa,go_sa-ir_sa,rust_sa-ir_sa' \
--mt_steps 'cpp_sa-ir_sa,java_sa-ir_sa,go_sa-ir_sa,rust_sa-ir_sa' \
--word_dropout '0.1' \
--word_blank '0.2' \

# Modelization
--n_layers 6 \
--emb_dim 1024 \
--n_heads 8 \
--dropout '0.1' \
--word_shuffle 5 \
--encoder_only false \
--max_vocab '-1' \
--max_len 2000 \
--bt_max_len 512 \

# Validation
--has_sentence_ids 'valid|cpp_sa-go_sa,valid|cpp_sa-java_sa,valid|cpp_sa-rust_sa,valid|go_sa-java_sa,valid|go_sa-rust_sa,valid|java_sa-rust_sa,test|cpp_sa-go_sa,test|cpp_sa-java_sa,test|cpp_sa-rust_sa,test|go_sa-java_sa,test|go_sa-rust_sa,test|java_sa-rust_sa'\
--stopping_criterion 'valid_java_sa-cpp_sa_mt_comp_acc,30' \
--validation_metrics 'valid_cpp_sa-go_sa_mt_comp_acc,valid_cpp_sa-java_sa_mt_comp_acc,valid_cpp_sa-rust_sa_mt_comp_acc,valid_go_sa-cpp_sa_mt_comp_acc,valid_go_sa-java_sa_mt_comp_acc,valid_go_sa-rust_sa_mt_comp_acc,valid_java_sa-go_sa_mt_comp_acc,valid_java_sa-cpp_sa_mt_comp_acc,valid_java_sa-rust_sa_mt_comp_acc,valid_rust_sa-go_sa_mt_comp_acc,valid_rust_sa-java_sa_mt_comp_acc,valid_rust_sa-cpp_sa_mt_comp_acc' \
--early_stopping true \
--eval_bleu true \
--eval_computation 'go_sa-cpp_sa,java_sa-cpp_sa,rust_sa-cpp_sa,cpp_sa-go_sa,java_sa-go_sa,rust_sa-go_sa,cpp_sa-java_sa,go_sa-java_sa,rust_sa-java_sa,cpp_sa-rust_sa,go_sa-rust_sa,java_sa-rust_sa' \
--generate_hypothesis true \
--translation_eval_set GfG \
--n_sentences_eval 1500 
```

### Train in multi GPU
To train a model in multi GPU replace `python train.py` with:

```
export NGPU=2; python -m torch.distributed.launch --nproc_per_node=$NGPU train.py
```


## References
This repository contains code that was used to train our TransCoder-IR models. Our paper was published on arxiv and accepted at ICLR 2023:

[1] Marc Szafraniec*, Baptiste Rozière*, Hugh Leather, Francois Charton, Patrick Labatut, Gabriel Synnaeve Pytorch original implementation of [Code Translation with Compiler Representations](https://arxiv.org/pdf/2207.03578.pdf).

\* Equal Contribution

```
@article{szafraniec2022code,
  title={Code translation with Compiler Representations},
  author={Szafraniec, Marc and Roziere, Baptiste and Charton, Hugh Leather Francois and Labatut, Patrick and Synnaeve, Gabriel},
  journal={ICLR},
  year={2023}
}
```
