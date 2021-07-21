lr=$1
batch_size=16
epochs=2
output_dir=saved_models/baseline_codebert_${lr}_${epochs}_epochs/

python run.py \
    --output_dir=$output_dir \
    --model_type=roberta \
    --config_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --tokenizer_name=roberta-base \
    --do_train \
    --train_data_file=../dataset/train.txt \
    --eval_data_file=../dataset/valid.txt \
    --test_data_file=../dataset/test.txt \
    --epoch $epochs \
    --block_size 400 \
    --train_batch_size $batch_size \
    --eval_batch_size $batch_size \
    --learning_rate $lr \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456 \
    --output_dir $output_dir && \
python run.py \
    --output_dir=$output_dir \
    --model_type=roberta \
    --config_name=microsoft/codebert-base \
    --model_name_or_path=microsoft/codebert-base \
    --tokenizer_name=roberta-base \
    --do_eval \
    --do_test \
    --train_data_file=../dataset/train.txt \
    --eval_data_file=../dataset/valid.txt \
    --test_data_file=../dataset/test.txt \
    --epoch $epochs \
    --block_size 400 \
    --train_batch_size $batch_size \
    --eval_batch_size $batch_size \
    --learning_rate $lr \
    --max_grad_norm 1.0 \
    --evaluate_during_training \
    --seed 123456; \
python ../evaluator/evaluator.py -a ../dataset/test.txt -p ${output_dir}predictions.txt