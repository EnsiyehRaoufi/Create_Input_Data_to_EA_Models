"""
Generate train/test/validation splits for entity alignment links.
Reads a tab-delimited ent_links file and writes out three files
(train_links, test_links, valid_links) under a size-named subdirectory.
"""

from sklearn.model_selection import train_test_split
import os
from Param import *

def create_sup_ref_pairs(fname, test_size=6, train_size=3, val_size=1):
    """
    Split the input linkage file into train/test/validation subsets based on percentage.

    Args:
        fname (str): Name of the input file under INPUT_DIR.
        test_size (int): Percentage for the test set (e.g. 3 → 30%).
        train_size (int): Percentage for the training set (e.g. 6 → 60%).
        val_size (int): Percentage for the validation set (e.g. 1 → 10%).
    """
    pairs_list = []
    # Open input file and load all reference pairs into a list
    with open(INPUT_DIR +fname, "r") as f:
        for line in f.readlines():
            # Each line is one “source<TAB>target” entry (including newline)
            pairs_list.append(line)
            
    # Split off the training set; remaining goes to test+validation
    pair_train, pair_test = train_test_split(pairs_list, test_size=(test_size+val_size)/10, shuffle=False)
    # Split remaining pairs into test and validation sets
    pair_test, pair_val = train_test_split(pair_test, test_size=val_size/10, shuffle=False)
    
    # Build output folder name based on sizes (e.g. “631” for 6/3/1)
    folder_name = str(test_size)+str(train_size)+str(val_size)
    train_val_test_dir = INPUT_DIR + folder_name +'/'
    # Check if the directory already exists
    if not os.path.exists(train_val_test_dir):
        # Create directory for the three output link files if it doesn’t exist
        os.makedirs(train_val_test_dir)
        
    # Write each training pair (tab-delimited) to train_links
    with open(train_val_test_dir+'/train_links', 'w') as f:
        for p in pair_train:
            p = p.strip('\n').split('\t')
            f.write(p[0]+'\t'+p[1]+'\n')
            
    # Write each test pair to test_links
    with open(train_val_test_dir+'/test_links', 'w') as f:
        for p in pair_test:
            p = p.strip('\n').split('\t')
            f.write(p[0]+'\t'+p[1]+'\n')
            
    # Write each validation pair to valid_links
    with open(train_val_test_dir+'/valid_links', 'w') as f:
        for p in pair_val:
            p = p.strip('\n').split('\t')
            f.write(p[0]+'\t'+p[1]+'\n')
            
# Execute split using constants TEST, TRAIN, VAL from Param
create_sup_ref_pairs('ent_links', TEST, TRAIN, VAL)
