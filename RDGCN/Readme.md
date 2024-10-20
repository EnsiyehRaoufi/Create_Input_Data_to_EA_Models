This gives you the proper input files to the RDGCN entity alignment model having the xml/ttl/nt files of source and target KGs together with their reference alignment file.
(Link to the RDGCN model: https://github.com/StephanieWyt/RDGCN)


1. Please put the source KG, target KG, and reference alignment files in the "raw_files" folder. 
2. Please fill out the necessary parameters in the Param.py file. Then,
3. Please run the run.sh file (you can run it in the command window using: bash run.sh) 

The original paper used glove.840B.300d pre-trained English word embedding model (https://nlp.stanford.edu/projects/glove/) to construct the entity name's representations. You can also use "wiki-news-300d-1M.vec" or a pre-trained BERT model such as "bert-base-multilingual-cased" for entity names' embeddings. You should download the language model in this directory and then run the code. 

Generating the Embeddings using a "Nvidia Tesla V100 SXM2 32Go" GPU takes less than 10 minutes for the large AgroLD dataset.
The proper input to the RDGCN model would be available in the 'rdgcn_inputs' folder after running the codes.
You can read the json file that contains the entity name's representations using read_json.py
