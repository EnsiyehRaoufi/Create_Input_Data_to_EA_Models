import sklearn
from sklearn.model_selection import train_test_split
import os
import random
import pickle
import re
from Param import *

import sys
orig_stdout = sys.stdout
f = open('out.txt', 'w')
sys.stdout = f # Redirect standard output to out.txt for logging

# Check if the directory already exists
if not os.path.exists(INPUT_DIR):
    os.makedirs(INPUT_DIR)

PATH_DATA = './raw_files/'+DATASET
PATH = './raw_files/'
def create_att_rel_triples_files(data_path):
    """Creates 4 distinct file (2 for each KG), _att_triples files contain
    attribute triples of the KGs while _rel_triples files contain relation triples.
    """
    # Initialize lists for attribute and relation triples
    att_triples = []
    rel_triples = []
    with open(data_path,"r",encoding="utf-8") as f:
        for line in f:
            l = line.rstrip('\n').split(' ',2)[-1]
            l0 = line.rstrip('\n').split(' ',2)[0]
            if l[0] != "<":
                if l[0] != "_" and l0[0]!='_': #If not blank node
                    att_triples.append(line)
            else:
                if l0[0] != "_": #If not blank node
                    rel_triples.append(line)

    fname = data_path.split('/')[-1]
    fname = fname.split('_')[0]
    with open(INPUT_DIR+fname+'_att_triples', 'w') as f:
        for p in att_triples:
            f.write(p)

    path = data_path.rpartition('/')[0]
    with open(path+'/'+fname+'_rel_triples', 'w') as f:
        for p in rel_triples:
            f.write(p)

def create_ent_id_files(fname):
    """Creates 2 files (1 for each KG) containing the KG entities, each of which
    assigned a unique ID.
    """
    # Assign unique integer IDs to each entity URI in both KG files
    count = 0
    for i in range(2):
        ent_dict = {}
        name = fname[i]
        with open(name, "r") as f:
            for line in f.readlines():
                h, r, t = line.rstrip('\n').split(' ',2)
                head_tail = []
                if not h.startswith('_:'):
                    h = h.strip('<>')
                    head_tail.append(h)
                    if t.startswith('<'):
                        t = t.strip('<>')
                        t = t.strip('> .')
                        head_tail.append(t)
                    for ent in head_tail:
                        if ent not in ent_dict:
                            e_id = count
                            ent_dict[ent] = str(e_id)
                            count+=1

        name = name.split(r"./raw_files/")[-1]
        with open(PATH+name+"_ids", 'w') as f:
            for key in ent_dict.keys():
                f.write(ent_dict[key]+"\t"+key+"\n")

def create_ref_align():
    """Creates reference alignment file based on the unique IDs of entities.
    """
    # Map original entity URIs to integer IDs to build reference alignment
    ent_dict_1 = {}
    with open(PATH+"ent_ids_1", "r") as f:
        for line in f.readlines():
            ent_id, ent_url = line.split('\t')
            ent_url = ent_url[:-1]
            ent_url = ent_url.strip()
            ent_dict_1[ent_url] = str(ent_id)

    ent_dict_2 = {}
    with open(PATH+"ent_ids_2", "r") as f:
        for line in f.readlines():
            ent_id, ent_url = line.split('\t')
            ent_url = ent_url[:-1]
            ent_url = ent_url.strip()
            ent_dict_2[ent_url] = str(ent_id)

    pair_ent_ids = []
    with open("./raw_files/same_as", "r") as f:
            for line in f.readlines():
                ent1, ent2 = line.split()
                if ent1 in ent_dict_1:
                    pair_ent_ids.append(ent_dict_1[ent1]+'\t'+ent_dict_2[ent2])

    with open('./raw_files/ref_align', 'w') as f:
        for p in pair_ent_ids:
            f.write(p+'\n')
            
    pair_ent_ids = {}
    with open("./raw_files/same_as", "r") as f:
        for line in f.readlines():
            ent1, ent2 = line.split()
            if ent1 in ent_dict_1:
                pair_ent_ids[ent1] = ent2
    print("Number of aligned entities: ", len(pair_ent_ids))
    with open('./raw_files/ref_align2', 'w') as f:
        for k, v in pair_ent_ids.items():
            f.write(k+'\t'+v+'\n')
            
def create_rel_ids_files(fname):
    """Create files assigning unique IDs to relation properties in each KG.
    """
    # Assign unique integer IDs to each relation predicate in both KG files
    rel_dict1 = {}
    count = 0
    with open(fname[0], "r") as f:
        for line in f.readlines():
            h, r, t = line.rstrip('\n').split(' ',2)
            rel = r.strip('<>')
            if rel not in rel_dict1.keys():
                rel_dict1[rel] = str(count)
                count +=1
    name = fname[0].split(r"./raw_files/")[-1]
    with open(PATH+name+"_rel_ids", 'w') as f:
        for key in rel_dict1.keys():
            f.write(rel_dict1[key]+"\t"+key+"\n")

    rel_dict2 = {}
    with open(fname[1], "r") as f:
        for line in f.readlines():
            h, r, t = line.rstrip('\n').split(' ',2)
            rel = r.strip('<>')
            if rel not in rel_dict2.keys():
                rel_dict2[rel] = str(count)
                count +=1

    name = fname[1].split(r"./raw_files/")[-1]
    with open(PATH+name+"_rel_ids", 'w') as f:
        for key in rel_dict2.keys():
            f.write(rel_dict2[key]+"\t"+key+"\n")

if __name__ == '__main__':
    # Execute full data‐preparation pipeline: split triples, assign IDs, build alignments
    
    print("----------------create attribute and relation triples files--------------------")
    for fname in [PATH_DATA+'_triples', PATH+'en_triples']:
        create_att_rel_triples_files(fname)

    print("----------------create entity id files--------------------")
    fname = [PATH_DATA+'_triples', PATH+'en_triples']
    create_ent_id_files(fname)
    os.rename(PATH+DATASET+'_triples_ids', PATH+'ent_ids_1')
    os.rename(PATH+'en_triples_ids', PATH+'ent_ids_2')

    print("----------------create id reference alignment file--------------------")
    create_ref_align()

    print("----------------create relation id files--------------------")
    fname = [PATH_DATA+'_rel_triples', PATH+'en_rel_triples']
    create_rel_ids_files(fname)
    os.rename(PATH+DATASET+'_rel_triples_rel_ids', PATH+'rel_ids_1')
    os.rename(PATH+'en_rel_triples_rel_ids', PATH+'rel_ids_2')

    #print("-------Copying relation triple files to MultiKE Input------------")
    os.rename(PATH+DATASET+'_rel_triples', INPUT_DIR+'rel_triples_1')
    os.rename(PATH+'en_rel_triples', INPUT_DIR+'rel_triples_2')
    #print("-------Copying reference alignment file to MultiKE Input------------")
    os.rename(PATH+'ref_align2', INPUT_DIR+'ent_links')
  
    #print("-------Renaming triple files to MultiKE Input------------")
    os.rename(INPUT_DIR+DATASET+'_att_triples', INPUT_DIR+'attr_triples_1')
    os.rename(INPUT_DIR+'en_att_triples', INPUT_DIR+'attr_triples_2')

    #Delete unnecessary files
    #os.popen('rm {}ref_ent_ids'.format(INPUT_DIR))

    sys.stdout = orig_stdout
    f.close()
