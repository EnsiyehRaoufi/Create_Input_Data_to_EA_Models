from sklearn.model_selection import train_test_split
import os
from Param import *

def create_sup_ref_pairs(fname, test_size=6, train_size=3, val_size=1):
    pairs_list = []
    with open(INPUT_DIR +fname, "r") as f:
        for line in f.readlines():
            pairs_list.append(line)

    pair_train, pair_test = train_test_split(pairs_list, test_size=(test_size+val_size)/10, shuffle=False)
    pair_test, pair_val = train_test_split(pair_test, test_size=val_size/10, shuffle=False)

    folder_name = str(test_size)+str(train_size)+str(val_size)
    train_val_test_dir = INPUT_DIR + folder_name +'/'
    # Check if the directory already exists
    if not os.path.exists(train_val_test_dir):
        os.makedirs(train_val_test_dir)

    with open(train_val_test_dir+'/train_links', 'w') as f:
        for p in pair_train:
            p = p.strip('\n').split('\t')
            f.write(p[0]+'\t'+p[1]+'\n')

    with open(train_val_test_dir+'/test_links', 'w') as f:
        for p in pair_test:
            p = p.strip('\n').split('\t')
            f.write(p[0]+'\t'+p[1]+'\n')

    with open(train_val_test_dir+'/valid_links', 'w') as f:
        for p in pair_val:
            p = p.strip('\n').split('\t')
            f.write(p[0]+'\t'+p[1]+'\n')

create_sup_ref_pairs('ent_links', TEST, TRAIN, VAL)
