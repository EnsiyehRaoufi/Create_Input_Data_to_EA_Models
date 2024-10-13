Create input files to be used in the Entity-Matchers pipeline (by having the source KG, target KG, and reference alignment files in ttl, xml or nt format). Employing Entity-Matchers you can run experiments of several entity alignment models on your dataset by reporting precision, recall, and F1-score instead of Hit@K as the evaluation metrics.

(Entity-Matchers code: https://github.com/epfl-dlab/entity-matchers)

1. Please put the source KG, target KG, and reference alignment files in the "raw_files" folder. Then,
2. Please fill out the necessary parameters in the Param.py file. Then,
3. Please run the run.sh file (you can run it in the command window using: bash run.sh) 

All the input files to the Entity-matcher's models then will be created in this directory: ./Entity_Matchers_inputs/DATASET_en/
Also a Pickle dictionary for each dataset will be created in the following directory: ./Entity_Matchers_inputs/dictionaries-bert-int which you need to address these dictionaries as arguments when running BERT-INT on a dataset.
