lr=$1
output_dir=saved_models/baseline_graphcodebert_${lr}/

cd ../code || exit
python run.py \
    --output_dir=$output_dir \
    --model_type=roberta \
    --config_name=microsoft/graphcodebert-base \
    --model_name_or_path=microsoft/graphcodebert-base \
    --tokenizer_name=microsoft/graphcodebert-base \
    --do_train \
    --train_data_file=../dataset/train.jsonl \
    --eval_data_file=../dataset/valid.jsonl \
    --test_data_file=../dataset/test.jsonl \
    --epoch 2 \
    --block_size 256 \
    --train_batch_size 32 \
    --eval_batch_size 64 \
    --learning_rate $lr \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456 && \
  python run.py \
    --output_dir=$output_dir \
    --model_type=roberta \
    --config_name=microsoft/graphcodebert-base \
    --model_name_or_path=microsoft/graphcodebert-base \
    --tokenizer_name=microsoft/graphcodebert-base \
    --do_eval \
    --do_test \
    --train_data_file=../dataset/train.jsonl \
    --eval_data_file=../dataset/valid.jsonl \
    --test_data_file=../dataset/test.jsonl \
    --epoch 2 \
    --block_size 256 \
    --train_batch_size 32 \
    --eval_batch_size 64 \
    --learning_rate $lr \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456 && \
python ../evaluator/evaluator.py -a ../dataset/test.jsonl  -p ${output_dir}predictions.jsonl