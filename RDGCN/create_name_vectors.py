import numpy as np
from Param import *
import json
import time
import string

def loadGloveModel(gloveFile):
    print("Loading Glove Model...")
    f = open(gloveFile,'r', encoding='utf8')
    model = {}
    for line in f:
        splitLine = line.split(' ')
        word = splitLine[0]
        embedding = np.asarray(splitLine[1:], dtype='float32')
        model[word] = embedding
    #print(type(embedding), embedding)
    #print(model.keys())
    print("Done.",len(model)," words loaded!")
    return model

def get_name(uri):
    ent_name = uri.split(r"/")[-1]
    for punctuation in string.punctuation:
        ent_name = ent_name.replace(punctuation, ' ')
    split_text = ent_name.split()
    ent_name = ' '.join(split_text)
    ent_name = ent_name #.lower()
    #print(ent_name)
    return ent_name #name can be consist of several words

def get_ent_names():
    """Returns a dictionary of all enities in the two KGs with entity id
    as key and entity name as the value.
    """
    print("Extracting entity names for dataset: ", DATASET)
    ent_dict = {}
    for i in [1,2]:
        with open(INPUT_DIR+"ent_ids_"+str(i), "r") as f:
            for line in f.readlines():
                ent_id, ent_uri = line.split('\t')
                ent_uri = ent_uri[:-1]
                ent_dict[int(ent_id)] = get_name(ent_uri)
    print("Done.",len(ent_dict)," names extracted!")
    return ent_dict

def rand_vec_generat(DIM=300):
    """generates random initial vectors if the entity name does not exist in Glove
    """
    return(list(np.random.uniform(-1, 1, DIM)).copy())

def uniq_rel(fnames):
    triple_list = []
    for fname in fnames:
        with open(INPUT_DIR+fname, 'r') as f:
            triple_list.append(f.readlines())
    uniq = []
    for triples in triple_list:
        for line in triples:
            rel = line.rstrip('\n').split('\t')[1]
            if rel not in uniq:
                uniq.append(rel)
    for i in range(len(uniq)):
        uniq[i] = int(uniq[i])
    uniq.sort()
    for i in range(len(uniq)):
        uniq[i] = str(uniq[i])
    return uniq.copy()


def substitude(fname, uniq_rel_dict):
    changed_lines = []
    with open(INPUT_DIR+fname, 'r') as f:
        lines = f.readlines()
        for line in lines:
            l = line.split('\t')
            l[1] = uniq_rel_dict[l[1]]
            changed_lines.append(l)
    return changed_lines.copy()

def cheq_continu():
    l = 0
    uniq_list = {}
    for i in range(2):
        l = len(uniq_list)
        with open(INPUT_DIR+'triples_'+str(i+1), "r") as f:
            uniq_list = {}
            for line in f.readlines():
                ll = line.rstrip('\n').split('\t',2)
                _, r, _  = ll
                if r not in uniq_list.keys():
                    uniq_list[r] = 0
            uniq_list = list(uniq_list.keys())
            uniq_list = [int(i) for i in uniq_list]
            uniq_list.sort()

    return l+len(uniq_list)==uniq_list[-1]+1


def uniq_relation():
    """Checks and modifies relation ids in kg1 and kg2 to be unique, continuous and starts from zero
    """
    if not cheq_continu():
        print("There is necessary for RDGCN model that relation ids in kg1 and kg2 \
        to be unique, continuous and starts from zero. Working on relations ids...")
        fnames = ['triples_1', 'triples_2']
        uniq = uniq_rel(fnames)
        with open(PATH+'uniq_rel_ids', 'w') as res:
            for u in uniq:
                res.write(str(u)+'\n')

        uniq_rel_dict = {}
        for u in range(len(uniq)):
            uniq_rel_dict[uniq[u]] = str(u)
        #Save triples_1 and triples_2 in uniq relations
        for fname in fnames:
            changed_lines = substitude(fname, uniq_rel_dict)
            with open(INPUT_DIR+fname, 'w') as f:
                for l in changed_lines:
                    f.write(str(l[0])+'\t'+str(l[1])+'\t'+str(l[2]))
        #save unique relations in result2 and check again
        print("Relation predicate ids are now unique, continuous and starts from zero: ", cheq_continu())


if __name__ == '__main__':
    start = time.time()
    uniq_relation()
    initial_emb_model = loadGloveModel(PRETRAINED_TEXT_EMB_MODEL)
    ent_name_dict = get_ent_names() #dictionary of all entity names
    ent_ids =  list(ent_name_dict.keys())
    ent_names = [ent_name_dict[id] for id in ent_ids]
    ent_vectors = [] #list of entity initial vectors
    count = 0
    for name in ent_names:
        flag = False
        emb = []
        words = name.split()
        for word in words:
            if word in initial_emb_model.keys():
                flag = True
                n_vec = initial_emb_model[word].tolist()
                if not emb:
                    emb = n_vec.copy()
                else:
                    emb = [(x + y)/2 for x, y in zip(emb, n_vec)]
        if flag:
            ent_vectors.append(emb)
        else:
            count +=1
            ent_vectors.append(rand_vec_generat())
    print("{} vectors given from {} model, and {} random vectors generated!".format(len(ent_names)-count, PRETRAINED_TEXT_EMB_MODEL, count))
    with open(INPUT_DIR+DATASET+'_vectorList.json', 'w') as f:
        json.dump(ent_vectors, f)
    print("Runtime: ", time.time()-start)
