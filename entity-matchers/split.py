"""
Generate multiple random train/validation/test splits from an input file, because it is needed as standard input to the entity-matchers.
Loads lines, shuffles them, splits according to specified ratios (as tenths),
and writes each fold’s splits into organized subdirectories.
"""
import random
from Param import *
import os

# Load the data from a .txt file
def load_data(file_path):
        """
        Read all lines from the specified file into a list of strings.
        """

    with open(file_path, 'r') as file:
        data = file.readlines()  # Reads the file line by line
    return data

# Shuffle the data randomly
def shuffle_data(data):
        """
        Randomly shuffle the list of data entries in-place and return it.
        """

    random.shuffle(data)
    return data

# Split the data into train (70%), validation (20%), and test (10%)
def split_data(data, train_ratio=2, val_ratio=1, test_ratio=7):
        """
        Split data into train/validation/test subsets based on ratio parameters.
        Ratios are out of 10 (e.g. train_ratio=7 → 70%).
        """

    total_size = len(data)
    # Compute number of training samples from ratio
    train_size = int(train_ratio * total_size*0.1)
    # Compute number of validation samples from ratio
    val_size = int(val_ratio * total_size*0.1)

    train_data = data[:train_size]
    val_data = data[train_size:train_size + val_size]
    test_data = data[train_size + val_size:]

    return train_data, val_data, test_data

# Save the train, validation, and test splits to files
def save_split(train_data, val_data, test_data, out_dir):
        """
    Write train_data, val_data, and test_data lists to files named
    train_links, valid_links, and test_links under out_dir.
    """
    # Save the train, validation, and test splits into separate files for each random split

    train_file = out_dir+'/train_links'
    val_file = out_dir+'/valid_links'
    test_file = out_dir+'/test_links'

    with open(train_file, 'w') as f_train, open(val_file, 'w') as f_val, open(test_file, 'w') as f_test:
        f_train.writelines(train_data)
        f_val.writelines(val_data)
        f_test.writelines(test_data)

# Full process to generate 5 independent random splits
def generate_random_splits(file_path, num_splits=5):
        """
    Perform the full random‐split pipeline num_splits times:
    load data, compute train ratio, create directories,
    shuffle, split, and save each fold’s results.
    """

    data = load_data(file_path)

    # Calculate train_ratio so that train+val+test = 10 (100%)
    TRAIN_SIZE = 10-(VAL_SIZE+TEST_SIZE)
    # Build output directory name from split ratios and fold count
    output_dir = INPUT_DIR+"{}{}{}_{}folds".format(TEST_SIZE, TRAIN_SIZE, VAL_SIZE, NUM_FOLD)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for split_num in range(1, num_splits + 1):
        out = output_dir +'/'+str(split_num)
        if not os.path.exists(out):
            os.makedirs(out)
        # Shuffle a fresh copy of the data for this fold
        shuffled_data = shuffle_data(data.copy()) 
        # Divide shuffled data into train/val/test sets
        train_data, val_data, test_data = split_data(shuffled_data,
                    train_ratio = TRAIN_SIZE,
                    val_ratio = VAL_SIZE,
                    test_ratio = TEST_SIZE)  # Split the shuffled data
        # Save this fold’s splits to files
        save_split(train_data, val_data, test_data, out)  # Save each split

# Example usage
file_path = INPUT_DIR +'ent_links'  # Path to your .txt file
generate_random_splits(file_path, num_splits=5)
