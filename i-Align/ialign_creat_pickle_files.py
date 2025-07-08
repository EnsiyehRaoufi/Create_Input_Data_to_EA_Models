"""
    Utility to build pickle files for IALIGN:
    - Map attribute predicates to IDs
    - Build entity and predicate vocabularies
    - Generate seed/test splits of entity alignment
    - Assemble KG entity and attribute feature dictionaries
    """
import os
import re
import string
import pickle
import random
from sklearn.model_selection import train_test_split
import numpy as np
from Param import *
import sys

orig_stdout = sys.stdout
f = open('out.txt', 'w')
# Redirect all print output to out.txt for easier debugging
sys.stdout = f

def attr_ids():
     """
        Read attribute triples for each KG and assign each unique predicate a new ID.
        Outputs files attr_ids_1 and attr_ids_2 mapping ID→predicate URL.
        """
    # Loop over KG1 and KG2 to build predicate→ID maps
    for i in range(2):
        att_dict = {}
        count = 0
        # Read attribute triples for KG i+1
        with open(PATH+'attr_triples_'+str(i+1), "r") as f:
            for line in f.readlines():
                _, r, _ = line.rstrip('\n').split('\t',2)
                r = r.strip('<>')
                if r not in att_dict:
                    att_dict[r] = count
                    count +=1

        # Write predicate ID→URL mappings
        with open(PATH+"att_ids_"+str(i+1), "w") as f:
            for key in att_dict.keys():
                f.write(str(att_dict[key])+"\t"+key+'\n')

def kg_ent_vocab():
    """Creates dictionary of entity ids (vocabs) of each of which KGs. The ids
    should start from 1 in KG1 and should be continued in KG2.
    """
    for i in range(2):
        ents = {}
        with open(PATH+'ent_ids_'+str(i+1), "r") as f:
            for line in f.readlines():
                l=line.rstrip('\n').split('\t')
                ents[l[1]] = int(l[0])+1
        with open(INPUT_DIR+'KG'+str(i+1)+'_ent_vocab', 'wb') as handle:
            pickle.dump(ents, handle, protocol=pickle.HIGHEST_PROTOCOL)

def kg_pred_vocab():
    """Creates a dictionary of all relation and attribute predicates of the two KGs by
    assigning unique ids starting from 1
    """
    preds = {}
    count = 1
    for i in range(2):
        with open(PATH+'att_ids_'+str(i+1), "r") as f:
            for line in f.readlines():
                l=line.rstrip('\n').split('\t')
                if l[1] not in preds:
                    preds[l[1]] = count
                    count +=1
        with open(PATH+'rel_ids_'+str(i+1), "r") as f:
            for line in f.readlines():
                l=line.rstrip('\n').split('\t')
                if l[1] not in preds:
                    preds[l[1]] = count
                    count +=1
    preds['SELF-REL']= count
    with open(INPUT_DIR+'pred_vocab', 'wb') as handle:
        pickle.dump(preds, handle, protocol=pickle.HIGHEST_PROTOCOL)

