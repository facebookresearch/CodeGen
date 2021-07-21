model_path=$1
n_layers=$2
obf_proba=$3
model_type=$4
prefix=$5
lr=$6
output_dir=saved_models/${prefix}${model_type}_${obf_proba}_L${n_layers}_LR${lr}/
cd ../code || exit
python run.py \
    --output_dir=$output_dir \
    --model_type=$model_type \
    --model_name_or_path=$model_path \
    --do_train \
    --train_data_file=../dataset_xlm/train.jsonl \
    --eval_data_file=../dataset_xlm/valid.jsonl \
    --test_data_file=../dataset_xlm/test.jsonl \
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
    --model_type=$model_type \
    --model_name_or_path=$model_path \
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
python ../evaluator/evaluator.py -a ../dataset_xlm/test.jsonl  -p ${output_dir}predictions.jsonl