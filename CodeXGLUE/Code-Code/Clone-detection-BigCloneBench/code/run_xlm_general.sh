model_path=$1
n_layers=$2
obf_proba=$3
model_type=$4
prefix=$5
lr=$6

epochs=2
batch_size=16
pretrained_model=$model_path
output_dir=saved_models/${prefix}${model_type}_${obf_proba}_L${n_layers}_LR${lr}_${epochs}_epochs/

python run.py  \
 --model_type=$model_type \
 --model_name_or_path=$pretrained_model \
 --tokenizer_name=$pretrained_model  \
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
 --seed 123456\
 --output_dir $output_dir && \
python run.py \
    --output_dir=$output_dir \
    --model_type=$model_type \
    --model_name_or_path=$pretrained_model  \
    --tokenizer_name=$pretrained_model \
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
    --seed 123456 ; \
python ../evaluator/evaluator.py -a ../dataset/test.txt -p ${output_dir}predictions.txt