def kg_seed_test_data():
    """
    Map entity URLs from ent_ids files to integer IDs,
    split aligned pairs into seed (30%) and test (70%) sets,
    and serialize them as seed_data and test_data pickles.
    """
    # Map KG1 entity URLs to new integer IDs (+1)
    ent_dict_1 = {}
    with open(PATH+"ent_ids_1", "r") as f:
        for line in f.readlines():
            ent_id, ent_url = line.split('\t')
            ent_url = ent_url[:-1]
            ent_url = ent_url.strip()
            ent_dict_1[ent_url] = int(ent_id)+1

    # Map KG2 entity URLs to new integer IDs (+1)
    ent_dict_2 = {}
    with open(PATH+"ent_ids_2", "r") as f:
        for line in f.readlines():
            ent_id, ent_url = line.split('\t')
            ent_url = ent_url[:-1]
            ent_url = ent_url.strip()
            ent_dict_2[ent_url] = int(ent_id)+1

    pair_ent_ids = []
    # Read reference alignment links
    with open(PATH+"ent_links", "r") as f:
            for line in f.readlines():
                ent1, ent2 = line.split()
                if ent1 in ent_dict_1:
                    pair_ent_ids.append([ent_dict_1[ent1], ent_dict_2[ent2]])

    # 30% seed, 70% test
    seed, test_pairs = train_test_split(pair_ent_ids, test_size=0.7, shuffle=False)
    with open(INPUT_DIR+'seed_data', 'wb') as handle:
        pickle.dump(np.array(seed), handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Randomize test pairs before saving
    random.shuffle(test_pairs)
    with open(INPUT_DIR+'test_data', 'wb') as handle:
        pickle.dump(np.array(test_pairs), handle, protocol=pickle.HIGHEST_PROTOCOL)

def kg_entities():
    """Creates a dictionary of entities for each KG. The key_value of each entity
     contains max 4 tuples of (relation_id, entity_id)
    """

    # Load predicate→ID vocab
    pred_ids = pickle.load(open(INPUT_DIR+'pred_vocab', "rb"))
    for i in range(2):
        entities = {}
        ent_ids = pickle.load(open(INPUT_DIR+'KG'+str(i+1)+'_ent_vocab', "rb"))
        # Read relation triples for KG i+1
        with open(PATH+'rel_triples_'+str(i+1), "r") as f:
            rel_tri = f.readlines()
        for tri in rel_tri: # Collect up to 4 (predicate,entity) pairs per head entity
            h, r, t = tri.rstrip('\n').split('\t',2)
            if ent_ids[h] not in entities:
                entities[ent_ids[h]] = [(pred_ids[r], ent_ids[t])]
            else:
                if len(entities[ent_ids[h]])<5:
                 entities[ent_ids[h]].append((pred_ids[r], ent_ids[t]))
        for e in ent_ids:
            if ent_ids[e] not in entities: # Ensure every entity has at least 4 neighbor slots
                entities[ent_ids[e]] = [(0, 0)]*4
        for e in entities:
            l = len(entities[e])
            if l<4: # Pad shorter lists to length 4 with (0,0) tuples
                for j in range(4-l):
                    entities[e].append((0,0))
        with open(INPUT_DIR+'KG'+str(i+1)+'_ENTITIES', 'wb') as handle:
            pickle.dump(entities, handle, protocol=pickle.HIGHEST_PROTOCOL)

def kg_attributes():
    """
    Encode up to 10 characters per literal value as integer sequences,
    pad to length 10, group up to 20 attributes per entity,
    and serialize KG attribute feature dictionaries and updated char_vocab.
    """
    # Load existing character vocabulary
    pred_ids = pickle.load(open(INPUT_DIR+'pred_vocab', "rb"))
    char_ids = pickle.load(open(PATH+'char_vocab', "rb"))
    #find max id number in char_vocab to add more chars if necessary
    max_id = -1
    for c, v in char_ids.items():
        if char_ids[c]>max_id:
            max_id = char_ids[c]
    print("Number of characters in char_vocab: ", max_id)
    for i in range(2):
        entities = {}
        ent_ids = pickle.load(open(INPUT_DIR+'KG'+str(i+1)+'_ent_vocab', "rb"))
        # Read attribute triples for KG i+1
        with open(PATH+'attr_triples_'+str(i+1), "r") as f:
            rel_tri = f.readlines()
        for tri in rel_tri:
            h, r, t = tri.rstrip('\n').split('\t',2)
            # Remove surrounding quotes from literal value
            t = t.strip('""')

            encoded_val = []
            count = 0
            for char in t:
                # Encode up to first 10 characters of the literal
                if count<10: # Pad shorter sequences to exactly 10 character IDs
                    if char in char_ids:
                        encoded_val.append(char_ids[char])
                    else:
                        max_id +=1
                        char_ids[char] = max_id
                        print("New character: ", char)
                        encoded_val.append(char_ids[char])

                    count+=1
            l = len(encoded_val)
            if l<10:
                for j in range(10-l):
                    encoded_val.append(0)

            # Initialize attribute list for new entity
            if ent_ids[h] not in entities:
                entities[ent_ids[h]] = [(pred_ids[r], encoded_val)]
            else:
                if len(entities[ent_ids[h]])<20:
                    entities[ent_ids[h]].append((pred_ids[r], encoded_val))

        #if entities in the dict has less than 20 attributes, we add some zero_attr
        #to do padding
        zero_attr = (0, [0]*10)
        for k,v in entities.items():
            if len(v)<20:
                for j in range(20-len(v)):
                    entities[k].append(zero_attr)
        #if there are some entities with no attributes just add them to the dictionary
        #we assign 20 zero_attr to such entities
        for e in ent_ids:
            if ent_ids[e] not in entities:
                entities[ent_ids[e]] = [zero_attr]*20

        with open(INPUT_DIR+'KG'+str(i+1)+'_ATTRIBUTES', 'wb') as handle:
            pickle.dump(entities, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # Save updated character vocabulary
    with open(INPUT_DIR+'char_vocab', 'wb') as handle:
        pickle.dump(char_ids, handle, protocol=pickle.HIGHEST_PROTOCOL)

def cleanse_data():
    """Set delimiters in attribute/relation triples and the reference alignment
    files to be tab(\t)
    """
    # Normalize ent_links to tab-delimited format
    with open(PATH+'ent_links', "r") as f:
        flag = True
        modified_ref = []
        for line in f.readlines():
            ll = line.rstrip('\n').split(' ')
            if len(ll)!=2:
                flag = False
                break
            else:
                h, t = ll
                modified_ref.append((h,t))
        if flag:
            with open(PATH+'ent_links', "w") as f:
                for tup in modified_ref:
                    f.write(tup[0]+'\t'+tup[1]+'\n')
    for i in range(2):
        # Normalize attribute triples to tabs
        with open(PATH+'attr_triples_'+str(i+1), "r") as f:
            modified_tri = []
            flag = True
            for line in f.readlines():
                ll = line.rstrip('\n').split(' ',2)
                if len(ll)!=3:
                    flag = False
                    break
                else:
                    h, r, t = ll
                    h = h.strip('<>')
                    r = r.strip('<>')
                    t = t.rstrip(' .')
                    modified_tri.append((h,r,t))
            if flag:
                with open(PATH+'attr_triples_'+str(i+1), "w") as f:
                    for tri in modified_tri:
                        f.write(tri[0]+'\t'+tri[1]+'\t'+tri[2]+'\n')

        # Normalize relation triples to tabs
        with open(PATH+'rel_triples_'+str(i+1), "r") as f:
            modified_tri = []
            for line in f.readlines():
                ll = line.rstrip('\n').split(' ',2)
                if len(ll)==3:
                    h, r, t = ll
                    h = h.strip('<>')
                    r = r.strip('<>')
                    t = t.strip('<>')
                    t = t.rstrip('> .')
                    modified_tri.append((h,r,t))
            if len(ll)==3:
                with open(PATH+'rel_triples_'+str(i+1), "w") as f:
                    for tri in modified_tri:
                        f.write(tri[0]+'\t'+tri[1]+'\t'+tri[2]+'\n')

if __name__ == '__main__':
     # Execute full pipeline: cleanse → attribute IDs → entity & predicate vocabs → seed/test → KG entities → KG attributes

    print("----------------cleanse data and remove <> from triples--------------------")
    cleanse_data()
    print("----------------create attribute predicates IDs--------------------")
    attr_ids()
    print("----creating entity vocab dictionary file----")
    kg_ent_vocab()
    print("----creating predicate vocab dictionary file----")
    kg_pred_vocab()
    print("----------------creating seed and test data file--------------------")
    kg_seed_test_data()
    print("----------------creating KG entities file--------------------")
    kg_entities()
    print("----------------creating KG attributes file--------------------")
    kg_attributes()
    # Restore original console output
    sys.stdout = orig_stdout
    # Close logging file out.txt
    f.close()
