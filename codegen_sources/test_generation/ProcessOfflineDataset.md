Process to create offline parallel dataset using unit tests
## Select Java input functions
select_java_inputs.py
```angular2html
python codegen_sources/test_generation/select_java_inputs.py --local False
```
## Create evosuite tests:
Run create_tests.py:
```angular2html
python codegen_sources/test_generation/create_tests.py --local False
```

## compute translations
For instance for the first iteration for C++
```angular2html
python codegen_sources/test_generation/compute_transcoder_translations.py --target_language cpp --model_path /checkpoint/broz/Transcoder_saved_models/TransCoder_model_1.pth --local False
```

## Compute test results
Should be done automatically in compute_transcoder_translations. To run it manually:
``` 
python codegen_sources/test_generation/compute_test_results.py --translations_csv_path <INPUT_PATH> --output_path <OUTPUT_PATH> --target_language python --local False
```
## Select tests
```
python codegen_sources/test_generation/select_successful_tests.py --input_df <path_to_input_folder> --output_folder <path> --langs python cpp 
```

