
#Info about the source, target and reference alignment files
KG_FILES = ["source.ttl", "target.ttl"] #source and target kg file names
KG_FORMAT = 'ttl' #Format of the input file, could be ttl, xml, nt.
DATASET = 'doremus' #Dataset name should not contain any punctuations

ALIGN_FILE = "refDHT.rdf" #Name of the file containing reference alignment
ALIGN_FORMAT = 'xml' #Format of the reference alignment file, could be ttl, xml or nt.

#Info about building the dictionary for BERT-INT model
DICT_NAME = 'desc_doremus' #Name of the dictionary that we plan to feed to BERT-INT model
TEST_REF_SIZE = 0.7 #Percentage of the reference alignment to be used for test set
HANDL_BLANK_NODE = 1 		
#0/1, if 0: all blank nodes will be removed from the attribute/relation triple files,
#if 1: the attribute-values of the blank nodes will be added to the entities that have relation with them as head nodes, e.g. 
#<http://data.doremus.org/event/7aba53dc-7968-37a9-a8ab-15d4b949bdad> <http://erlangen-crm.org/current/P10_falls_within> _:n455ce0a2371740d896626c64a0c50cb7b820 and
#_:n455ce0a2371740d896626c64a0c50cb7b820 <http://erlangen-crm.org/current/P1_is_identified_by> "20 ème siècle - 1 ère moitié"
#So, we remove the "_:n455ce0a2371740d896626c64a0c50cb7b820" blank node but we add ""20 ème siècle - 1 ère moitié" to the descriptions of the source entity
#which is http://data.doremus.org/event/7aba53dc-7968-37a9-a8ab-15d4b949bdad in the BERT-INT dictionary file
                           

