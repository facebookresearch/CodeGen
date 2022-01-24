This repository is a toolkit to do machine learning for programming languages. It implements tokenization, dataset preprocessing, model training and model evaluation.

We provide reference implementations of the following papers:
- [TransCoder-ST: Leveraging Automated Unit Tests for Unsupervised Code Translation](https://arxiv.org/pdf/2110.06773.pdf) (2021)
- [DOBF: A Deobfuscation Pre-Training Objective for Programming Languages](https://arxiv.org/pdf/2102.07492.pdf) (2021)
- [TransCoder: Unsupervised Translation of Programming Languages](https://arxiv.org/pdf/2006.03511.pdf) (2020)

We also provide pre-trained models for language modeling, translation and deobfuscation.

You can find some documentation for each projects in the docs folder:
- [TransCoder](docs/transcoder.md).
- [DOBF](docs/dobf.md)
- [TransCoder-ST](docs/TransCoder-ST.md)


## Dependencies
Run [install_env.sh](install_env.sh).
We use black code formatter.

## Data
### Source code processors

This repository contains [programming languages processors](codegen_sources/preprocessing/lang_processors/lang_processor.py) for C++, Java and Python. These processors include:
 - tokenization and detokenization
 - obfuscation
 - function extractions 
 
 These processors are based on [TreeSitter](https://tree-sitter.github.io/tree-sitter/) parsers. As these parsers are available in more than 30 programming languages, one can easily create a new programming language processor.

Example of code tokenization:

```python
from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor

java_code = r"""class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!"); 
    }
}"""
java_processor = JavaProcessor(root_folder="<YOUR_TREESITER_FOLDER>")
tokenized_java_code = java_processor.tokenize_code(java_code)
print(tokenized_java_code)
```

### BPE
This repository provides wrappers for [fast BPE](codegen_sources/preprocessing/bpe_modes/fast_bpe_mode.py) and [Roberta BPE](codegen_sources/preprocessing/bpe_modes/roberta_bpe_mode.py) at file level.

### Dataset Preprocessing

This repository contains a [pipeline](codegen_sources/preprocessing/preprocess.py) to create programming languages datasets. Now it supports [four datasets modes](codegen_sources/preprocessing/dataset_modes):
- Monolingual (ex: Java source code) 
- Monolingual Functions (ex: Java functions) 
- Monolingual Obfuscated (ex: Obfuscated Java source code.)
- Monolingual Obfuscated Functions (ex: Obfuscated Java functions)

First, download C++ / Java / Python source code from [Google BigQuery](https://cloud.google.com/blog/products/gcp/github-on-bigquery-analyze-all-the-open-source-code). To run our preprocessing pipeline, you need to donwload the raw source code on your machine in a JSON format. A sample of it is given [here](data/test_dataset).

The pipeline does the following:
- Source code extraction from json (`.json.gz`) and tokenization (`.tok`)
- Train BPE codes and vocab 
- Apply BPE (`.bpe`)
- Binarization (`.pth`)
- Symlink folder with appropriate file names for `.pth` (XLM-syml). To be given as `data_path` argument for training.

To run the pipeline : 

```bash
python -m codegen_sources.preprocessing.preprocess \
<DATA_PATH> \                            # folder containing json.gz
--langs java cpp python  \               # languages to process
--mode monolingual_functions \           # dataset mode
--bpe_mode=fast_bpe \                    # BPE mode. by default it is fast_BPE. can be roberta_bpe
--local=True \                           # Run on your local machine if True. If False run on a cluster (requires submitit setup)
--train_splits=1                         # Number of trainings splits
```
If you give several languages, the BPE codes and vocab will be learned commonly on these languages , so that you will have a common vocabulary to train one model for several languages. If you do not want that, launch the pipeline on every language separatly. [These tests](codegen_sources/preprocessing/tests/pipeline/test_pipeline.py) test the pipeline on different modes. It will give you an overview of the possible options. 

Also, we provide the BPE codes and vocabulary [here](data/bpe/cpp-java-python). These are the codes and vocabulary used for TransCoder and DOBF. They were learned on concatenated C++, Java, and Python data. If you want to use them instead of learning new ones, give the corresponding paths as ```fastbpe_code_path``` and ```fastbpe_vocab_path``` arguments.

In TransCoder and DOBF readmes, we provide the commands to preprocess the respective datasets.


## Model

### Overview
In this repository, we provide [code](codegen_sources/model) to [train](codegen_sources/model/train.py) transformer-based models (code based on [XLM repository](https://github.com/facebookresearch/XLM)). The available training tasks are the following:
- Masked Language Model (MLM)
- Causal Language Model (CLM)
- Supervised Machine translation (MT)
- Classification
- Deobfuscation = DOBF 
- Unsupervised Machine translation = TransCoder (Denoising auto encoding AE + Back Translation BT) 

We [evaluate](codegen_sources/model/src/evaluation/evaluator.py) our models with metrics adapted to each task (e.g. computation accuracy and BLEU score for TransCoder, subtoken score for Deobfuscation).

Also, we provide [wrappers](codegen_sources/wrappers) to fine-tune and evaluate our models on [CodeXGLUE](https://arxiv.org/pdf/2102.04664.pdf) benchmark.


### Download models
You can donwload the following models :
- [MLM](docs/dobf.md#pre-trained-models)
- [TransCoder](docs/transcoder.md#pre-trained-models). Use it to translate some code [here](codegen_sources/model/translate.py).
- [DOBF](docs/dobf.md#pre-trained-models). Use it to deobfuscate some code [here](codegen_sources/model/deobfuscate.py).

### Re train specific models

To have details on how to retrain specific models, please refer to the README specific to each model.
- [TransCoder README](docs/transcoder.md).
- [DOBF README](docs/dobf.md)

## References

### TransCoder model (NeurIPS 2020)

[1] B. Roziere*, M.A. Lachaux*, L. Chanussot, G. Lample [Unsupervised Translation of Programming Languages](https://research.fb.com/wp-content/uploads/2020/11/Unsupervised-Translation-of-Programming-Languages.pdf).

```
@article{roziere2020unsupervised,
  title={Unsupervised translation of programming languages},
  author={Roziere, Baptiste and Lachaux, Marie-Anne and Chanussot, Lowik and Lample, Guillaume},
  journal={Advances in Neural Information Processing Systems},
  volume={33},
  year={2020}
}
```

### DOBF

[2] B. Roziere*, M.A. Lachaux*, M. Szafraniec , G. Lample [DOBF: A Deobfuscation Pre-Training Objective for Programming Languages](https://arxiv.org/abs/2102.07492).

```
@article{roziere2021dobf,
  title={{DOBF}: A Deobfuscation Pre-Training Objective for Programming Languages},
  author={Roziere, Baptiste and Lachaux, Marie-Anne and Szafraniec, Marc and Lample, Guillaume},
  journal={arXiv preprint arXiv:2102.07492},
  year={2021}
}
```

### TransCoder-ST
[3] B. Roziere, J.M. Zhang, F. Charton, M. Harman, G. Synnaeve, G. Lample [Leveraging Automated Unit Tests for Unsupervised Code Translation](https://arxiv.org/pdf/2110.06773.pdf).

```
@article{roziere2021leveraging,
  title={Leveraging Automated Unit Tests for Unsupervised Code Translation},
  author={Roziere, Baptiste and Zhang, Jie M and Charton, Francois and Harman, Mark and Synnaeve, Gabriel and Lample, Guillaume},
  journal={arXiv preprint arXiv:2110.06773},
  year={2021}
}
```

*Equal Contribution

## License
The validation and test parallel datasets from GeeksForGeeks, and the evaluation scripts under [data/transcoder_evaluation_gfg](data/transcoder_evaluation_gfg) are released under the Creative Commons Attribution-ShareAlike 2.0 license. See https://creativecommons.org/licenses/by-sa/2.0/ for more information.

The rest of the `CodeGen` repository is under the MIT license. See [LICENSE](LICENSE) for more details.
