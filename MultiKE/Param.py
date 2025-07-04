
#Info about the source, target and reference alignment files
KG_FILES = ["source.ttl", "target.ttl"] #source and target kg file names
KG_FORMAT = 'ttl' #Format of the input file, could be ttl, xml, nt.
DATASET = 'agrold' #Dataset name should not contain any punctuation
ALIGN_FILE = "same_as.ttl" #Name of the file containing reference alignment
ALIGN_FORMAT = 'ttl' #Format of the reference alignment file, could be ttl, xml or nt.
INPUT_DIR = './multike_inputs/'+DATASET+'/' #Directory to the output of the codes, NO NEED TO CHANGE

#Info about extracting local names of the entities
#We should set proper attributes for assigning those attribute values as entity's local names in KG1 and KG2
KG1_ATTR_URI =   'http://www.w3.org/2004/02/skos/core#altlabel' #for Doremus could be: 'http://erlangen-crm.org/current/P102_has_title'
KG2_ATTR_URI = 'http://www.southgreen.fr/agrold/vocabulary/description' #for Doremus could be: 'http://erlangen-crm.org/current/P102_has_title'
TEST, TRAIN, VAL = 6, 3, 1 #How to split the reference alignment to be used for test, train, and validation sets
