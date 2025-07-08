"""
Convert Turtle RDF files to N-Triples, filter out blank-node triples,
and generate a same_as alignment file. Reports total runtime.
"""

from rdflib import Graph
from collections import defaultdict
from Param import *
import time
import os

if __name__ == '__main__':
    """Read turtle files and save them in ntriples format. read reference alignment file and
     save the aligned entities in a file named same_as"""
    
    # Record script start time for runtime measurement
    start_time = time.time()
    RAW_FILE_DIR = "./raw_files/"
    OUTPUT_NAMES = [DATASET+"_triples", "en_triples"]
    not_blank_lines = [[],[]]
    
    # Loop over each KG file: parse Turtle → serialize N-Triples → filter blanks
    for i in range(2):
        g = Graph()
        f = RAW_FILE_DIR+KG_FILES[i]
        # Load the file into the RDFLib graph
        g.parse(f, format=KG_FORMAT)
        fname = OUTPUT_NAMES[i]
        # Write out graph in N-Triples format
        g.serialize(destination= RAW_FILE_DIR+fname, format="nt")

        with open(RAW_FILE_DIR+fname, "r") as f:
            for line in f.readlines():
                line = line.rstrip('\n')
                #Remove blank nodes
                #if "_:" not in line:
                # Skip any triple containing a blank-node identifier, convert to lowercase
                not_blank_lines[i].append(line.lower())
        with open(RAW_FILE_DIR+fname, 'w') as f:
            for nb in not_blank_lines[i]:
                f.write(nb+"\n")
                
    # Parse reference alignment file (TTL or XML) into RDFLib graph
    g = Graph()
    g.parse(RAW_FILE_DIR+ALIGN_FILE, format=ALIGN_FORMAT)
    fname = RAW_FILE_DIR+"same_as"
    g.serialize(destination=fname+"_raw", format="nt")

    # Extract owl:sameAs pairs directly from TTL triples
    if ALIGN_FORMAT == 'ttl':
        with open(fname+"_raw", "r") as f:

            f_read_lines = f.readlines()
            pairs_list = []

            for line in f_read_lines:
                h, _, t = line.rstrip('\n').split(' ',2)
                h = h.strip('<>')
                t = t.strip('<>')
                t = t.strip('> .')
                pairs_list.append((t,h))

    # Group blank-node entity1/entity2 URIs to build alignments
    elif ALIGN_FORMAT == 'xml':
        ent_pairs_1 = defaultdict(list)
        ent_pairs_2 = defaultdict(list)
        with open(fname+"_raw", "r") as f:
            for line in f.readlines():
                l = line.rstrip('\n').split(' ',2)
                t = l[-1]
                if t.startswith('<http://') and "alignmententity1" in l[1]:
                    t = t.strip('<>')
                    t = t.strip('> .')
                    ent_pairs_1[l[0]].append(t)
                if t.startswith('<http://') and "alignmententity2" in l[1]:
                    t = t.strip('<>')
                    t = t.strip('> .')
                    ent_pairs_2[l[0]].append(t)
        pairs_list = []
        for ent1 in ent_pairs_1.keys():
            if ent1 in ent_pairs_2.keys():
                for t in ent_pairs_2[ent1]:
                    pairs_list.append((ent_pairs_1[ent1][0], t))
                if len(ent_pairs_2[ent1])>1:
                    print("For {} More than 1 aligned entity existed!".format(ent_pairs_1[ent1]))
                if len(ent_pairs_1[ent1])>1:
                    print("More than 1 member existed in ent_pairs_1 for this entity: ", ent1)

    #print("Number of aligned entities: ", len(pairs_list))
    # Write cleaned same_as URI pairs (lowercased) to output
    with open(fname, 'w') as f:
        for pair in pairs_list:
            f.write(pair[0].lower()+" "+pair[1].lower()+'\n')
    os.remove(fname+"_raw")
    # Print total elapsed time
    print("--- Runtime: %s seconds ---" % (time.time() - start_time))
