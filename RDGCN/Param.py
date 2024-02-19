
#Info about the source, target and reference alignment files
KG_FILES = ["source.nt", "target.nt"] #source and target kg file names
KG_FORMAT = 'nt' #Format of the input file, could be ttl, xml, nt.
ALIGN_FILE = "refDHT.rdf" #Name of the file containing reference alignment
ALIGN_FORMAT = 'xml' #Format of the reference alignment file, could be ttl, xml or nt.

DATASET = 'doremus' #Dataset name should not contain any punctuations

INPUT_DIR = './rdgcn_inputs/'+DATASET+'_en/' #NO NEED to CHANGE
PATH = './raw_files/' #NO NEED to CHANGE

PRETRAINED_TEXT_EMB_MODEL = 'glove.840B.300d.txt' #full name (and directory) of the pre-trained word embedding model
DIM = 300 #dimensions of the entity name's representations
