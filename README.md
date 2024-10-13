# Create Input Files to the Entity Alignment Models from TTL/XML/NT Source and Target KGs
Create proper input files to the Entity Alignment (EA) models using reference alignment file and the turtle/XML/NTriple files of source and target knowledge graphs.
Please note that the inputs have been made so the EA models can be run on a variety of datasets without causing runtime errors.

We pre-process and prepare the proper JSON, PKL, etc. files needed to run the original experiments presented by several EA methods including [BERT-INT](https://github.com/kosugi11037/bert-int), [RDGCN](https://github.com/StephanieWyt/RDGCN), [MultiKE](https://github.com/nju-websoft/MultiKE), and [i-Align](https://bitbucket.org/bayudt/i-align/src/master/). 
Also, having source and target KG and the ground truth files in TTL/XML/NT formats, we prepare the data in the format needed by [Entity-Matchers](https://github.com/epfl-dlab/entity-matchers). Afterward, by employing Entity-Matchers, we can run the EA experiments of several EA methods on our datasets. Please notice that to go toward a more fair evaluation metric, instead of Hit@K, Precision, Recall, and F1-Scores have been reported for the EA models.

Any contributions to providing codes to generate proper inputs for the other entity alignment models are highly welcomed!
