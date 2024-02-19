This gives you the proper input files to the iAlign entity alignment model having the xml/ttl/nt files of source and target KGs together with their reference alignment file.

1. Please put the source KG, target KG, and reference alignment files in the "raw_files" folder. 
I want to clarify that I have transferred the "char_vocab" from the i-Align to this directory because we need to update this character vocabulary if we encounter any new characters in our datasets.
(Link to the i-Align model: https://bitbucket.org/bayudt/i-align/src/master/)
2. Please fill out the necessary parameters in the Param.py file. Then,
3. Please run the run.sh file (you can run it in the command window using: bash run.sh) 

The proper input to the iAlign model would be available in 'iAlign_inputs' folder after running the codes.

You can read the pickle files using read_pkl.py
